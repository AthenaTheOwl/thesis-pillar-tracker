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

from thesis_pillar_tracker.model import Pillar, load_pillars
from thesis_pillar_tracker.scoring import (
    VALID_VERDICTS,
    VERDICT_WEIGHT,
    pillar_standing,
    rank_pillars,
)

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

st.divider()
st.subheader("score a pillar yourself")
st.caption(
    "build your own evidence log and watch the standing recompute live. this drives the "
    "real engine - `thesis_pillar_tracker.scoring.pillar_standing` - the same function "
    "that ranks the committed pillars above. CONFIRMS +1, WEAKENS -1, INVALIDATES -2, "
    "NEUTRAL 0. flip a verdict and the standing flips with it."
)

VERDICT_OPTIONS = sorted(VALID_VERDICTS)

# pre-fill with a committed example so the section starts populated, then let the user edit.
seed_id = next((s.id for s in standings), "my-pillar")
seed = by_id.get(seed_id)
seed_rows = (
    [
        {"date": row.date, "verdict": row.verdict, "source": row.source, "note": row.note}
        for row in seed.real_evidence
    ]
    if seed and seed.real_evidence
    else [
        {"date": "2026-04-18", "verdict": "CONFIRMS", "source": "earnings call", "note": "capacity still sold out"},
        {"date": "2026-06-12", "verdict": "WEAKENS", "source": "capex update", "note": "guidance raised, gap narrowing"},
    ]
)

col_id, col_title = st.columns(2)
my_id = col_id.text_input("pillar id", value=seed.id if seed else "my-pillar")
my_title = col_title.text_input(
    "title / claim", value=seed.title if seed else "my constraint stays binding"
)

st.markdown("**evidence log** - edit rows, change verdicts, add or delete. recomputes live.")
edited = st.data_editor(
    seed_rows,
    column_config={
        "date": st.column_config.TextColumn("date", help="YYYY-MM-DD", width="small"),
        "verdict": st.column_config.SelectboxColumn(
            "verdict", options=VERDICT_OPTIONS, width="small", required=True
        ),
        "source": st.column_config.TextColumn("source"),
        "note": st.column_config.TextColumn("note", width="large"),
    },
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="evidence_editor",
)


def _build_pillar(pillar_id: str, title: str, rows: list[dict]) -> Pillar:
    """Render user rows into the exact evidence-log shape the real parser reads, then
    hand the engine a real Pillar. No scoring logic lives here - pillar_standing does it."""
    lines = ["## Evidence log", ""]
    for row in rows:
        date = str(row.get("date") or "").strip()
        verdict = str(row.get("verdict") or "").strip().upper()
        source = str(row.get("source") or "").strip() or "source"
        note = str(row.get("note") or "").strip() or "note"
        if not date or not verdict:
            continue
        lines.append(f"- {date} {verdict} [{source}] - {note}")
    body = "\n".join(lines)
    data = {"id": pillar_id or "my-pillar", "title": title or pillar_id, "status": "active"}
    return Pillar(path=REPO / "thesis" / "live.md", data=data, body=body)


rows = [r for r in edited if str(r.get("date") or "").strip()]
if not rows:
    st.warning("add at least one evidence row with a date to score this pillar.")
else:
    my_pillar = _build_pillar(my_id, my_title, rows)
    standing = pillar_standing(my_pillar)  # <- the real engine, on your input

    m1, m2, m3 = st.columns(3)
    m1.metric("standing", standing.standing)
    m2.metric("score", f"{standing.score:+d}")
    m3.metric("latest verdict", standing.latest_verdict)

    contributions = " + ".join(
        f"{row.verdict}({VERDICT_WEIGHT.get(row.verdict, 0):+d})"
        for row in standing.real_evidence
    )
    st.markdown(
        f"`{standing.id}` -> **{standing.standing}** "
        f"(score {standing.score:+d} from {len(standing.real_evidence)} accepted rows)"
    )
    if contributions:
        st.caption(f"score = {contributions} = {standing.score:+d}")

    if standing.score < 0:
        st.error(
            f"net-negative: accepted evidence is eroding this constraint "
            f"(standing **{standing.standing}**). this is where a reviewer acts."
        )
    elif standing.score == 0:
        st.warning(
            f"net-zero (**{standing.standing}**): evidence cancels out or none is logged. "
            "needs a clearer accepted verdict before raising confidence."
        )
    else:
        st.success(
            f"net-positive (**{standing.standing}**): accepted evidence still backs the "
            "constraint. add a WEAKENS or INVALIDATES row to see it turn."
        )

st.caption(
    "v0.1 ships six starter pillars with backfilled public-event evidence. the model "
    "+ scoring live in `thesis_pillar_tracker/`; this page reads the committed "
    "`thesis/*.md` and drives the same scoring engine on your input above. "
    "repo: github.com/AthenaTheOwl/thesis-pillar-tracker"
)
