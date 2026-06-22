# Product Brief

## Purpose

Thesis Pillar Tracker keeps one investing thesis honest by breaking it into
named falsifiable pillars. Each pillar has an evidence log. Each month has one
review artifact. Each quarter has one binding-constraint snapshot.

## User

- A thesis owner who wants the evidence trail in Git.
- A reviewer who wants to see which facts confirm, weaken, or invalidate each
  pillar.
- A future implementation agent that needs clear file contracts before adding
  more automation.

## Operating Cadence

- Pillars change rarely.
- Evidence is appended when the human reviewer accepts a public event as
  relevant.
- Monthly reviews reference every active pillar.
- Quarterly snapshots state the current binding constraint and the change from
  the prior quarter.

## v0.1 Scope

- Typed Markdown files for pillars, reviews, and snapshots.
- A Python CLI for creating artifacts and appending evidence.
- Validation scripts for voice, spec shape, pillar schema, and review coverage.
- One checked-in monthly report artifact and one checked-in quarterly snapshot.

## Out Of Scope

- Intraday data.
- Price feeds.
- Options data.
- LLM-only verdicts.
- Multi-thesis support inside one repo.

