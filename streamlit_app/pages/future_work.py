"""Future work and reflection on the paper prototype."""
import streamlit as st

from utils import lede

st.title("Future work")
lede("This survey can show patterns but not explain them. Here's what I'd build next to get closer to answers.")

st.subheader("Next steps")
st.markdown(
    "1. **Test whether the genre gaps are real.** Add confidence intervals to the gallery and a "
    "Kruskal–Wallis test across favorite genres, so readers can tell a real difference from noise in a small group.\n"
    "2. **Look at the conditions together.** Anxiety, depression and insomnia overlap, so clustering "
    "respondents into symptom-and-listening profiles would say more than one condition at a time.\n"
    "3. **Compare against validated measures.** Pair this with PHQ-9 and GAD-7 data, ideally from a "
    "treatment program that uses music in its groups, to see whether self-ratings tell the same story.\n"
    "4. **Run a real accessibility audit.** Screen reader and keyboard-only testing, WCAG contrast checks "
    "on every color pair, and a downloadable table behind each chart as a text alternative.\n"
    "5. **A/B test the dashboard layout.** Sidebar filters against filters above the charts, measured by "
    "how quickly a first-time user can find one insight."
)

st.subheader("What changed from my Lab 4.3 paper prototype")
# TODO (Simon): replace with what actually changed from your own paper prototype.
st.markdown(
    "- **Filters moved to the sidebar** so the KPIs and charts stay in view while you change them.\n"
    "- **Every filtered number got a baseline.** The prototype showed filtered values alone; now each "
    "KPI and bar is compared with the whole survey.\n"
    "- **A pie chart became a horizontal bar**, because lengths are easier to compare than slices, "
    "especially for the small Worsen group.\n"
    "- **Small genres came out of the box plot.** Groups under 20 people produced medians that looked "
    "more meaningful than they were."
)
