# Design - 0002

## Package

The package uses a top-level package layout:

```
thesis_pillar_tracker/
  __init__.py
  cli.py
  model.py
  scoring.py
```

`model.py` is the file-contract layer. It validates ids, reads simple
frontmatter, renders pillar and snapshot Markdown, and writes those files.
`scoring.py` owns evidence verdict validation, monthly review rendering, and
report-row rendering. `cli.py` is an argparse wrapper over those layers.

## CLI

The CLI creates and edits only repo artifacts:

- `new-pillar` writes `thesis/<id>.md`.
- `log-evidence` appends to an existing pillar file.
- `monthly-review` writes `monthly_reviews/YYYY-MM.md`.
- `quarterly-snapshot` writes `quarterly_snapshots/YYYYQn.md`.
- `validate` delegates to the schema validator.

## Validation

The validator checks:

- Pillar ids match filenames.
- Required frontmatter fields exist.
- Pillar status values are in the allowed set.
- Evidence lines use `YYYY-MM-DD VERDICT [source] - note`.
- The active pillar count is between 6 and 12.
- Each monthly review references every active pillar.

## Storage

There is no database. Git is the audit log. Markdown stays readable so a human
reviewer can inspect evidence without running code.
