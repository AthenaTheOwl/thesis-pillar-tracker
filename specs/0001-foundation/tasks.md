# Tasks — 0001 Foundation

Ordered for the first 2-3 PRs after this scaffold.

## PR 1 — Pillar schema + first six pillars

- [ ] Add `schemas/pillar.schema.json` constraining YAML frontmatter
- [ ] Add `scripts/validate_pillar_schema.py`
- [ ] Add `scripts/voice_lint.py` copied from sports-prediction-os
- [ ] Author the first six pillars under `thesis/`
- [ ] Add a `Makefile` target `make validate` that runs both scripts
- [ ] Confirm `make validate` passes locally

## PR 2 — Backfill three months of evidence

- [ ] For each of the six pillars, log evidence from the prior 3 months
- [ ] Format every entry as `YYYY-MM-DD VERDICT [source] — note`
- [ ] Re-run `make validate`
- [ ] Open `monthly_reviews/2026-06.md` and write a review skeleton

## PR 3 — CLI surface

- [ ] Add `pyproject.toml` with `tpt` console script
- [ ] Implement `tpt new-pillar`
- [ ] Implement `tpt log-evidence`
- [ ] Implement `tpt monthly-review`
- [ ] Add pytest smoke tests for each subcommand
- [ ] Add `make test` target chaining `pytest` then `make validate`

## Out of scope for foundation

- [ ] LLM-suggested verdicts (later spec)
- [ ] Per-pillar Brier scoring (depends on brief-calibration)
- [ ] Quarterly snapshot CLI (spec 0003)
