# thesis-pillar-tracker

Six constraints hold up one investing thesis. Five are still standing. One —
ABF substrate supply — went down this month: two evidence rows, latest verdict
INVALIDATES, score -2. The tracker stamps that on the page so nobody pretends the
thesis is intact when a leg has already snapped.

## What it does

A thesis is a story, and stories survive their own falsification by accident — the
number that broke them gets filed somewhere and the narrative keeps walking. This
repo refuses that. It breaks the thesis into 6 to 12 named, falsifiable pillars,
each with a written claim and the exact condition that would kill it. Then it logs
accepted evidence against each pillar — CONFIRMS, WEAKENS, NEUTRAL, INVALIDATES —
and scores every constraint by how strongly the evidence still holds it up.

Six starter pillars ship checked in: CoWoS packaging, ERCOT load, HBM allocation,
PJM capacity, ABF substrate, transformer lead times. Each month it writes one
review file; each quarter, one binding-constraint snapshot. The evidence is the
audit trail, so a pillar can't quietly survive being invalidated — the standing
table puts it last and labels it.

## try it

One command, no setup. It reads the committed pillars and prints where each
constraint stands:

```bash
uv run tpt show
```

```
thesis pillar standing - ranked by how strongly accepted evidence
still backs each constraint (CONFIRMS +1, WEAKENS -1, INVALIDATES -2)

 #  pillar                 standing        score evid latest      title
-----------------------------------------------------------------------
 1  hbm-allocation-2027    holding            +2    3 NEUTRAL     HBM allocation remains tight for leading acceler
 2  transformer-leadtime   holding            +2    2 CONFIRMS    Transformer lead times remain a grid bottleneck
 3  chip-cowos-2027        holding            +1    3 WEAKENS     CoWoS supply remains binding through 2027 Q2
 4  ercot-load-2027        holding            +1    3 WEAKENS     ERCOT load growth stays ahead of firm capacity a
 5  pjm-capacity-2027      contested          +0    2 WEAKENS     PJM capacity prices stay elevated
 6  substrate-abf-supply   invalidated        -2    2 INVALIDATES ABF substrate supply remains constrained for adv

strongest constraint: hbm-allocation-2027 (holding, score +2 from 3 evidence rows).
watch: substrate-abf-supply is invalidated (score -2); latest evidence INVALIDATES. review before next monthly close.
```

Ranked by standing, the broken pillar at the bottom. Read-only, offline.

## live demo

A root `streamlit_app.py` renders the same ranked standing as an interactive
page: metrics, a ranked table, a headline callout, and a per-pillar evidence
inspector. It reads the committed `thesis/*.md` directly - no network, no secrets.

Run locally:

```bash
uv run --with streamlit streamlit run streamlit_app.py
```

Deploy on Streamlit Community Cloud: New app -> repo
`AthenaTheOwl/thesis-pillar-tracker`, branch `main`, main file `streamlit_app.py`.

<!-- live-url: (add the Streamlit Community Cloud URL here once deployed) -->

## How it connects

The pillars are not abstract — they name the same chokepoints the rest of the
cluster instruments. This repo is the scoreboard; the siblings are the wires.

- [grid-silicon](https://github.com/AthenaTheOwl/grid-silicon) — the ERCOT
  load and transformer pillars, as phantom-vs-real megawatts on the wire.
- [interconnect-alpha](https://github.com/AthenaTheOwl/interconnect-alpha) —
  the survival model behind the PJM-capacity and ERCOT-load constraints.
- [chip-supply-chain-map](https://github.com/AthenaTheOwl/chip-supply-chain-map)
  / [fab-risk-radar](https://github.com/AthenaTheOwl/fab-risk-radar) — the CoWoS,
  HBM, and ABF-substrate pillars, traced back to the fabs they bind.
- [earnings-pillar-diff](https://github.com/AthenaTheOwl/earnings-pillar-diff) —
  reads earnings transcripts for the evidence rows this tracker logs.

## CLI examples

```bash
uv run tpt new-pillar \
  --id chip-cowos-2027 \
  --title "CoWoS supply remains binding through 2027 Q2" \
  --claim "Advanced packaging capacity remains a gating constraint for accelerator shipments through 2027 Q2" \
  --falsification "Two consecutive quarterly supplier updates show supply above committed accelerator demand"

uv run tpt log-evidence \
  --pillar chip-cowos-2027 \
  --source "accepted public event" \
  --verdict CONFIRMS \
  --note "reviewer-approved evidence note"

uv run tpt monthly-review --month 2026-07
uv run tpt quarterly-snapshot \
  --quarter 2026Q3 \
  --binding-constraint "advanced packaging capacity" \
  --delta "unchanged from prior quarter"
```

## Run

```bash
uv sync
uv run tpt --help
uv run pytest
python scripts/voice_lint.py
python scripts/spec_check.py
python scripts/validate_pillar_schema.py
```

## Layout

```
thesis-pillar-tracker/
  PRODUCT_BRIEF.md              # product contract
  SYSTEM_MAP.md                 # artifact and runtime map
  monthly_reviews/              # YYYY-MM.md review artifacts
  quarterly_snapshots/          # YYYYQn.md constraint snapshots
  reports/                      # YYYY-MM-monthly.jsonl report rows
  schemas/                      # documented artifact schemas
  scripts/                      # local validation gates
  specs/0001-foundation/        # scaffold spec
  specs/0002-design/            # v0.1 implementation ledger
  thesis_pillar_tracker/        # CLI, model, and scoring modules
  tests/                        # pytest suite
  thesis/                       # one file per pillar
  STATUS.md
```

## License

MIT. See LICENSE.
