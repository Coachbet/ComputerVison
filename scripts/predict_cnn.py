#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emoji_provider.data import image_id, list_images  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Kaggle submission with the CNN.")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--model", type=Path, default=ROOT / "outputs/models/lenet_cnn.keras")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/submissions/cnn_submission.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    from tensorflow import keras
    from emoji_provider.cnn import make_dataset

    metadata = json.loads(args.model.with_suffix(".json").read_text())
    config = metadata["config"]
    classes = np.asarray(metadata["classes"])
    paths = list_images(args.data_dir / "test")
    dummy = np.zeros(len(paths), dtype=np.int32)
    dataset = make_dataset(paths, dummy, config["image_size"], config["batch_size"])
    prediction = classes[keras.models.load_model(args.model).predict(dataset, verbose=0).argmax(axis=1)]
    submission = pd.DataFrame({"Id": [image_id(path) for path in paths], "Label": prediction})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    submission.to_csv(args.output, index=False)
    print(f"Saved {len(submission)} predictions to: {args.output}")


if __name__ == "__main__":
    main()
