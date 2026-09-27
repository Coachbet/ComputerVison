import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import streamlit as st
from shared import ROOT, configure_page, page_header

configure_page("Transparence IA", "🤖")
page_header("🤖 Transparence IA", "Journal des demandes, résultats et vérifications humaines")
st.markdown((ROOT / "docs/AI_USAGE.md").read_text())
