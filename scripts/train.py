#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

import joblib
import pandas as pd
import yaml
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emoji_provider.data import load_training_table  # noqa: E402
from emoji_provider.features import extract_many  # noqa: E402
from emoji_provider.model import build_model  # noqa: E402
from emoji_provider.tracking import append_result  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the explainable baseline.")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--config", type=Path, default=ROOT / "configs/baseline.yaml")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/models/baseline.joblib")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = yaml.safe_load(args.config.read_text())
    table = load_training_table(args.data_dir)
    x = extract_many(
        table["path"].tolist(), config["histogram_bins"], config["image_size"],
        config.get("feature_method", "color"),
    )
    y = table["Label"].astype(str).to_numpy()
    x_train, x_val, y_train, y_val = train_test_split(
        x, y, test_size=config["validation_size"], random_state=config["seed"], stratify=y
    )
    model = build_model(config, config["seed"])
    model.fit(x_train, y_train)
    prediction = model.predict(x_val)
    accuracy = accuracy_score(y_val, prediction)
    macro_f1 = f1_score(y_val, prediction, average="macro")

    metrics_dir = ROOT / "outputs/metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    experiment = config.get("experiment_name", "model")
    report = pd.DataFrame(classification_report(y_val, prediction, output_dict=True)).T
    report.to_csv(metrics_dir / f"{experiment}_classification_report.csv")
    labels = sorted(set(y))
    matrix = pd.DataFrame(
        confusion_matrix(y_val, prediction, labels=labels), index=labels, columns=labels
    )
    matrix.to_csv(metrics_dir / f"{experiment}_confusion_matrix.csv")

    if config.get("refit_full", True):
        model.fit(x, y)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "config": config}, args.output)
    append_result(ROOT / "experiments/results.csv", {
        "experiment": config.get("experiment_name", "logistic_regression"),
        "validation_accuracy": accuracy,
        "validation_macro_f1": macro_f1, "kaggle_score": "",
        "notes": config.get("notes", "Entraînement automatique"),
    })
    print(f"Validation accuracy: {accuracy:.4f}")
    print(f"Validation macro F1: {macro_f1:.4f}")
    print(f"Model saved to: {args.output}")


if __name__ == "__main__":
    main()
