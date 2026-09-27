import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import streamlit as st
from shared import ROOT, configure_page, load_results, page_header

configure_page("Expériences", "🧪")
page_header("🧪 Expériences", "Comparer les hypothèses, scores locaux et scores Kaggle")

results = load_results()
if results.empty:
    st.info("Aucun résultat enregistré.")
else:
    display = results.copy()
    metrics = ["validation_accuracy", "validation_macro_f1", "kaggle_score"]
    for col in metrics:
        display[col] = pd.to_numeric(display[col], errors="coerce")
    st.dataframe(display, use_container_width=True, hide_index=True)
    chart = display.set_index("experiment")[metrics].dropna(how="all")
    st.bar_chart(chart)
    best_idx = display["validation_macro_f1"].idxmax()
    st.success(
        f"Meilleur modèle local : {display.loc[best_idx, 'experiment']} "
        f"(macro-F1 {display.loc[best_idx, 'validation_macro_f1']:.3f})"
    )

st.markdown((ROOT / "docs/METHODOLOGY.md").read_text())

st.subheader("Analyse détaillée du meilleur modèle")
reports = sorted((ROOT / "outputs/metrics").glob("*_classification_report.csv"))
matrices = sorted((ROOT / "outputs/metrics").glob("*_confusion_matrix.csv"))
if reports:
    report_path = st.selectbox("Rapport par classe", reports, format_func=lambda p: p.stem)
    st.dataframe(pd.read_csv(report_path, index_col=0), use_container_width=True)
if matrices:
    matrix_path = st.selectbox("Matrice de confusion", matrices, format_func=lambda p: p.stem)
    st.dataframe(pd.read_csv(matrix_path, index_col=0), use_container_width=True)

st.subheader("Soumissions disponibles")
submissions = sorted((ROOT / "outputs/submissions").glob("*.csv"))
if not submissions:
    st.info("Aucune soumission générée.")
for path in submissions:
    st.download_button(
        f"Télécharger {path.name}", path.read_bytes(), file_name=path.name, mime="text/csv",
        key=str(path),
    )
