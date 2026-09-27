#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emoji_provider.data import image_id, list_images  # noqa: E402
from emoji_provider.features import extract_many  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Kaggle submission.")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--model", type=Path, default=ROOT / "outputs/models/baseline.joblib")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/submissions/submission.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    artifact = joblib.load(args.model)
    paths = list_images(args.data_dir / "test")
    config = artifact["config"]
    x_test = extract_many(
        paths, config["histogram_bins"], config["image_size"],
        config.get("feature_method", "color"),
    )
    submission = pd.DataFrame({
        "Id": [image_id(path) for path in paths],
        "Label": artifact["model"].predict(x_test),
    })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    submission.to_csv(args.output, index=False)
    print(f"Saved {len(submission)} predictions to: {args.output}")


if __name__ == "__main__":
    main()
