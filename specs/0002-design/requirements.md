# Requirements - 0002 Design

## Functional Requirements

- **R-TPT-013** The repo shall include a package-installable Python module named
  `thesis_pillar_tracker`.
- **R-TPT-014** The package shall expose a console script named `tpt`.
- **R-TPT-015** `tpt new-pillar` shall create a pillar file with required
  frontmatter and an evidence-log section.
- **R-TPT-016** `tpt log-evidence` shall append one dated evidence line to an
  existing pillar.
- **R-TPT-017** `tpt monthly-review` shall create a monthly review skeleton that
  references every active pillar.
- **R-TPT-018** `tpt quarterly-snapshot` shall create a quarterly snapshot
  skeleton.
- **R-TPT-019** `STATUS.md` shall keep the exact `Current state`, `Known
  limits`, and `Next feature queue` sections.

## Non-Functional Requirements

- **R-TPT-020** Local validation shall run with no external services.
- **R-TPT-021** The Python project shall use uv dependency groups for dev
  dependencies.
- **R-TPT-022** The Python project shall set `[tool.uv] package = true`.
- **R-TPT-023** Existing monthly review artifacts shall not be overwritten by
  CLI commands unless the caller passes `--force`.

