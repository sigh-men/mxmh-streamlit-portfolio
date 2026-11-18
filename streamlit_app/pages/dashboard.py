"""Dashboard: sidebar filters drive the KPIs and all three charts."""
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import (
    CHART_CONFIG, CONDITION_COLORS, CONDITIONS, EFFECT_COLORS, EFFECT_ORDER, INK, SOURCE_URL,
    data_file_updated, load_data,
)

df = load_data()
start, end = df["Timestamp"].min(), df["Timestamp"].max()

st.title("Dashboard")
st.markdown(
    f"[:blue-badge[:material/database: Data: MxMH survey on Kaggle]]({SOURCE_URL}) &nbsp; "
    f"Last refreshed {data_file_updated()}. Responses collected "
    f"{start:%b} {start.day} to {end:%b} {end.day}, {end.year}."
)

with st.sidebar:
    st.divider()
    st.markdown("**Filters**")
    age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
    ages = st.slider("Age range (years)", age_min, age_max, (age_min, age_max))
    genres = st.multiselect("Favorite genre", df["Fav genre"].value_counts().index, placeholder="All genres")
    services = st.multiselect("Streaming service", df["Primary streaming service"].value_counts().index,
                              placeholder="All services")
    focus = st.selectbox("Condition to focus on", CONDITIONS)

mask = df["Age"].between(*ages)
if ages == (age_min, age_max):
    mask |= df["Age"].isna()  # keep the one respondent with no age until the range is narrowed
if genres:
    mask &= df["Fav genre"].isin(genres)
if services:
    mask &= df["Primary streaming service"].isin(services)
f = df[mask]

if f.empty:
    st.warning("No respondents match these filters. Widen the age range or remove a genre or service.")
    st.stop()

# ------------------------------------------------------------------ KPIs
answered = f["Music effects"].dropna()
diff = f[focus].mean() - df[focus].mean()
k1, k2, k3, k4 = st.columns(4)
k1.metric("Respondents", f"{len(f):,}", f"{len(f) / len(df):.0%} of the survey", delta_color="off", delta_arrow="off")
k2.metric("Median listening", f"{f['Hours per day'].median():.1f} hrs/day")
k3.metric(f"Average {focus.lower()}", f"{f[focus].mean():.1f} / 10",
          f"{diff:+.2f} vs everyone" if abs(diff) >= 0.005 else None, delta_color="inverse")
k4.metric("Say music helps", f"{(answered == 'Improve').mean():.0%}" if len(answered) else "No answers")
if len(f) < 30:
    st.caption(f":material/warning: Only {len(f)} people match. Averages this small can swing a lot.")

# ------------------------------------------------------------------ Linked charts
left, right = st.columns(2, gap="large")
with left:
    means, overall = f[CONDITIONS].mean(), df[CONDITIONS].mean()
    fig = go.Figure()
    fig.add_bar(x=CONDITIONS, y=means, name="This group", marker_color=[CONDITION_COLORS[c] for c in CONDITIONS],
                marker_line_width=0, text=[f"{v:.1f}" for v in means], textposition="outside",
                hovertemplate="%{x}: %{y:.2f}<extra>This group</extra>")
    fig.add_scatter(x=CONDITIONS, y=overall, mode="markers", name="All 736 respondents",
                    marker=dict(symbol="line-ew-open", size=46, color=INK, line=dict(width=2.5, color=INK)),
                    hovertemplate="%{x}: %{y:.2f}<extra>All respondents</extra>")
    fig.update_layout(title="Average self-ratings compared with everyone",
                      yaxis=dict(title="Average self-rating (0–10)", range=[0, 10], dtick=2), xaxis_title=None,
                      legend=dict(orientation="h", y=1.0, yanchor="bottom", x=1, xanchor="right"))
    st.plotly_chart(fig, width="stretch", config=CHART_CONFIG)
    st.caption("Bars show the filtered group; the dark line on each bar is the whole survey.")

with right:
    order = EFFECT_ORDER + ["No answer"]
    eff = f["Music effects"].fillna("No answer").value_counts().reindex(order).fillna(0).astype(int)
    eff = eff[eff > 0].rename_axis("Effect").reset_index(name="Respondents")
    fig = px.bar(eff, x="Respondents", y="Effect", orientation="h", text="Respondents", color="Effect",
                 color_discrete_map=EFFECT_COLORS, category_orders={"Effect": order},
                 title="What they say music does for their mental health")
    fig.update_traces(marker_line_width=0, hovertemplate="%{y}: %{x} people<extra></extra>")
    fig.update_layout(showlegend=False, yaxis_title=None, xaxis_title="Respondents")
    st.plotly_chart(fig, width="stretch", config=CHART_CONFIG)
    st.caption("Answers to: does listening to music improve or worsen your mental health?")

rng = np.random.default_rng(42)  # fixed jitter so whole-number answers don't stack on one point
jit = f.assign(
    _x=f["Hours per day"] + rng.uniform(-0.25, 0.25, len(f)),
    _y=f[focus] + rng.uniform(-0.25, 0.25, len(f)),
    Effect=f["Music effects"].fillna("No answer"),
)
fig = px.scatter(
    jit, x="_x", y="_y", color="Effect", symbol="Effect",
    color_discrete_map=EFFECT_COLORS, category_orders={"Effect": EFFECT_ORDER + ["No answer"]},
    symbol_map={"Improve": "circle", "No effect": "diamond", "Worsen": "x", "No answer": "square-open"},
    hover_data={"_x": False, "_y": False, "Hours per day": True, focus: True, "Age": True, "Fav genre": True},
    labels={"_x": "Listening time (hours per day)", "_y": f"Self-rated {focus.lower()} (0–10)", "Effect": "Effect of music"},
    title=f"Listening time vs. self-rated {focus.lower()}, one dot per person",
)
fig.update_traces(marker=dict(size=7, opacity=0.65))
fig.update_layout(yaxis=dict(range=[-0.6, 10.6], dtick=2),
                  legend=dict(orientation="h", y=1.0, yanchor="bottom", x=1, xanchor="right", title=None))
st.plotly_chart(fig, width="stretch", config=CHART_CONFIG)
st.caption("Dots are nudged slightly apart so overlapping answers stay visible. Hover for age and genre.")

# ------------------------------------------------------------------ Narrative
st.subheader("What you can take from this")
st.markdown(
    "- **Anxiety is the highest-rated condition** (5.8 of 10 across everyone), then depression (4.8), "
    "insomnia (3.7) and OCD (2.6). That order holds for most filter combinations.\n"
    "- **Listening time and symptoms are nearly unrelated.** The scatter shows high and low scores at "
    "every level of daily listening (r ≤ 0.14 for all four conditions).\n"
    "- **The 17 people who say music makes things worse report the highest averages**, especially for "
    "depression (7.2 vs 4.9 for those who say it helps).\n"
    "- **Respondents 50 and older report much lower anxiety and depression** (3.5 and 2.5 on average). "
    "Drag the age slider above 50 to compare.\n"
    "- **Limits:** this is a voluntary online survey that skews young (median age 21) and toward music "
    "fans. Scores are single self-ratings, not clinical measures, and several genres have under 20 fans. "
    "Treat these as associations in this sample, not causes."
)
