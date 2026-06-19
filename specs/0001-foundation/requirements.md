# Requirements — 0001 Foundation

The scaffold for Thesis Pillar Tracker. Implementation lives in later specs.

## Functional requirements

- **R-TPT-001** The repo SHALL maintain a directory `thesis/` containing one
  Markdown file per pillar, named `<pillar_id>.md`.
- **R-TPT-002** Each pillar file SHALL contain a YAML frontmatter block with
  fields: `id`, `title`, `claim`, `falsification`, `created`, `status`.
- **R-TPT-003** Status SHALL be one of: `active`, `weakened`, `invalidated`,
  `retired`.
- **R-TPT-004** Each pillar file SHALL contain an append-only evidence log
  below the frontmatter; entries are timestamped and tagged with a verdict
  from {CONFIRMS, WEAKENS, INVALIDATES, NEUTRAL}.
- **R-TPT-005** The repo SHALL maintain `monthly_reviews/YYYY-MM.md` files;
  each file is written once at the end of the review cycle and is not
  edited after commit.
- **R-TPT-006** Each monthly review file SHALL reference every active
  pillar and include a `portfolio_action_required` boolean.
- **R-TPT-007** The repo SHALL maintain `quarterly_snapshots/YYYYQn.md`
  files; each names the current binding constraint and the delta vs the
  prior quarter.
- **R-TPT-008** The repo SHALL ship a CLI entry point `tpt` that exposes
  `new-pillar`, `log-evidence`, `monthly-review`, and `quarterly-snapshot`
  subcommands (implementation in spec 0002).

## Non-functional requirements

- **R-TPT-009** All Markdown SHALL pass `scripts/voice_lint.py` before
  commit.
- **R-TPT-010** Pillar and review schemas SHALL be validated by
  `scripts/validate_pillar_schema.py` before commit.
- **R-TPT-011** The first pillar set SHALL contain between 6 and 12
  pillars; values outside this range SHALL fail validation.
- **R-TPT-012** A monthly review SHALL be considered "shippable" only
  when it references the full active pillar set.
