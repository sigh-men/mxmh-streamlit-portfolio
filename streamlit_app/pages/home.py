"""Overview: the respondent waveform, three headline findings and where to go next."""
import plotly.graph_objects as go
import streamlit as st

from utils import CHART_CONFIG, ETHICS_NOTE, INK, MUTED, aside, lede, load_data, source_line

df = load_data()

st.title("What 736 listeners say about music and their mental health")
lede(
    "In 2022, 736 people told a researcher how they listen to music and rated their own anxiety, "
    "depression, insomnia and OCD from 0 to 10. I work in residential addiction treatment, where "
    "music shows up in almost every coping plan, so I wanted to see what this survey can and "
    "can't say about that."
)

# One bar per respondent, mirrored around zero like an audio waveform. Sorted by anxiety so the
# color sweeps from low to high; shuffled within each anxiety level so heights vary like real audio.
wave = df.sample(frac=1, random_state=7).sort_values("Anxiety", kind="stable").reset_index(drop=True)
height = wave["Hours per day"].clip(upper=12).clip(lower=0.35)
fig = go.Figure(
    go.Bar(
        x=wave.index, y=height, base=-height / 2,
        marker=dict(
            color=wave["Anxiety"], cmin=0, cmax=10, line_width=0,
            colorscale=[[0, "#D7E3F1"], [0.5, "#5B8FC9"], [1, "#0B2E5E"]],
            colorbar=dict(title=dict(text="Anxiety (0–10)", font=dict(size=12, color=MUTED)),
                          thickness=10, len=0.9, tickfont=dict(size=11, color=MUTED), outlinewidth=0),
        ),
        customdata=wave[["Age", "Fav genre", "Hours per day", "Anxiety"]],
        hovertemplate=("Age %{customdata[0]:.0f}, favorite genre %{customdata[1]}<br>"
                       "%{customdata[2]} hrs/day, anxiety %{customdata[3]:.0f}/10<extra></extra>"),
    )
)
fig.update_layout(
    height=250, bargap=0.12, margin=dict(l=0, r=0, t=4, b=4), showlegend=False,
    xaxis=dict(visible=False), yaxis=dict(visible=False, range=[-6.4, 6.4]),
)
st.plotly_chart(fig, width="stretch", config={**CHART_CONFIG, "displayModeBar": False})
st.caption(
    "Each bar is one respondent, sorted from lowest to highest self-rated anxiety. Darker bars mean "
    "higher anxiety; taller bars mean more listening per day (capped at 12 hours so the 24-hour "
    "outliers don't flatten everyone else). Hover a bar to see that person's answers."
)

st.subheader("Three things the survey shows")
improve = (df["Music effects"] == "Improve").mean() / df["Music effects"].notna().mean()
c1, c2, c3 = st.columns(3, gap="large")
c1.markdown(
    f"**{improve:.0%} say music improves their mental health.** Only 17 people said it makes "
    "things worse. That's a belief people report, not a measured outcome."
)
c2.markdown(
    "**Anxiety and depression travel together** (r = 0.52), more than any other pair of "
    "conditions. Comparing groups on one condition at a time misses that overlap."
)
c3.markdown(
    "**How much people listen barely tracks their symptoms.** Hours per day correlates with "
    "every condition at r = 0.14 or less."
)

st.subheader("Explore the project")
links = st.columns(4, gap="medium")
links[0].page_link("pages/bio.py", label="About me", icon=":material/person:")
links[0].caption("Background, tools and how I approach visualization.")
links[1].page_link("pages/gallery.py", label="EDA gallery", icon=":material/bar_chart:")
links[1].caption("Five charts, each with a reading guide and observations.")
links[2].page_link("pages/dashboard.py", label="Dashboard", icon=":material/tune:")
links[2].caption("Filter by age, genre and streaming service.")
links[3].page_link("pages/future_work.py", label="Future work", icon=":material/arrow_forward:")
links[3].caption("What I'd build next and what changed from the prototype.")

st.write("")
aside(f"<strong>About this data.</strong> {ETHICS_NOTE}")
source_line()
