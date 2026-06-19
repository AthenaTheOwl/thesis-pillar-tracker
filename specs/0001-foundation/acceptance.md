# Acceptance — 0001 Foundation

## What v0 done means

- The repo has six named pillars under `thesis/`, each with a falsifiable
  claim and three months of evidence entries.
- `monthly_reviews/2026-06.md` exists and references all six pillars.
- `make validate` passes on a clean clone.
- `tpt --help` lists `new-pillar`, `log-evidence`, `monthly-review`.

## Commands to run

```bash
git clone <repo>
cd thesis-pillar-tracker
uv sync
make validate
uv run tpt --help
```

Expected: zero exit codes; help text lists three subcommands.

## Gates to pass

- `python scripts/voice_lint.py thesis/ monthly_reviews/` — no banned
  terms.
- `python scripts/validate_pillar_schema.py` — every pillar file matches
  the schema and the active-pillar count is in [6, 12].
- `uv run pytest` — smoke tests for each CLI subcommand pass.

## Out of scope for acceptance

- Quarterly snapshot CLI (spec 0003).
- Live evidence ingestion (spec 0004 if ever).
- Calibration against published predictions (brief-calibration repo's job).
