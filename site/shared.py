from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]


def configure_page(title: str, icon: str = "🔬") -> None:
    st.set_page_config(page_title=f"{title} | EmojiVision", page_icon=icon, layout="wide")
    st.markdown(
        """
        <style>
        .block-container {max-width: 1200px; padding-top: 2rem;}
        [data-testid="stMetric"] {background: #f5f7fb; border: 1px solid #e5e9f2;
                                  padding: 1rem; border-radius: .8rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_results() -> pd.DataFrame:
    path = ROOT / "experiments/results.csv"
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def page_header(title: str, description: str) -> None:
    st.title(title)
    st.caption(description)
