"""About me: professional summary, highlights and visualization philosophy."""
import base64

import streamlit as st

from utils import EMAIL, LINKEDIN, ROOT, lede

st.title("About me")
lede("I work where behavioral health meets data: half my week is with clients, the other half is in their outcomes data.")

# st.image has no alt-text option, so the image is embedded as HTML with an alt attribute.
banner = base64.b64encode((ROOT / "assets" / "banner.png").read_bytes()).decode()
st.markdown(
    f'<img src="data:image/png;base64,{banner}" style="width:100%;border-radius:6px" '
    'alt="Waveform made of 736 thin vertical bars, one per survey respondent, shading from '
    'light blue to dark navy as self-rated anxiety rises.">',
    unsafe_allow_html=True,
)
st.caption("The 736 MxMH respondents as a waveform: one bar per person, darker for higher self-rated anxiety, taller for more daily listening. The same chart opens the Overview page.")

left, right = st.columns([3, 2], gap="large")

with left:
    st.subheader("Summary")
    st.markdown(
        "I'm the Lead Behavioral Health Technician and Project Analyst at Sobriety House, a "
        "residential substance use treatment program in Denver. I facilitate groups and supervise "
        "a team of technicians, and I manage our outcomes platforms (Trac9 and ReliaTrax) and write "
        "the monthly clinical outcomes report leadership uses to make decisions. I'm finishing a "
        "B.S. in Data Science & Machine Learning with a minor in Social Work at MSU Denver this "
        "December. I want to build analysis that clinicians trust enough to act on."
    )

    st.subheader("How I approach visualization")
    st.markdown(
        "Most of the data I work with is about people on some of their hardest days, and that "
        "shapes how I chart it.\n\n"
        "- **One question per chart.** The title says what the chart shows, and every axis has units.\n"
        "- **Readable by everyone.** Color-blind-safe palettes, shape as a second cue, alt text, and "
        "a typeface built for low-vision readers (Atkinson Hyperlegible, used throughout this app).\n"
        "- **Honest about limits.** Fixed scales so small differences don't look dramatic, group "
        "sizes on the chart, and no language that turns a correlation into a cause or a group "
        "average into a verdict on a person."
    )

with right:
    st.subheader("Highlights")
    st.markdown(
        "- B.S. Data Science & Machine Learning, minor in Social Work, MSU Denver (December 2026)\n"
        "- Monthly clinical outcomes reporting for a multi-campus residential treatment program\n"
        "- Lead BHT supervising a team of technicians and facilitating groups\n"
        "- Senior capstone in biomedical text mining (mapping metadata to ontologies)\n"
        "- Python, pandas, Plotly and Streamlit (this app), plus Trac9 and ReliaTrax"
    )
    st.subheader("Contact")
    st.markdown(f"[{EMAIL}](mailto:{EMAIL})  \n[LinkedIn]({LINKEDIN})")
