"""Étape 1 du modèle : transformer une image en 222 nombres (« features »)."""
from pathlib import Path

import numpy as np
from PIL import Image

MODES = ["RGBA", "RGB", "P", "LA", "L"]


def load_rgb(path: Path, size: int) -> Image.Image:
    """Charge l'image sur fond blanc (la transparence est conservée visuellement)."""
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        background = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        rgb = Image.alpha_composite(background, rgba).convert("RGB")
        return rgb.resize((size, size), Image.Resampling.LANCZOS)


def extract_color_histogram(path: Path, bins: int = 32, size: int = 96) -> np.ndarray:
    """Bloc C : 6 histogrammes normalisés (R, G, B, H, S, V) -> 6 x bins valeurs."""
    rgb = load_rgb(path, size)
    hsv = rgb.convert("HSV")
    features: list[np.ndarray] = []
    for array in (np.asarray(rgb), np.asarray(hsv)):
        for channel in range(3):
            hist, _ = np.histogram(array[..., channel], bins=bins, range=(0, 256))
            hist = hist.astype(np.float32)
            features.append(hist / max(hist.sum(), 1.0))
    return np.concatenate(features)


def extract_features(path: Path, bins: int = 32, size: int = 96) -> np.ndarray:
    """Vecteur complet : A (métadonnées) + B (statistiques de couleur) + C (histogrammes)."""
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

    # Bloc A : 15 métadonnées (taille, fichier, transparence, boîte englobante, mode)
    metadata = np.asarray([
        np.log1p(width), np.log1p(height), width / max(height, 1),
        np.log1p(path.stat().st_size), alpha.mean(), alpha.std(),
        visible.mean(), bbox_width, bbox_height, bbox_width * bbox_height,
        *[float(original_mode == mode) for mode in MODES],
    ], dtype=np.float32)

    # Bloc B : 15 statistiques de couleur sur les pixels visibles
    channel_stats = np.concatenate([
        visible_rgb.mean(axis=0),
        visible_rgb.std(axis=0),
        np.quantile(visible_rgb, [0.10, 0.50, 0.90], axis=0).ravel(),
    ]).astype(np.float32)

    return np.concatenate([metadata, channel_stats, extract_color_histogram(path, bins, size)])


def extract_many(paths: list[Path], bins: int = 32, size: int = 96) -> np.ndarray:
    return np.vstack([extract_features(path, bins=bins, size=size) for path in paths])


def feature_names(bins: int = 32) -> list[str]:
    """Nom de chaque colonne, préfixé par son bloc : A_, B_ ou C_."""
    meta = ["log_largeur", "log_hauteur", "ratio_l_h", "log_taille_fichier", "alpha_moyen",
            "alpha_ecart_type", "part_pixels_visibles", "bbox_largeur", "bbox_hauteur",
            "bbox_aire"] + [f"mode_{mode}" for mode in MODES]
    stats = [f"{stat}_{c}" for stat in ("moyenne", "ecart_type", "q10", "q50", "q90") for c in "RGB"]
    hist = [f"{space}{channel}_bin{i}" for space, chans in (("rgb", "RGB"), ("hsv", "HSV"))
            for channel in chans for i in range(bins)]
    return [f"A_{n}" for n in meta] + [f"B_{n}" for n in stats] + [f"C_{n}" for n in hist]
