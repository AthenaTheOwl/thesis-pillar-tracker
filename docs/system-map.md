# System Map

## Artifact Flow

```
pillar author
  -> thesis/<pillar_id>.md
  -> evidence logger appends dated verdict lines
  -> monthly reviewer writes monthly_reviews/YYYY-MM.md
  -> report writer emits reports/YYYY-MM-monthly.jsonl
  -> snapshot writer writes quarterly_snapshots/YYYYQn.md
```

## File Contracts

- `thesis/*.md` files carry frontmatter plus an append-only evidence log.
- `monthly_reviews/*.md` files list every active pillar in scope.
- `reports/*.jsonl` files carry machine-readable monthly verdict rows.
- `quarterly_snapshots/*.md` files name the current binding constraint and the
  delta from the prior quarter.
- `schemas/*.json` documents the typed shape used by scripts and reviewers.

## Runtime Components

- `thesis_pillar_tracker/model.py` owns artifact data shapes, parsing, and
  file-contract validation.
- `thesis_pillar_tracker/scoring.py` owns evidence verdict validation,
  monthly review rendering, and report-row rendering.
- `thesis_pillar_tracker/cli.py` exposes the `tpt` command.
- `scripts/validate_pillar_schema.py` checks pillar fields, evidence-line
  shape, and monthly review coverage.
- `scripts/spec_check.py` checks repo-level contract items.
- `scripts/voice_lint.py` checks Markdown prose for banned terms.

## Gate Sequence

```
uv run pytest
python scripts/voice_lint.py
python scripts/spec_check.py
python scripts/validate_pillar_schema.py
```
