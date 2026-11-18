"""EDA gallery: five chart types, each paired with a reading guide and observations."""
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import (
    AGE_LABELS, CHART_CONFIG, CONDITION_COLORS, CONDITION_SYMBOLS, CONDITIONS, EFFECT_COLORS,
    EFFECT_ORDER, FREQ_LEVELS, INK, MUTED, chart_notes, genre_names, lede, load_data, source_line,
)

df = load_data()

st.title("EDA gallery")
lede(
    "Five questions, five chart types. Everything here describes a self-selected online survey, "
    "so read the patterns as associations within this group of respondents, not as evidence "
    "that music causes or treats anything."
)


def show(fig, extra: str = "") -> None:
    st.plotly_chart(fig, width="stretch", config=CHART_CONFIG)
    source_line(extra)


# ------------------------------------------------------------------ Histogram
st.divider()
st.header("How much do people listen each day?")
chart, notes = st.columns([3, 2], gap="large")
with chart:
    median = df["Hours per day"].median()
    fig = px.histogram(df, x="Hours per day", nbins=25, color_discrete_sequence=["#0072B2"],
                       title="Most people listen 1 to 5 hours a day")
    fig.update_traces(hovertemplate="%{x} hrs/day: %{y} people<extra></extra>", marker_line_width=0)
    fig.add_vline(x=median, line=dict(color=INK, dash="dot", width=1.5))
    fig.add_annotation(x=median, y=1, yref="paper", text=f"Median {median:.0f} hrs", showarrow=False,
                       xanchor="left", xshift=6, font=dict(color=INK, size=12))
    fig.add_annotation(x=24, y=3, text="3 people report<br>all 24 hours", showarrow=True, arrowhead=0,
                       ax=-10, ay=-60, arrowcolor=MUTED, font=dict(color=MUTED, size=12))
    fig.update_layout(xaxis_title="Listening time (hours per day)", yaxis_title="Respondents", bargap=0.06)
    show(fig)
with notes:
    chart_notes(
        [
            "Each bar is a range of daily listening hours; its height is how many people fall in it.",
            "The dotted line is the median: half listen less, half listen more.",
            "Drag across the chart to zoom into the long tail; double-click to reset.",
        ],
        [
            "The median is 3 hours, and 74% of people listen 4 hours or less.",
            "The tail is long: 40 people report 10+ hours, which mostly reads as background listening "
            "(79% say they listen while working).",
            "Only 6 people report zero hours, which fits a survey promoted to music fans.",
        ],
    )

# ------------------------------------------------------------------ Box plot
st.divider()
st.header("Do self-ratings differ by favorite genre?")
chart, notes = st.columns([3, 2], gap="large")
with chart:
    cond = st.segmented_control("Condition", CONDITIONS, default="Anxiety", key="box_cond") or "Anxiety"
    counts = df["Fav genre"].value_counts()
    keep = counts[counts >= 20].index
    sub = df[df["Fav genre"].isin(keep)]
    order = sub.groupby("Fav genre")[cond].median().sort_values().index.tolist()
    fig = px.box(sub, y="Fav genre", x=cond, orientation="h", category_orders={"Fav genre": order[::-1]},
                 points="outliers", color_discrete_sequence=[CONDITION_COLORS[cond]],
                 title=f"{cond} ratings overlap heavily across genres")
    fig.update_yaxes(tickvals=order, ticktext=[f"{g} ({counts[g]})" for g in order], title="Favorite genre (fans)")
    fig.update_layout(height=520, xaxis=dict(title=f"Self-rated {cond.lower()} (0–10)", range=[-0.5, 10.5], dtick=2,
                                             showgrid=True, gridcolor="#EDF0F3"), yaxis_showgrid=False)
    show(fig, extra="Genres with fewer than 20 fans (Lofi 10, Gospel 6, Latin 3) are left out.")
with notes:
    chart_notes(
        [
            "Each box holds the middle half of scores for one genre; the line inside is the median.",
            "Whiskers show the typical range and dots are unusual scores. The scale is fixed at 0–10.",
            "Genres are sorted with the highest median at the top; the number of fans is in brackets. "
            "Switch conditions above the chart.",
        ],
        [
            "Anxiety medians run from 4.5 (Rap) to 7.5 (Folk), but most genres sit between 6 and 7.",
            "Within every genre, people span nearly the whole 0–10 range.",
            "Hip hop fans have the highest median depression (7) of the larger genres; R&B fans one of the lowest (4).",
            "Rock has 188 fans, so its median is the most stable; smaller genres can move with a few answers.",
        ],
    )

# ------------------------------------------------------------------ Heatmap
st.divider()
st.header("Which measures move together?")
chart, notes = st.columns([3, 2], gap="large")
with chart:
    corr = df[CONDITIONS + ["Hours per day", "Age"]].corr().round(2)
    fig = px.imshow(corr, text_auto=True, zmin=-1, zmax=1, color_continuous_scale="PuOr", aspect="auto",
                    title="Anxiety and depression are the most closely linked")
    fig.update_traces(hovertemplate="%{y} and %{x}: r = %{z}<extra></extra>", textfont=dict(size=13))
    fig.update_coloraxes(colorbar=dict(title="r", thickness=10, outlinewidth=0))
    fig.update_xaxes(showline=False, ticks="")
    show(fig, extra="Pearson correlation; one missing age is skipped.")
with notes:
    chart_notes(
        [
            "Each square is the correlation (r) between two measures, from −1 to +1.",
            "Purple means both rise together, orange means one rises as the other falls, white is no link. "
            "The value is printed in every square, so you don't need the color.",
            "The diagonal is always 1, a measure compared with itself.",
        ],
        [
            "Anxiety and depression have the strongest link (r = 0.52).",
            "Insomnia sits closer to depression (0.38) than to anxiety (0.29).",
            "Listening hours barely relate to any condition (r ≤ 0.14).",
            "Older respondents rate anxiety slightly lower (r = −0.18), a weak pattern.",
        ],
    )

# ------------------------------------------------------------------ 100% stacked bar
st.divider()
st.header("Does the reported effect of music change with age?")
chart, notes = st.columns([3, 2], gap="large")
with chart:
    eff = df.dropna(subset=["Music effects", "Age group"])
    tab = eff.groupby(["Age group", "Music effects"], observed=True).size().reset_index(name="n")
    tab["share"] = tab["n"] / tab.groupby("Age group", observed=True)["n"].transform("sum")
    tab["label"] = [f"{v:.0%}" if v >= 0.06 else "" for v in tab["share"]]  # skip labels on thin slivers
    sizes = eff["Age group"].value_counts()
    fig = px.bar(tab, x="Age group", y="share", color="Music effects", custom_data=["n"], text="label",
                 category_orders={"Age group": AGE_LABELS, "Music effects": EFFECT_ORDER},
                 color_discrete_map=EFFECT_COLORS, title="The share who say music helps dips through middle age")
    fig.update_traces(hovertemplate="%{x}: %{y:.0%} (%{customdata[0]} people)<extra>%{fullData.name}</extra>",
                      textfont=dict(size=12), marker_line_width=0)
    fig.update_xaxes(tickvals=AGE_LABELS, ticktext=[f"{a}<br><span style='font-size:11px'>n={sizes[a]}</span>" for a in AGE_LABELS])
    fig.update_layout(xaxis_title="Age group (years)", yaxis=dict(title="Share of respondents", tickformat=".0%", range=[0, 1]),
                      legend=dict(title="Effect of music", orientation="h", y=-0.3, yanchor="top", x=0, xanchor="left"),
                      margin=dict(b=90))
    show(fig, extra="9 people with no age or no answer are left out.")
with notes:
    chart_notes(
        [
            "Each bar is one age group and adds to 100%, so groups of different sizes compare fairly.",
            "Blue is Improve, gray is No effect, orange is Worsen. Click a legend item to hide it.",
            "Group sizes are under each label; the 35+ groups are small.",
        ],
        [
            "Overall, 74% say music improves their mental health; 17 people (2%) say it makes things worse.",
            "Improve falls from 80% at 10–17 to 61% at 35–49, and No effect rises as it does.",
            "The 50+ group (n = 46) goes back up to 76%, but a few answers could move it.",
            "People judged music's effect themselves, so this shows belief, not a measured outcome.",
        ],
    )

# ------------------------------------------------------------------ Line chart
st.divider()
st.header("Do people who listen to a genre more often rate themselves differently?")
chart, notes = st.columns([3, 2], gap="large")
with chart:
    genres = genre_names(df)
    genre = st.selectbox("Genre", genres, index=genres.index("Pop"), key="line_genre")
    col = f"Frequency [{genre}]"
    means = df.groupby(col, observed=False)[CONDITIONS].mean().reindex(FREQ_LEVELS)
    n = df[col].value_counts().reindex(FREQ_LEVELS).fillna(0).astype(int)
    fig = go.Figure()
    for c in CONDITIONS:
        fig.add_scatter(x=FREQ_LEVELS, y=means[c], name=c, mode="lines+markers",
                        line=dict(color=CONDITION_COLORS[c], width=2.5),
                        marker=dict(symbol=CONDITION_SYMBOLS[c], size=9, color=CONDITION_COLORS[c]),
                        customdata=n.values, hovertemplate="%{x}: %{y:.2f} (n=%{customdata})<extra>" + c + "</extra>")
        fig.add_annotation(x=FREQ_LEVELS[-1], y=means[c].iloc[-1], text=c, showarrow=False, xanchor="left",
                           xshift=10, font=dict(color=CONDITION_COLORS[c], size=12))
    fig.update_layout(title=f"Average self-ratings by how often people listen to {genre}", showlegend=False,
                      xaxis_title=f"How often they listen to {genre}", yaxis=dict(title="Average self-rating (0–10)", range=[0, 10], dtick=2),
                      margin=dict(r=90))
    show(fig, extra="Group sizes: " + ", ".join(f"{k} {v}" for k, v in n.items()) + ".")
with notes:
    gap = (means.loc["Very frequently"] - means.loc["Never"]).round(2)
    biggest = gap.abs().idxmax()
    chart_notes(
        [
            "Left to right goes from people who never listen to the genre to those who listen very often.",
            "Each line is one condition, labeled at its end and marked with its own shape.",
            "The scale is fixed at 0–10, so a flat line means no difference.",
        ],
        [
            f"For {genre}, the biggest gap is in {biggest.lower()}: "
            f"{means.loc['Never', biggest]:.2f} for Never vs {means.loc['Very frequently', biggest]:.2f} for Very frequently.",
            f"Across all four conditions the gaps range from {gap.min():+.2f} to {gap.max():+.2f} points.",
            "For most genres the lines stay within about a point of each other.",
            "Every respondent is counted in every genre's chart, so these groups overlap.",
        ],
    )
