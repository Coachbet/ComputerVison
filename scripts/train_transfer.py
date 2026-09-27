#!/usr/bin/env python3
"""Train an ImageNet-pretrained MobileNetV3 and fine-tune its last layers."""
import argparse
import json
import os
import random
import sys
from pathlib import Path

import numpy as np
import yaml
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from emoji_provider.data import load_training_table  # noqa: E402
from emoji_provider.tracking import append_result  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train and fine-tune MobileNetV3.")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--config", type=Path, default=ROOT / "configs/transfer.yaml")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/models/mobilenet_v3.keras")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = yaml.safe_load(args.config.read_text())
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    import pandas as pd
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    from emoji_provider.cnn import make_dataset

    seed = config["seed"]
    random.seed(seed); np.random.seed(seed); tf.random.set_seed(seed)
    table = load_training_table(args.data_dir)
    classes = sorted(table.Label.astype(str).unique())
    mapping = {label: i for i, label in enumerate(classes)}
    y = table.Label.astype(str).map(mapping).to_numpy()
    indices = np.arange(len(table))
    train_idx, val_idx = train_test_split(
        indices, test_size=config["validation_size"], random_state=seed, stratify=y
    )
    train_ds = make_dataset(
        table.iloc[train_idx].path.tolist(), y[train_idx], config["image_size"],
        config["batch_size"], True, seed,
    )
    val_ds = make_dataset(
        table.iloc[val_idx].path.tolist(), y[val_idx], config["image_size"],
        config["batch_size"], False, seed,
    )
    weights = compute_class_weight("balanced", classes=np.arange(len(classes)), y=y[train_idx])
    class_weights = dict(enumerate(weights.astype(float)))

    base = keras.applications.MobileNetV3Small(
        input_shape=(config["image_size"], config["image_size"], 3), include_top=False,
        weights="imagenet", pooling="avg", include_preprocessing=True,
    )
    base.trainable = False
    inputs = keras.Input((config["image_size"], config["image_size"], 3))
    x = keras.Sequential([
        layers.RandomRotation(0.03), layers.RandomTranslation(0.04, 0.04),
        layers.RandomContrast(0.08),
    ], name="augmentation")(inputs)
    x = layers.Rescaling(255.0)(x)
    x = base(x, training=False)
    x = layers.Dropout(0.30)(x)
    outputs = layers.Dense(len(classes), activation="softmax")(x)
    model = keras.Model(inputs, outputs, name="emoji_mobilenet_v3")

    callbacks = [keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=config["early_stopping_patience"], restore_best_weights=True
    )]
    model.compile(
        keras.optimizers.Adam(config["head_learning_rate"]),
        "sparse_categorical_crossentropy", metrics=["accuracy"],
    )
    model.fit(
        train_ds, validation_data=val_ds, epochs=config["head_epochs"],
        class_weight=class_weights, callbacks=callbacks,
    )
    head_weights = model.get_weights()
    head_prediction = model.predict(val_ds, verbose=0).argmax(1)
    head_f1 = f1_score(y[val_idx], head_prediction, average="macro")

    base.trainable = True
    for layer in base.layers[:-30]:
        layer.trainable = False
    model.compile(
        keras.optimizers.Adam(config["fine_tune_learning_rate"]),
        "sparse_categorical_crossentropy", metrics=["accuracy"],
    )
    model.fit(
        train_ds, validation_data=val_ds, epochs=config["fine_tune_epochs"],
        class_weight=class_weights, callbacks=callbacks,
    )

    pred = model.predict(val_ds, verbose=0).argmax(1)
    if head_f1 > f1_score(y[val_idx], pred, average="macro"):
        model.set_weights(head_weights)
        pred = head_prediction
    accuracy = accuracy_score(y[val_idx], pred)
    macro_f1 = f1_score(y[val_idx], pred, average="macro")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    model.save(args.output)
    args.output.with_suffix(".json").write_text(json.dumps({
        "model_type": "transfer", "classes": classes, "config": config,
    }, indent=2))
    metrics = ROOT / "outputs/metrics"; metrics.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(classification_report(y[val_idx], pred, target_names=classes, output_dict=True)).T.to_csv(
        metrics / "mobilenet_v3_transfer_learning_classification_report.csv"
    )
    pd.DataFrame(confusion_matrix(y[val_idx], pred), index=classes, columns=classes).to_csv(
        metrics / "mobilenet_v3_transfer_learning_confusion_matrix.csv"
    )
    append_result(ROOT / "experiments/results.csv", {
        "experiment": "mobilenet_v3_transfer_learning", "validation_accuracy": accuracy,
        "validation_macro_f1": macro_f1, "kaggle_score": "",
        "notes": "ImageNet pretrained MobileNetV3Small with fine-tuning",
    })
    print(f"Validation accuracy: {accuracy:.4f}")
    print(f"Validation macro F1: {macro_f1:.4f}")
    print(f"Model saved to: {args.output}")


if __name__ == "__main__":
    main()
