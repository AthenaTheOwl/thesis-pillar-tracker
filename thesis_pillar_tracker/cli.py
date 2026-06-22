from __future__ import annotations

import argparse
import sys
from pathlib import Path

from thesis_pillar_tracker.model import (
    ArtifactError,
    create_pillar,
    create_quarterly_snapshot,
)
from thesis_pillar_tracker.scoring import (
    append_evidence,
    create_monthly_review,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tpt",
        description="Create and validate thesis pillar review artifacts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_pillar = subparsers.add_parser("new-pillar", help="create a pillar file")
    add_root(new_pillar)
    new_pillar.add_argument("--id", required=True)
    new_pillar.add_argument("--title", required=True)
    new_pillar.add_argument("--claim", required=True)
    new_pillar.add_argument("--falsification", required=True)
    new_pillar.add_argument("--created")
    new_pillar.set_defaults(func=cmd_new_pillar)

    log_evidence = subparsers.add_parser("log-evidence", help="append evidence")
    add_root(log_evidence)
    log_evidence.add_argument("--pillar", required=True)
    log_evidence.add_argument("--source", required=True)
    log_evidence.add_argument("--verdict", required=True)
    log_evidence.add_argument("--note", required=True)
    log_evidence.add_argument("--date")
    log_evidence.set_defaults(func=cmd_log_evidence)

    monthly = subparsers.add_parser("monthly-review", help="create a monthly review")
    add_root(monthly)
    monthly.add_argument("--month", required=True)
    monthly.add_argument("--force", action="store_true")
    monthly.set_defaults(func=cmd_monthly_review)

    quarterly = subparsers.add_parser(
        "quarterly-snapshot",
        help="create a quarterly binding-constraint snapshot",
    )
    add_root(quarterly)
    quarterly.add_argument("--quarter", required=True)
    quarterly.add_argument("--binding-constraint", required=True)
    quarterly.add_argument("--delta", required=True)
    quarterly.add_argument("--confidence", default="low")
    quarterly.add_argument("--force", action="store_true")
    quarterly.set_defaults(func=cmd_quarterly_snapshot)

    validate = subparsers.add_parser("validate", help="run pillar schema validation")
    add_root(validate)
    validate.set_defaults(func=cmd_validate)

    return parser


def add_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--root",
        default=".",
        help="repo root to read and write; defaults to the current directory",
    )


def cmd_new_pillar(args: argparse.Namespace) -> int:
    path = create_pillar(
        pillar_id=args.id,
        title=args.title,
        claim=args.claim,
        falsification=args.falsification,
        root=Path(args.root),
        created=args.created,
    )
    print(path)
    return 0


def cmd_log_evidence(args: argparse.Namespace) -> int:
    path = append_evidence(
        pillar_id=args.pillar,
        verdict=args.verdict,
        source=args.source,
        note=args.note,
        root=Path(args.root),
        event_date=args.date,
    )
    print(path)
    return 0


def cmd_monthly_review(args: argparse.Namespace) -> int:
    path = create_monthly_review(
        root=Path(args.root),
        month=args.month,
        force=args.force,
    )
    print(path)
    return 0


def cmd_quarterly_snapshot(args: argparse.Namespace) -> int:
    path = create_quarterly_snapshot(
        root=Path(args.root),
        quarter=args.quarter,
        binding_constraint=args.binding_constraint,
        delta=args.delta,
        confidence=args.confidence,
        force=args.force,
    )
    print(path)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    from scripts.validate_pillar_schema import validate_repo

    validate_repo(Path(args.root))
    print("OK: pillar schema validated.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ArtifactError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
