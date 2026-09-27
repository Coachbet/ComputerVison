import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from shared import ROOT, configure_page, load_results, page_header

configure_page("Accueil", "🎨")
page_header("🎨 EmojiVision", "Classifier le fournisseur d’un emoji à partir de son style visuel")

labels_path = ROOT / "data/train_labels.csv"
results = load_results()
labels = pd.read_csv(labels_path) if labels_path.exists() else pd.DataFrame()

cols = st.columns(4)
cols[0].metric("Images train", f"{len(labels):,}".replace(",", " ") if not labels.empty else "—")
cols[1].metric("Fournisseurs", labels["Label"].nunique() if not labels.empty else "—")
cols[2].metric("Expériences", len(results))
if not results.empty:
    scores = pd.to_numeric(results["validation_macro_f1"], errors="coerce")
    cols[3].metric("Meilleure macro-F1", f"{scores.max():.3f}")
else:
    cols[3].metric("Meilleure macro-F1", "—")

st.header("Le problème")
st.write(
    "Apple, Google, Samsung et les autres fournisseurs dessinent le même emoji avec "
    "des palettes, contours, ombres, proportions et formats différents. Le projet compare "
    "des features manuelles, un CNN et un modèle de style enrichi afin de prédire la source."
)

left, right = st.columns([1.1, 1])
with left:
    st.subheader("Meilleur résultat local")
    if not results.empty:
        best_idx = pd.to_numeric(results["validation_macro_f1"], errors="coerce").idxmax()
        best = results.loc[best_idx]
        st.success(f"{best['experiment']} — macro-F1 {float(best['validation_macro_f1']):.3f}")
        st.write(best.get("notes", ""))
    st.info("Un modèle plus complexe n’est retenu que s’il améliore la validation.")
with right:
    st.subheader("Répartition des classes")
    if not labels.empty:
        st.bar_chart(labels["Label"].value_counts())

st.header("Navigation")
st.write(
    "Utilise le menu latéral pour consulter les notions du cours, comparer les expériences, "
    "tester une image avec les modèles entraînés et vérifier le journal de transparence IA."
)
