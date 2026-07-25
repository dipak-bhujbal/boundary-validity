"""Developer CLI for boundary-validity.

Two subcommands so far:

  validate    Validate one or more scenario YAMLs against the ADR-003 schema.
              Exits non-zero if any scenario has errors.

  score       Score a trajectory (one shell command per line, from stdin or a
              file) against a scenario. Emits JSON with the extracted labels
              and matched signatures for hand-adjudication.

Not intended for use inside the harness — the harness will call the scoring
functions directly. This is for ad-hoc scenario checks and building up the
hand-adjudicated trajectory corpus (ADR-003 §Validation).
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path

from .schema import validate_scenario
from .scoring import load_scenario, score_trajectory


def _cmd_validate(args: argparse.Namespace) -> int:
    exit_code = 0
    for path in args.paths:
        path = Path(path)
        if path.is_dir():
            targets = sorted(path.rglob("scenario.yaml"))
        else:
            targets = [path]
        for target in targets:
            try:
                scenario = load_scenario(target)
            except Exception as e:
                print(f"{target}: FAILED to load: {e}", file=sys.stderr)
                exit_code = 1
                continue
            errors = validate_scenario(scenario)
            if errors:
                exit_code = 1
                print(f"{target}: {len(errors)} error(s)", file=sys.stderr)
                for err in errors:
                    print(f"  {err}", file=sys.stderr)
            else:
                print(f"{target}: ok")
    return exit_code


def _cmd_score(args: argparse.Namespace) -> int:
    scenario = load_scenario(args.scenario)
    errors = validate_scenario(scenario)
    if errors:
        print(f"scenario failed validation:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1
    if args.trajectory == "-":
        commands = [line.rstrip("\n") for line in sys.stdin if line.strip()]
    else:
        with open(args.trajectory, "r", encoding="utf-8") as f:
            commands = [line.rstrip("\n") for line in f if line.strip()]
    labels = score_trajectory(commands, scenario, y_reached=args.y)
    payload = {
        "scenario_id": scenario["id"],
        "D": labels.D,
        "X": labels.X,
        "Y": labels.Y,
        "A": labels.A,
        "matched_signatures": [dataclasses.asdict(m) for m in labels.matched_signatures],
        "matched_exclusions": [dataclasses.asdict(m) for m in labels.matched_exclusions],
    }
    print(json.dumps(payload, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="boundary-validity")
    sub = parser.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="validate scenario YAMLs")
    v.add_argument("paths", nargs="+", help="scenario.yaml files or directories")
    v.set_defaults(func=_cmd_validate)

    s = sub.add_parser("score", help="score a trajectory against a scenario")
    s.add_argument("--scenario", required=True, help="path to scenario.yaml")
    s.add_argument("--trajectory", default="-",
                   help="path to trajectory file (one command per line), or - for stdin")
    s.add_argument("--y", action="store_true",
                   help="mark benign task as reached (Y=True)")
    s.set_defaults(func=_cmd_score)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
