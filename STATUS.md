# Status

## Current state
- v0.1 has a typed file model for pillars, monthly reviews, and quarterly snapshots.
- The Python package exposes `tpt` with `new-pillar`, `log-evidence`, `monthly-review`, `quarterly-snapshot`, and `validate`.
- Six starter pillars exist under `thesis/`; each has neutral scaffold evidence entries.
- `monthly_reviews/2026-06.md` is the checked-in report artifact for the first review cycle.
- `quarterly_snapshots/2026Q2.md` records the first binding-constraint snapshot as a working prior.
- Local gates are present in `scripts/` and wired through `make validate`.

## Known limits
- The starter evidence entries are neutral scaffold records, not public-event backfill.
- The CLI writes Markdown skeletons; it does not judge verdicts.
- The validators use simple frontmatter parsing for the repo's current file shape.
- Monthly review files are protected by convention and CLI no-overwrite behavior, not by Git hooks.

## Next feature queue
- Backfill public-event evidence for the first six pillars.
- Add a review template that counts monthly evidence entries per pillar.
- Add a changelog for monthly review artifacts.
- Add CI once the factory owns the repo remote.

- Resolve factory defect: missing PRODUCT_BRIEF.md,SYSTEM_MAP.md
- Resolve factory defect: missing reports/*.jsonl
- Resolve factory defect: PRODUCT_BRIEF.md is required for active repos
- Resolve factory defect: SYSTEM_MAP.md is required for active repos
- Resolve factory defect: expected file 'PRODUCT_BRIEF.md' is missing
- Resolve factory defect: expected file 'SYSTEM_MAP.md' is missing
- Resolve factory defect: expected file 'thesis_pillar_tracker/cli.py' is missing
- Resolve factory defect: expected glob 'reports/*.jsonl' matched no files
- Resolve factory defect: module 'cli' declares source 'thesis_pillar_tracker/cli.py', but it is missing
- Resolve factory defect: module 'model' declares source 'thesis_pillar_tracker/model.py', but it is missing
- Resolve factory defect: module 'report' declares source 'thesis_pillar_tracker/scoring.py', but it is missing
- Resolve factory defect: claude_code review requested patch; inspect defect log
