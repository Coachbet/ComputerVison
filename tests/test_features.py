import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from emoji_provider.features import extract_features, feature_names  # noqa: E402


def _emoji(tmp_path: Path) -> Path:
    path = tmp_path / "emoji.png"
    image = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    for x in range(10, 30):
        for y in range(10, 30):
            image.putpixel((x, y), (255, 0, 0, 255))
    image.save(path)
    return path


def test_feature_vector_shape_and_names(tmp_path: Path) -> None:
    features = extract_features(_emoji(tmp_path), bins=8, size=16)
    assert features.shape == (15 + 15 + 6 * 8,)
    assert len(feature_names(bins=8)) == features.shape[0]
    assert np.isfinite(features).all()


def test_default_vector_has_222_features(tmp_path: Path) -> None:
    assert extract_features(_emoji(tmp_path)).shape == (222,)


def test_transparency_and_bbox(tmp_path: Path) -> None:
    features = extract_features(_emoji(tmp_path), bins=8, size=16)
    names = feature_names(bins=8)
    assert np.isclose(features[names.index("A_part_pixels_visibles")], 0.25)
    assert np.isclose(features[names.index("A_bbox_largeur")], 0.5)
