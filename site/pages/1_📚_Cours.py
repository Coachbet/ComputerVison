import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st
from shared import ROOT, configure_page, page_header

configure_page("Cours", "📚")
page_header(
    "📚 Comprendre le projet",
    "Un vrai parcours progressif, des pixels jusqu’à l’ensemble final",
)

COURSES = [
    ("1. Images, pixels et transparence", "01_images.md", "https://www.youtube.com/watch?v=Ilg3g-GewQ5"),
    ("2. Histogrammes et HOG", "02_features.md", None),
    ("3. Régression logistique et validation", "03_logistic.md", "https://www.youtube.com/watch?v=IHZwWFHWa-w"),
    ("4. Arbres et gradient boosting", "04_boosting.md", "https://www.youtube.com/watch?v=jxuNLH5dXCs"),
    ("5. CNN, convolution et LeNet", "05_cnn.md", "https://www.youtube.com/watch?v=HGwBXDKFk9I"),
    ("6. Transfer learning et MobileNetV3", "06_transfer.md", None),
    ("7. Ensemble et soumission finale", "07_ensemble.md", None),
]

st.info(
    "Ordre conseillé : lire les chapitres 1 → 7. Chaque chapitre relie la théorie, "
    "une analogie, notre implémentation et une question à laquelle vous devez savoir répondre."
)

selected = st.selectbox(
    "Choisir un chapitre",
    range(len(COURSES)),
    format_func=lambda index: COURSES[index][0],
)
title, filename, video = COURSES[selected]
st.progress((selected + 1) / len(COURSES), text=f"Chapitre {selected + 1} sur {len(COURSES)}")

course_path = ROOT / "site" / "content" / "courses" / filename
st.markdown(course_path.read_text(encoding="utf-8"))

if video:
    st.subheader("🎬 Vidéo recommandée")
    st.video(video)
else:
    st.caption("Les ressources officielles et vidéos utiles sont indiquées dans le chapitre.")

st.divider()
with st.expander("Supports PDF donnés en classe"):
    for name in ["CM-CV1-min.pdf", "CM-CV2.pdf", "CM-CV3.pdf"]:
        path = ROOT / "lessson" / name
        if path.exists():
            st.download_button(
                f"Télécharger {name}",
                path.read_bytes(),
                file_name=name,
                mime="application/pdf",
            )
