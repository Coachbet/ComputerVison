import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import yaml
from PIL import Image
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
idx = np.arange(len(y))
x_tr, x_val, y_tr, y_val, i_tr, i_val = train_test_split(
    x, y, idx, test_size=0.2, random_state=42, stratify=y)

model = build_model(config, 42).fit(x_tr, y_tr)
pred = model.predict(x_val)
proba = model.predict_proba(x_val).max(axis=1)
wrong = np.where(pred != y_val)[0]

# Apple <-> Google errors first, then the most confident other mistakes
ag = [k for k in wrong if {y_val[k], pred[k]} == {"apple", "google"}]
others = sorted([k for k in wrong if k not in ag], key=lambda k: -proba[k])
chosen = (ag[:2] + others)[:4]

fig, axes = plt.subplots(1, 4, figsize=(10, 3))
for ax, k in zip(axes, chosen):
    path = table["path"].iloc[i_val[k]]
    img = Image.open(path).convert("RGBA")
    ax.imshow(img)
    ax.set_facecolor("#eeeeee")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"true: {y_val[k]}\npred: {pred[k]} ({proba[k]:.0%})", fontsize=10)
    with Image.open(path) as raw:
        w, h = raw.size
        mode = raw.mode
    print(f"{Path(path).name}: true={y_val[k]}, pred={pred[k]}, conf={proba[k]:.2f}, "
          f"size={w}x{h}, mode={mode}, {Path(path).stat().st_size / 1024:.1f} KB")

plt.tight_layout()
(ROOT / "outputs").mkdir(exist_ok=True)
plt.savefig(ROOT / "outputs/misclassified.png", dpi=200)
print("Saved outputs/misclassified.png")
