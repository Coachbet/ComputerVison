#!/usr/bin/env python3
"""Train the strongest engineered-style model."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.argv[1:1] = [
    "--config", str(ROOT / "configs/style_extra_trees.yaml"),
    "--output", str(ROOT / "outputs/models/style_extra_trees.joblib"),
]

from train import main  # noqa: E402


if __name__ == "__main__":
    main()
