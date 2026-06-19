# First PR after the scaffold

This document names the literal first PR opened against the repo after the
scaffold lands. Scope is intentionally narrow: pillar schema, validator,
voice lint, and the first six pillars. No CLI yet.

## Title

`feat: pillar schema, validator, first six pillars`

## Files changed

- `schemas/pillar.schema.json` (new) — JSON Schema for the YAML
  frontmatter block. Required fields: id, title, claim, falsification,
  created, status. Status enum: active, weakened, invalidated, retired.
- `scripts/validate_pillar_schema.py` (new) — walks `thesis/`, parses
  frontmatter, validates against the schema, asserts pillar count is in
  [6, 12].
- `scripts/voice_lint.py` (new) — copied from sports-prediction-os; the
  banned word list is the source of truth there, do not duplicate the
  list in commentary.
- `thesis/chip-cowos-2027.md` (new)
- `thesis/hbm-allocation-2027.md` (new)
- `thesis/pjm-capacity-2027.md` (new)
- `thesis/ercot-load-2027.md` (new)
- `thesis/transformer-leadtime.md` (new)
- `thesis/substrate-abf-supply.md` (new)
- `Makefile` (new) — `make validate` target running both scripts.

## What each pillar file contains

Frontmatter (per R-TPT-002) plus a single placeholder evidence entry of
form:

```
- 2026-06-19 NEUTRAL [scaffold] — initial commit, no evidence yet
```

## Verification

After the PR is opened:

```bash
make validate
```

Expected output: `OK: 6 pillars validated.` Zero exit code.

A reviewer should also eyeball the six claims for plausibility and
falsification specificity. A pillar whose falsification is "if it goes
wrong" is not a pillar; reject and revise.

## Why this PR is the right first PR

- It binds the data shape before any code is written against it.
- It produces a runnable validator on a clean clone.
- It lets PR 2 backfill evidence without further schema churn.
- It does not commit to a CLI surface yet; that is PR 3.

## What this PR does NOT do

- No CLI. `tpt` lands in PR 3.
- No live evidence. Backfill is PR 2's job.
- No monthly review skeleton. Also PR 2.
- No GitHub Action. Local `make validate` is the gate for now.
