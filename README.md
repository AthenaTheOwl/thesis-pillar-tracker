# Thesis Pillar Tracker

Decomposes the semis / AI-infra thesis into 6-12 named falsifiable pillars.
Tags each new 10-Q line, fab announcement, CHIPS milestone, and FERC ruling
as CONFIRMS, WEAKENS, or INVALIDATES per pillar, with a quarterly one-page
"binding constraint moved" snapshot embedded.

## What this is

A monthly typed-artifact pipeline for a single working investing thesis.
Each pillar is a falsifiable claim ("CoWoS supply remains binding through
2027 Q2", "PJM capacity prices stay above $200/MW-day"). Each evidence
event is logged once, tagged against affected pillars, and given a verdict.
The output is a monthly verdict file plus a quarterly binding-constraint
snapshot.

The repo absorbs the older Fab+Hyperscaler Constraint Graph idea by
shipping the constraint layer as a quarterly memo rather than a live graph.
Maintenance budget is one cadence per month plus one snapshot per quarter.

Pillars live in `thesis/<pillar_id>.md` as append-only evidence logs.
Each monthly verdict file is committed at the end of the review cycle and
never edited; the next month starts a new file.

## Status

v0 scaffold; no implementation yet. The spec ledger names the pillar
schema, the evidence-event schema, the monthly verdict template, and the
quarterly snapshot template. Code lands in spec 0002.

## How to run

Will land in spec 0002. The expected shape:

```bash
uv sync
uv run tpt new-pillar --id chip-cowos-2027 --title "CoWoS binding through 2027 Q2"
uv run tpt log-evidence --pillar chip-cowos-2027 --source "TSMC 2026 Q2 earnings" --verdict CONFIRMS
uv run tpt monthly-review --month 2026-07
uv run tpt quarterly-snapshot --quarter 2026Q3
```

For v0 the only working command is `uv run tpt --help` showing the
unimplemented subcommands.

## Layout

```
thesis-pillar-tracker/
  thesis/                       # one file per pillar, append-only evidence log
  monthly_reviews/              # YYYY-MM.md verdict files
  quarterly_snapshots/          # YYYYQn.md constraint-moved snapshots
  src/tpt/                      # CLI + schemas (lands in spec 0002)
  specs/0001-foundation/        # this scaffold
  docs/first-pr.md              # the next PR after this scaffold
  AGENTS.md
  LICENSE
  README.md
```

## License

MIT. See LICENSE.
