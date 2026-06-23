"""thesis-pillar-tracker - live demo (Streamlit Community Cloud).

Reads the committed pillar files under thesis/*.md and shows how each thesis
pillar is standing: how strongly the accepted evidence still backs its
constraint. No network, no secrets - runs entirely off the committed files.

Deploy: Streamlit Community Cloud -> New app -> repo AthenaTheOwl/thesis-pillar-tracker,
branch main, main file streamlit_app.py.
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from thesis_pillar_tracker.model import load_pillars
from thesis_pillar_tracker.scoring import rank_pillars

REPO = Path(__file__).resolve().parent

st.set_page_config(page_title="thesis-pillar-tracker - pillar standing", layout="wide")
st.title("thesis-pillar-tracker")
st.caption(
    "one investing thesis, decomposed into falsifiable pillars. this page ranks "
    "the pillars by how strongly the accepted evidence still backs each constraint "
    "(CONFIRMS +1, WEAKENS -1, INVALIDATES -2)."
)

pillars = load_pillars(REPO)
if not pillars:
    st.warning("no pillar files found under thesis/*.md")
    st.stop()

standings = rank_pillars(pillars)

total = len(standings)
holding = sum(1 for s in standings if s.score > 0)
at_risk = sum(1 for s in standings if s.score < 0)

c1, c2, c3 = st.columns(3)
c1.metric("pillars", total)
c2.metric("holding", holding, help="net-positive accepted evidence")
c3.metric("at risk", at_risk, help="net-negative or invalidated", delta=None)

st.subheader("pillar standing - ranked")
st.dataframe(
    [
        {
            "rank": index,
            "pillar": s.id,
            "standing": s.standing,
            "score": s.score,
            "evidence": len(s.real_evidence),
            "latest verdict": s.latest_verdict,
            "title": s.title,
        }
        for index, s in enumerate(standings, start=1)
    ],
    use_container_width=True,
    hide_index=True,
)

strongest = standings[0]
weakest = standings[-1]
if weakest.score < 0:
    st.info(
        f"**watch:** {weakest.id} is {weakest.standing} (score {weakest.score:+d}); "
        f"latest accepted evidence {weakest.latest_verdict}. "
        f"strongest constraint is {strongest.id} (score {strongest.score:+d})."
    )
else:
    st.info(
        f"**strongest constraint:** {strongest.id} ({strongest.standing}, "
        f"score {strongest.score:+d} from {len(strongest.real_evidence)} accepted "
        "evidence rows). no pillar is currently net-negative."
    )

st.subheader("inspect a pillar")
by_id = {s.id: s for s in standings}
selected = st.selectbox("pillar", list(by_id), index=0)
chosen = by_id[selected]

st.markdown(f"**{chosen.title}**")
st.markdown(f"- claim: {chosen.pillar.data.get('claim', '')}")
st.markdown(f"- falsification: {chosen.pillar.data.get('falsification', '')}")
st.markdown(
    f"- standing: **{chosen.standing}** (score {chosen.score:+d}, "
    f"{len(chosen.real_evidence)} accepted evidence rows)"
)

st.markdown("**evidence log** (oldest first)")
for row in chosen.evidence:
    if row.source == "scaffold":
        continue
    st.markdown(f"- `{row.date}` **{row.verdict}** [{row.source}] - {row.note}")

st.caption(
    "v0.1 ships six starter pillars with backfilled public-event evidence. the model "
    "+ scoring live in `thesis_pillar_tracker/`; this page reads the committed "
    "`thesis/*.md`. repo: github.com/AthenaTheOwl/thesis-pillar-tracker"
)
