#!/usr/bin/env python3
import argparse
import json
import os
import random
import sys
from pathlib import Path

import numpy as np
import yaml
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emoji_provider.data import load_training_table  # noqa: E402
from emoji_provider.tracking import append_result  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a LeNet-style CNN.")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--config", type=Path, default=ROOT / "configs/cnn.yaml")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/models/lenet_cnn.keras")
    parser.add_argument("--epochs", type=int, help="Override the configured epoch count.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = yaml.safe_load(args.config.read_text())
    if args.epochs is not None:
        config["epochs"] = args.epochs

    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    import tensorflow as tf
    from tensorflow import keras
    from emoji_provider.cnn import build_lenet, make_dataset

    seed = config["seed"]
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

    table = load_training_table(args.data_dir)
    classes = sorted(table["Label"].astype(str).unique())
    class_to_index = {label: index for index, label in enumerate(classes)}
    encoded = table["Label"].astype(str).map(class_to_index).to_numpy()
    indices = np.arange(len(table))
    train_idx, val_idx = train_test_split(
        indices, test_size=config["validation_size"], random_state=seed, stratify=encoded
    )
    train_ds = make_dataset(
        table.iloc[train_idx]["path"].tolist(), encoded[train_idx], config["image_size"],
        config["batch_size"], training=True, seed=seed,
    )
    val_ds = make_dataset(
        table.iloc[val_idx]["path"].tolist(), encoded[val_idx], config["image_size"],
        config["batch_size"], training=False, seed=seed,
    )
    weights = compute_class_weight(class_weight="balanced", classes=np.arange(len(classes)), y=encoded[train_idx])
    class_weights = {index: float(weight) for index, weight in enumerate(weights)}
    model = build_lenet(config["image_size"], len(classes), config["learning_rate"])
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=config["early_stopping_patience"],
            restore_best_weights=True,
        ),
        keras.callbacks.ReduceLROnPlateau(monitor="val_loss", patience=2, factor=0.5),
    ]
    model.fit(
        train_ds, validation_data=val_ds, epochs=config["epochs"],
        callbacks=callbacks, class_weight=class_weights,
    )
    prediction = model.predict(val_ds, verbose=0).argmax(axis=1)
    accuracy = accuracy_score(encoded[val_idx], prediction)
    macro_f1 = f1_score(encoded[val_idx], prediction, average="macro")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    model.save(args.output)
    metadata = {"model_type": "cnn", "classes": classes, "config": config}
    args.output.with_suffix(".json").write_text(json.dumps(metadata, indent=2))
    append_result(ROOT / "experiments/results.csv", {
        "experiment": "lenet_cnn_augmented", "validation_accuracy": accuracy,
        "validation_macro_f1": macro_f1, "kaggle_score": "",
        "notes": "LeNet-style CNN, class weights, augmentation, early stopping",
    })
    print(f"Validation accuracy: {accuracy:.4f}")
    print(f"Validation macro F1: {macro_f1:.4f}")
    print(f"Model saved to: {args.output}")


if __name__ == "__main__":
    main()
