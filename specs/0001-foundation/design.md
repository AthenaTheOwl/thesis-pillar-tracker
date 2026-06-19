# Design — 0001 Foundation

## Architecture sketch

Thesis Pillar Tracker is a typed-artifact pipeline with three artifact
classes: pillars, evidence events, and review summaries. The Python CLI is
a thin wrapper over file IO plus schema validation. There is no database,
no daemon, no service.

```
+--------------+        +-----------------+        +-------------------+
| pillar files |  --->  | monthly review  |  --->  | quarterly snapshot|
| (append-only)|        | (write-once)    |        | (write-once)      |
+--------------+        +-----------------+        +-------------------+
        ^                       ^
        |                       |
   evidence-logger        monthly-reviewer
        |                       |
        +-------- tpt CLI ------+
```

## Data model

Pillar file (`thesis/<id>.md`):

```yaml
---
id: chip-cowos-2027
title: CoWoS supply remains binding through 2027 Q2
claim: TSMC CoWoS-L allocation cannot keep up with announced accelerator demand
falsification: A quarterly TSMC update showing CoWoS supply exceeding committed demand for two consecutive quarters
created: 2026-06-19
status: active
---

## Evidence log
- 2026-06-15 CONFIRMS [TSMC 2026 Q2 call transcript] — packaging utilization remains at >95%, lead times extended to 12 months
- 2026-05-30 NEUTRAL [SemiAnalysis post] — no incremental information
```

Monthly review file (`monthly_reviews/2026-07.md`):

```yaml
---
month: 2026-07
pillars_reviewed: [chip-cowos-2027, ...]
portfolio_action_required: false
---
```

## CLI surface (spec 0002)

- `tpt new-pillar --id ID --title TITLE` — creates `thesis/ID.md` from
  template.
- `tpt log-evidence --pillar ID --source URL --verdict V` — appends a
  line to the pillar evidence log.
- `tpt monthly-review --month YYYY-MM` — generates the review file
  skeleton; human fills in verdicts.
- `tpt quarterly-snapshot --quarter YYYYQn` — generates the snapshot
  file skeleton.

## Schema validation

A JSON Schema at `schemas/pillar.schema.json` constrains the YAML
frontmatter. `scripts/validate_pillar_schema.py` walks `thesis/` and
fails if any file is malformed. The same script enforces R-TPT-011 (6-12
pillars).

## Voice

`scripts/voice_lint.py` is copied from the portfolio canonical at
sports-prediction-os; banned word list mirrors that file.
