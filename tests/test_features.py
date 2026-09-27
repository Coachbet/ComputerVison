from pathlib import Path
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from emoji_provider.features import extract_color_histogram, extract_hog_color


def test_feature_shape_and_normalization(tmp_path: Path) -> None:
    path = tmp_path / "rgba.png"
    Image.new("RGBA", (17, 29), (255, 20, 30, 128)).save(path)
    features = extract_color_histogram(path, bins=8, size=16)
    assert features.shape == (48,)
    assert np.isfinite(features).all()
    assert np.isclose(features.sum(), 6.0)


def test_hog_color_features_are_finite(tmp_path: Path) -> None:
    path = tmp_path / "emoji.png"
    image = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    for x in range(10, 30):
        for y in range(10, 30):
            image.putpixel((x, y), (255, 0, 0, 255))
    image.save(path)
    features = extract_hog_color(path, bins=8, size=32)
    assert features.shape[0] > 48
    assert np.isfinite(features).all()
