# Thesis Pillar Tracker

Thesis Pillar Tracker is a monthly data-report repo for one investing thesis.
It decomposes the thesis into 6-12 named falsifiable pillars, records accepted
evidence against those pillars, and writes one monthly review file plus one
quarterly binding-constraint snapshot.

## Current Shape

- Six starter pillars live under `thesis/`.
- The first monthly report artifact is `monthly_reviews/2026-06.md`.
- The first machine-readable report artifact is `reports/2026-06-monthly.jsonl`.
- The first quarterly snapshot is `quarterly_snapshots/2026Q2.md`.
- The Python package exposes the `tpt` CLI.
- Local gates live in `scripts/`.

## Run

```bash
uv sync
uv run tpt --help
uv run pytest
python scripts/voice_lint.py
python scripts/spec_check.py
python scripts/validate_pillar_schema.py
```

## show

`tpt show` reads the committed pillars and prints a ranked standing - how
strongly the accepted evidence still backs each constraint - plus a headline
on the strongest pillar and any pillar to watch. read-only, offline.

```bash
uv run tpt show
```

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

## CLI Examples

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
