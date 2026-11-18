"""Data loading, chart styling and small layout helpers shared by every page."""
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "mxmh_survey_results.csv"
SOURCE_URL = "https://www.kaggle.com/datasets/catherinerasgaitis/mxmh-survey-results"

AUTHOR = "Simon Sealey"
EMAIL = "simon.sealey.ss@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/simon-sealey-008317199"  # TODO: your LinkedIn URL

# Palette: ink and mist for the interface, Okabe-Ito for data (color-blind safe).
INK = "#1B2230"
MUTED = "#5B6472"
RULE = "#DCE0E6"
MIST = "#F2F4F7"
COBALT = "#0B5CAD"

CONDITIONS = ["Anxiety", "Depression", "Insomnia", "OCD"]
CONDITION_COLORS = {"Anxiety": "#E69F00", "Depression": "#0072B2", "Insomnia": "#009E73", "OCD": "#CC79A7"}
CONDITION_SYMBOLS = {"Anxiety": "circle", "Depression": "diamond", "Insomnia": "square", "OCD": "triangle-up"}
EFFECT_ORDER = ["Improve", "No effect", "Worsen"]
EFFECT_COLORS = {"Improve": "#0072B2", "No effect": "#A7ADB8", "Worsen": "#D55E00", "No answer": INK}
FREQ_LEVELS = ["Never", "Rarely", "Sometimes", "Very frequently"]
AGE_BINS = [0, 17, 24, 34, 49, 120]
AGE_LABELS = ["10–17", "18–24", "25–34", "35–49", "50+"]

ETHICS_NOTE = (
    "This dataset includes real people, so results must be interpreted carefully. The responses come "
    "from a voluntary online survey shared on Reddit, Discord, social media and flyers in 2022, so they "
    "over-represent young, music-engaged respondents, and every mental health score is a self-rating, "
    "not a clinical diagnosis. The charts show patterns, not causes, and shouldn't be used to judge "
    "individuals or the people who listen to any genre."
)

BODY_FONT = "Atkinson Hyperlegible, sans-serif"
HEAD_FONT = "Bricolage Grotesque, sans-serif"

pio.templates["mxmh"] = go.layout.Template(
    layout=dict(
        font=dict(family=BODY_FONT, size=14, color=INK),
        title=dict(font=dict(family=HEAD_FONT, size=18, color=INK), x=0, xanchor="left", pad=dict(b=8)),
        paper_bgcolor="white",
        plot_bgcolor="white",
        colorway=list(CONDITION_COLORS.values()),
        xaxis=dict(showgrid=False, linecolor=RULE, ticks="outside", tickcolor=RULE,
                   title=dict(font=dict(size=13, color=MUTED)), tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor="#EDF0F3", zeroline=False, showline=False,
                   title=dict(font=dict(size=13, color=MUTED)), tickfont=dict(color=MUTED)),
        legend=dict(title=dict(font=dict(size=12, color=MUTED)), font=dict(size=13)),
        hoverlabel=dict(bgcolor=INK, bordercolor=INK, font=dict(family=BODY_FONT, color="white", size=13)),
        margin=dict(l=8, r=8, t=56, b=8),
    )
)
pio.templates.default = "plotly_white+mxmh"
CHART_CONFIG = {"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"]}

CSS = f"""
<style>
.block-container {{ max-width: 1180px; padding-top: 2.5rem; }}
h1 {{ letter-spacing: -0.03em; line-height: 1.02 !important; }}
h2, h3 {{ letter-spacing: -0.015em; }}
.lede {{ font-size: 1.2rem; line-height: 1.6; color: {MUTED}; max-width: 62ch; margin: 0.4rem 0 1.4rem; }}
[data-testid="stMarkdownContainer"] > p, [data-testid="stMarkdownContainer"] > ul,
[data-testid="stMarkdownContainer"] > ol {{ max-width: 80ch; }}
.aside {{ border-left: 3px solid {COBALT}; background: {MIST}; padding: 0.9rem 1.1rem;
          border-radius: 0 6px 6px 0; max-width: 78ch; line-height: 1.55; }}
.aside strong {{ color: {INK}; }}
.note-head {{ font-family: {HEAD_FONT}; font-weight: 700; font-size: 1.02rem; margin: 0.2rem 0 0.35rem; }}
.chart-meta {{ color: {MUTED}; font-size: 0.86rem; margin-top: -0.6rem; }}
[data-testid="stMetricValue"] {{ font-family: {HEAD_FONT}; font-weight: 700; letter-spacing: -0.02em; }}
[data-testid="stMetricLabel"] p {{ color: {MUTED}; }}
[data-testid="stSidebarNav"] a span {{ font-size: 0.98rem; }}
</style>
"""


def apply_style() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the survey and apply the cleaning steps documented in the README."""
    df = pd.read_csv(DATA_PATH).drop(columns=["Permissions"])  # identical consent text in every row
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%m/%d/%Y %H:%M:%S")
    # Self-reported BPM includes impossible values (0, 999,999,999); treat them as missing.
    df.loc[(df["BPM"] < 40) | (df["BPM"] > 250), "BPM"] = np.nan
    df["Primary streaming service"] = (
        df["Primary streaming service"]
        .replace({"I do not use a streaming service.": "No streaming service"})
        .fillna("Not reported")
    )
    df["Age group"] = pd.cut(df["Age"], bins=AGE_BINS, labels=AGE_LABELS)
    for col in genre_columns(df):
        df[col] = pd.Categorical(df[col], categories=FREQ_LEVELS, ordered=True)
    return df


def genre_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c.startswith("Frequency [")]


def genre_names(df: pd.DataFrame) -> list[str]:
    return [c.removeprefix("Frequency [").removesuffix("]") for c in genre_columns(df)]


def data_file_updated() -> str:
    return datetime.fromtimestamp(DATA_PATH.stat().st_mtime).strftime("%b %d, %Y at %I:%M %p")


def sidebar_profile() -> None:
    with st.sidebar:
        st.markdown(f"**{AUTHOR}**")
        st.caption("Data Science & ML, MSU Denver  \nLead BHT & Project Analyst")
        st.markdown(f"[Email](mailto:{EMAIL}) &nbsp;&nbsp; [LinkedIn]({LINKEDIN})")


def lede(text: str) -> None:
    st.markdown(f'<p class="lede">{text}</p>', unsafe_allow_html=True)


def aside(html: str) -> None:
    st.markdown(f'<div class="aside">{html}</div>', unsafe_allow_html=True)


def chart_notes(how_to_read: list[str], observations: list[str]) -> None:
    """The reading guide and observations that sit beside every gallery chart."""
    st.markdown('<p class="note-head">How to read this chart</p>', unsafe_allow_html=True)
    st.markdown("\n".join(f"- {b}" for b in how_to_read))
    st.markdown('<p class="note-head">What stands out</p>', unsafe_allow_html=True)
    st.markdown("\n".join(f"- {b}" for b in observations))


def source_line(extra: str = "") -> None:
    st.markdown(
        f'<p class="chart-meta">Source: MxMH survey (Rasgaitis, 2022) on '
        f'<a href="{SOURCE_URL}">Kaggle</a>, n = 736. {extra}</p>',
        unsafe_allow_html=True,
    )
