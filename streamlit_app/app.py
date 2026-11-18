"""Entry point: page config, shared styling and navigation."""
import streamlit as st

from utils import apply_style, sidebar_profile

st.set_page_config(page_title="Music & Mental Health | Simon Sealey", page_icon="🎧", layout="wide")
apply_style()

pages = [
    st.Page("pages/home.py", title="Overview", icon=":material/graphic_eq:", default=True),
    st.Page("pages/bio.py", title="About me", icon=":material/person:"),
    st.Page("pages/gallery.py", title="EDA gallery", icon=":material/bar_chart:"),
    st.Page("pages/dashboard.py", title="Dashboard", icon=":material/tune:"),
    st.Page("pages/future_work.py", title="Future work", icon=":material/arrow_forward:"),
]
nav = st.navigation(pages)
sidebar_profile()
nav.run()
