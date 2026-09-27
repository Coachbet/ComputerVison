#!/usr/bin/env python3
"""Train the course-aligned HOG + colour baseline."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.argv[1:1] = [
    "--config", str(ROOT / "configs/hog.yaml"),
    "--output", str(ROOT / "outputs/models/hog_logreg.joblib"),
]

from train import main  # noqa: E402


if __name__ == "__main__":
    main()
