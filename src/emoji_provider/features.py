from pathlib import Path

import numpy as np
from PIL import Image
from skimage.feature import hog


def load_rgb(path: Path, size: int) -> Image.Image:
    """Load an image on a white background while preserving visible transparency."""
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        rgb = Image.alpha_composite(background, rgba).convert("RGB")
        return rgb.resize((size, size), Image.Resampling.LANCZOS)


def extract_color_histogram(path: Path, bins: int = 32, size: int = 96) -> np.ndarray:
    """Extract normalized RGB and HSV histograms from one heterogeneous image."""
    rgb = load_rgb(path, size)
    hsv = rgb.convert("HSV")

    features: list[np.ndarray] = []
    for array in (np.asarray(rgb), np.asarray(hsv)):
        for channel in range(3):
            hist, _ = np.histogram(array[..., channel], bins=bins, range=(0, 256))
            hist = hist.astype(np.float32)
            features.append(hist / max(hist.sum(), 1.0))
    return np.concatenate(features)


def extract_hog_color(path: Path, bins: int = 32, size: int = 64) -> np.ndarray:
    """Combine edge/orientation information (HOG) with global colour statistics."""
    rgb = np.asarray(load_rgb(path, size))
    gray = np.asarray(Image.fromarray(rgb).convert("L"))
    gradients = hog(
        gray,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm="L2-Hys",
        feature_vector=True,
    ).astype(np.float32)
    return np.concatenate([gradients, extract_color_histogram(path, bins=bins, size=size)])


def extract_style_features(path: Path, bins: int = 32, size: int = 96) -> np.ndarray:
    """Describe provider rendering style, transparency and native file properties."""
    with Image.open(path) as image:
        width, height = image.size
        original_mode = image.mode
        rgba = np.asarray(image.convert("RGBA"), dtype=np.uint8)

    alpha = rgba[..., 3].astype(np.float32) / 255.0
    visible = alpha > 0.05
    if visible.any():
        ys, xs = np.where(visible)
        bbox_width = (xs.max() - xs.min() + 1) / max(width, 1)
        bbox_height = (ys.max() - ys.min() + 1) / max(height, 1)
        visible_rgb = rgba[..., :3][visible].astype(np.float32) / 255.0
    else:
        bbox_width = bbox_height = 0.0
        visible_rgb = np.zeros((1, 3), dtype=np.float32)

    modes = ["RGBA", "RGB", "P", "LA", "L"]
    mode_features = [float(original_mode == mode) for mode in modes]
    channel_stats = np.concatenate([
        visible_rgb.mean(axis=0),
        visible_rgb.std(axis=0),
        np.quantile(visible_rgb, [0.10, 0.50, 0.90], axis=0).ravel(),
    ])
    metadata = np.asarray([
        np.log1p(width), np.log1p(height), width / max(height, 1),
        np.log1p(path.stat().st_size), alpha.mean(), alpha.std(),
        visible.mean(), bbox_width, bbox_height, bbox_width * bbox_height,
        *mode_features,
    ], dtype=np.float32)
    color = extract_color_histogram(path, bins=bins, size=size)
    return np.concatenate([metadata, channel_stats.astype(np.float32), color])


def extract_many(
    paths: list[Path], bins: int = 32, size: int = 96, method: str = "color"
) -> np.ndarray:
    extractors = {
        "color": extract_color_histogram,
        "hog_color": extract_hog_color,
        "style": extract_style_features,
    }
    if method not in extractors:
        raise ValueError(f"Unknown feature method: {method}")
    extractor = extractors[method]
    return np.vstack([extractor(path, bins=bins, size=size) for path in paths])
