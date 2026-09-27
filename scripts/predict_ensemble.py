#!/usr/bin/env python3
"""Blend the strongest style model with the complementary visual transfer model."""
import argparse
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from emoji_provider.data import image_id, list_images  # noqa: E402
from emoji_provider.features import extract_many  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create the best blended Kaggle submission.")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--style-model", type=Path, default=ROOT / "outputs/models/style_boosting.joblib")
    parser.add_argument("--visual-model", type=Path, default=ROOT / "outputs/models/mobilenet_v3.keras")
    parser.add_argument("--style-weight", type=float, default=0.5)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/submissions/best_ensemble.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not 0 <= args.style_weight <= 1:
        raise ValueError("--style-weight must be between 0 and 1")
    from tensorflow import keras
    from emoji_provider.cnn import make_dataset

    paths = list_images(args.data_dir / "test")
    artifact = joblib.load(args.style_model)
    config = artifact["config"]
    style_x = extract_many(
        paths, config["histogram_bins"], config["image_size"], config["feature_method"]
    )
    style_model = artifact["model"]
    style_probabilities = style_model.predict_proba(style_x)

    metadata = json.loads(args.visual_model.with_suffix(".json").read_text())
    visual_classes = np.asarray(metadata["classes"])
    visual_config = metadata["config"]
    dataset = make_dataset(
        paths, np.zeros(len(paths), dtype=np.int32), visual_config["image_size"],
        visual_config["batch_size"], False, visual_config["seed"],
    )
    visual_probabilities = keras.models.load_model(args.visual_model).predict(dataset, verbose=0)
    if not np.array_equal(style_model.classes_, visual_classes):
        raise ValueError("Models do not use the same class order")

    probabilities = (
        args.style_weight * style_probabilities
        + (1.0 - args.style_weight) * visual_probabilities
    )
    prediction = visual_classes[probabilities.argmax(axis=1)]
    submission = pd.DataFrame({"Id": [image_id(path) for path in paths], "Label": prediction})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    submission.to_csv(args.output, index=False)
    print(f"Saved {len(submission)} blended predictions to: {args.output}")


if __name__ == "__main__":
    main()
