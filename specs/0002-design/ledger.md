# Ledger - 0002

## Decision Records

- `D-0002-001`: Use Markdown plus frontmatter as the storage format.
- `D-0002-002`: Keep validators dependency-light so gates run on a clean clone
  after `uv run`.
- `D-0002-003`: Treat monthly reviews as write-once artifacts. CLI commands
  refuse to overwrite them unless `--force` is passed.
- `D-0002-004`: Keep evidence verdicts human-authored. The CLI records verdicts;
  it does not infer them.

## Traceability

- R-TPT-013 through R-TPT-018 map to `thesis_pillar_tracker/`.
- R-TPT-019 maps to `STATUS.md` and `scripts/spec_check.py`.
- R-TPT-020 maps to all scripts under `scripts/`.
- R-TPT-021 and R-TPT-022 map to `pyproject.toml`.
- R-TPT-023 maps to artifact writer checks in `model.py` and `scoring.py`.
