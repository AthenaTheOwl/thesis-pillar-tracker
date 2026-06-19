# AGENTS.md — thesis-pillar-tracker

Operating contract for AI agents (Claude, Codex, Cursor) working in this
repo. Conventions match the wider AthenaTheOwl portfolio.

## What this repo is

A monthly review cadence on a single investing thesis, decomposed into
6-12 named falsifiable pillars. The repo's job is to produce typed
evidence logs and one verdict file per month, plus a quarterly
binding-constraint snapshot. Not a dashboard. Not a real-time feed.

## Roles you may see in tasks

| Role | What they do |
|---|---|
| `pillar-author` | Drafts the pillar set; defines falsification criteria |
| `evidence-logger` | Tags new public events against existing pillars |
| `monthly-reviewer` | Aggregates the month's evidence; emits the verdict file |
| `snapshot-writer` | Once per quarter writes the binding-constraint snapshot |

Not all roles are implemented in v0.

## Voice constraints

- No marketing words. No "leverage", "synergy", "best-in-class",
  "seamless", "cutting-edge".
- No antithetical reversals as a structural device.
- Plain assertions. The pillars and the evidence are the moat.
- Honest about uncertainty: WEAKENS is allowed; INVALIDATES is allowed.

## Gates (will land in spec 0002)

Before any monthly review is committed:

```bash
uv run pytest
python scripts/voice_lint.py
python scripts/spec_check.py
python scripts/validate_pillar_schema.py
```

Pillars and evidence files are validated against schemas. Verdict files
must reference every pillar in scope.

## Out of scope

- Live prices, intraday data, options chains. Monthly cadence only.
- LLM-graded verdicts. Tagging is human-in-the-loop; the LLM may
  suggest, the human commits.
- Other theses. One thesis per repo. Fork for a second thesis.
