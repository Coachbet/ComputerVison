import sys
from pathlib import Path
import yaml
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from emoji_provider.data import load_training_table
from emoji_provider.features import extract_many
from emoji_provider.model import build_model

config = yaml.safe_load((ROOT / "configs/style_boosting.yaml").read_text())
table = load_training_table(ROOT / "data")
x = extract_many(table["path"].tolist(), config["histogram_bins"], config["image_size"])
y = table["Label"].astype(str).to_numpy()
x_tr, x_val, y_tr, y_val = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

for name, cols in [("All 222 features", slice(None)), ("Without Block A (207)", slice(15, None))]:
    model = build_model(config, 42).fit(x_tr[:, cols], y_tr)
    pred = model.predict(x_val[:, cols])
    print(f"{name}: accuracy {accuracy_score(y_val, pred):.3f}, macro-F1 {f1_score(y_val, pred, average='macro'):.3f}")