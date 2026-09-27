import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import joblib
import pandas as pd
import streamlit as st
from shared import ROOT, configure_page, page_header

sys.path.insert(0, str(ROOT / "src"))
from emoji_provider.features import extract_many

configure_page("Prédiction", "🔮")
page_header("🔮 Prédiction interactive", "Déposer un PNG et comparer les modèles entraînés")

models = {
    "Style + métadonnées + boosting (recommandé)": ROOT / "outputs/models/style_boosting.joblib",
    "Style + métadonnées + Extra Trees": ROOT / "outputs/models/style_extra_trees.joblib",
    "HOG + couleurs": ROOT / "outputs/models/hog_logreg.joblib",
    "CNN LeNet": ROOT / "outputs/models/lenet_cnn.keras",
    "MobileNetV3 transfer learning": ROOT / "outputs/models/mobilenet_v3.keras",
}
available = {name: path for name, path in models.items() if path.exists()}
if not available:
    st.warning("Entraîne d’abord un modèle.")
    st.stop()

choice = st.selectbox("Modèle", list(available))
uploaded = st.file_uploader("Image d’emoji", type=["png"])
if uploaded:
    st.image(uploaded, width=180)
    suffix = ".png"
    with tempfile.NamedTemporaryFile(suffix=suffix) as temp:
        temp.write(uploaded.getvalue())
        temp.flush()
        path = Path(temp.name)
        if available[choice].suffix == ".keras":
            import numpy as np
            import tensorflow as tf
            from tensorflow import keras
            from emoji_provider.cnn import decode_image

            metadata = json.loads(available[choice].with_suffix(".json").read_text())
            image, _ = decode_image(tf.constant(str(path)), tf.constant(0), metadata["config"]["image_size"])
            probabilities = keras.models.load_model(available[choice]).predict(image[None], verbose=0)[0]
            labels = metadata["classes"]
        else:
            artifact = joblib.load(available[choice])
            config = artifact["config"]
            features = extract_many(
                [path], config["histogram_bins"], config["image_size"],
                config.get("feature_method", "color"),
            )
            model = artifact["model"]
            labels = model.classes_.tolist()
            probabilities = model.predict_proba(features)[0]

    result = pd.Series(probabilities, index=labels).sort_values(ascending=False)
    st.success(f"Prédiction : **{result.index[0]}** — confiance {result.iloc[0]:.1%}")
    st.bar_chart(result)
    st.caption("La confiance est une probabilité du modèle, pas une garantie de justesse.")
