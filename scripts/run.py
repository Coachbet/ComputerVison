#!/usr/bin/env python3
"""Entraîne le modèle, le mesure, puis écrit la soumission Kaggle datée dans outputs/.

Un seul fichier est produit par lancement :
    outputs/submission_<date>_<heure>_acc<score>.csv   (colonnes Id,Label)
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import yaml
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from emoji_provider.data import image_id, list_images, load_training_table  # noqa: E402
from emoji_provider.features import extract_many  # noqa: E402
from emoji_provider.model import build_model  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--config", type=Path, default=ROOT / "configs/style_boosting.yaml")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs")
    args = parser.parse_args()

    config = yaml.safe_load(args.config.read_text())
    bins, size = config["histogram_bins"], config["image_size"]

    # 1. Images d'entraînement -> 222 mesures par image
    table = load_training_table(args.data_dir)
    x = extract_many(table["path"].tolist(), bins, size)
    y = table["Label"].astype(str).to_numpy()

    # 2. 80 % pour apprendre, 20 % pour mesurer (mêmes proportions de classes)
    x_train, x_val, y_train, y_val = train_test_split(
        x, y, test_size=config["validation_size"], random_state=config["seed"], stratify=y
    )
    model = build_model(config, config["seed"])
    model.fit(x_train, y_train)
    prediction = model.predict(x_val)
    accuracy = accuracy_score(y_val, prediction)
    print(classification_report(y_val, prediction, digits=3))
    print(f"Validation accuracy: {accuracy:.4f}")
    print(f"Validation macro F1: {f1_score(y_val, prediction, average='macro'):.4f}")

    # 3. Modèle final : réentraîné sur 100 % des images, puis prédiction du test
    model.fit(x, y)
    paths = list_images(args.data_dir / "test")
    submission = pd.DataFrame({
        "Id": [image_id(p) for p in paths],
        "Label": model.predict(extract_many(paths, bins, size)),
    })

    # 4. Un seul fichier de sortie, daté
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output = args.output_dir / f"submission_{stamp}_acc{accuracy:.3f}.csv"
    submission.to_csv(output, index=False)
    print(f"Saved {len(submission)} predictions to: {output}")


if __name__ == "__main__":
    main()
