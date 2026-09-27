from pathlib import Path

import pandas as pd

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def list_images(folder: Path) -> list[Path]:
    """Return image paths in deterministic order."""
    if not folder.is_dir():
        raise FileNotFoundError(f"Image directory not found: {folder}")
    paths = sorted(
        path for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not paths:
        raise ValueError(f"No supported image found in: {folder}")
    return paths


def image_id(path: Path) -> str:
    return path.stem


def load_training_table(data_dir: Path) -> pd.DataFrame:
    """Match train images to labels by Id, never by accidental row order."""
    labels_path = data_dir / "train_labels.csv"
    if not labels_path.is_file():
        raise FileNotFoundError(f"Labels file not found: {labels_path}")
    labels = pd.read_csv(labels_path, dtype={"Id": str})
    if not {"Id", "Label"}.issubset(labels.columns):
        raise ValueError(f"{labels_path} must contain columns: Id, Label")
    if labels["Id"].duplicated().any():
        raise ValueError("Duplicate Id values found in train_labels.csv")

    images = pd.DataFrame({"path": list_images(data_dir / "train")})
    images["Id"] = images["path"].map(image_id)
    table = images.merge(labels[["Id", "Label"]], on="Id", how="left", validate="one_to_one")
    if table["Label"].isna().any():
        missing = table.loc[table["Label"].isna(), "Id"].head().tolist()
        raise ValueError(f"Missing labels for image Id(s): {missing}")
    return table
