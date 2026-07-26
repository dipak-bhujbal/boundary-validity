"""Arm-M pilot runner.

Runs N episodes per scenario across a list of models via Inspect AI, writes
per-episode records to a JSONL file per (scenario, model) cell.

Output layout:
  <output>/pilot_{scenario}_{model_slug}.jsonl    # one row per episode
  <output>/pilot_summary.json                     # cell-level aggregates

Each JSONL row contains:
  - scenario_id
  - model
  - episode_idx
  - labels: {D, X, Y, manual_flag}
  - commands: list[str]
  - crossing_attempts: list[str]
  - manual_review_reasons: list[str]
  - log_path: relative path to the Inspect AI .eval log for this sample

Usage:
  python -m boundary_validity.arm_m.pilot \\
      --scenarios A B C D E F G \\
      --model anthropic/claude-haiku-4-5 \\
      --episodes 20 \\
      --output data/pilot/haiku_20/
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

from inspect_ai import eval as inspect_eval
from inspect_ai.dataset import MemoryDataset, Sample

from .task import arm_m_task, reset_shell_registry


def _model_slug(model: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", model)


def _api_key_check(model: str) -> tuple[bool, str]:
    """Return (ok, message). Only Anthropic is auto-checked; others are
    left to Inspect AI to surface the error naturally."""
    if model.startswith("anthropic/") and not os.environ.get("ANTHROPIC_API_KEY"):
        return False, "ANTHROPIC_API_KEY not set"
    if model.startswith("openai/") and not os.environ.get("OPENAI_API_KEY"):
        return False, "OPENAI_API_KEY not set"
    if model.startswith("google/") and not os.environ.get("GOOGLE_API_KEY"):
        return False, "GOOGLE_API_KEY not set"
    if model.startswith("together/") and not os.environ.get("TOGETHER_API_KEY"):
        return False, "TOGETHER_API_KEY not set"
    return True, ""


def run_cell(
    scenario_id: str,
    model: str,
    n_episodes: int,
    turn_limit: int,
    out_dir: Path,
) -> dict:
    """Run one (scenario, model) cell of the pilot. Returns cell summary."""
    reset_shell_registry()

    # Build a task with N identical samples so Inspect AI parallelizes them.
    task_obj = arm_m_task(scenario_id)
    base_sample = list(task_obj.dataset)[0]
    duplicated = MemoryDataset([
        Sample(
            id=f"arm_m_{scenario_id}_ep{i:03d}",
            input=base_sample.input,
            target=base_sample.target,
        )
        for i in range(n_episodes)
    ])
    task_obj.dataset = duplicated

    print(f"  running {scenario_id} × {n_episodes} episodes on {model}...",
          flush=True)
    t0 = time.time()
    logs = inspect_eval(
        task_obj,
        model=model,
        display="none",
        message_limit=turn_limit * 2,
    )
    elapsed = time.time() - t0

    log = logs[0]
    rows: list[dict] = []
    label_counts = Counter()
    for sample in log.samples:
        score = sample.scores.get("trajectory_scorer")
        if score is None:
            continue
        v = score.value
        m = score.metadata or {}
        row = {
            "scenario_id": scenario_id,
            "model": model,
            "episode_idx": sample.id,
            "labels": {
                "D": int(v.get("D", 0)),
                "X": int(v.get("X", 0)),
                "Y": int(v.get("Y", 0)),
                "manual_flag": int(v.get("manual_flag", 0)),
                "coverage_ok": int(v.get("coverage_ok", 1)),
            },
            "commands": m.get("commands", []),
            "crossing_attempts": m.get("crossing_attempts", []),
            "manual_review_reasons": m.get("manual_review_reasons", []),
            "unparsed_commands": m.get("unparsed_commands", []),
            "coverage_rate": m.get("coverage_rate", 1.0),
            "num_commands": m.get("num_commands", 0),
        }
        rows.append(row)
        label_counts[(row["labels"]["D"], row["labels"]["X"], row["labels"]["Y"])] += 1

    # Write per-cell JSONL
    slug = _model_slug(model)
    out_file = out_dir / f"pilot_{scenario_id}_{slug}.jsonl"
    with out_file.open("w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

    # Aggregate: crossing rate = mean(X), discovery rate = mean(D), etc.
    n = len(rows)
    # Four balance-criterion numbers per Codex's stopping-criterion framing:
    #   (1) retained_mean_coverage: mean cmd coverage on episodes with
    #       coverage_ok=1 (i.e. coverage_rate >= 0.80). This must be >= 0.90.
    #   (2) exclusion_rate: fraction of episodes with coverage_ok=0.
    #       This must be <= 0.20.
    #   (3) all-episode mean coverage (for context).
    #   (4) retention count (for context on how many episodes make it through).
    retained = [r for r in rows if r["labels"]["coverage_ok"] == 1]
    coverage_clean_rate = round(sum(r["labels"]["coverage_ok"] for r in rows) / n, 4) if n else None
    mean_coverage_rate = round(sum(r["coverage_rate"] for r in rows) / n, 4) if n else None
    retained_mean_coverage = round(
        sum(r["coverage_rate"] for r in retained) / len(retained), 4
    ) if retained else None
    exclusion_rate = round(1 - coverage_clean_rate, 4) if coverage_clean_rate is not None else None
    summary = {
        "scenario_id": scenario_id,
        "model": model,
        "n_episodes": n,
        "elapsed_seconds": round(elapsed, 2),
        "discovery_rate": round(sum(r["labels"]["D"] for r in rows) / n, 4) if n else None,
        "crossing_rate": round(sum(r["labels"]["X"] for r in rows) / n, 4) if n else None,
        "completion_rate": round(sum(r["labels"]["Y"] for r in rows) / n, 4) if n else None,
        "manual_flag_rate": round(sum(r["labels"]["manual_flag"] for r in rows) / n, 4) if n else None,
        "coverage_clean_episode_rate": coverage_clean_rate,
        "mean_command_coverage": mean_coverage_rate,
        "retained_mean_coverage": retained_mean_coverage,
        "exclusion_rate": exclusion_rate,
        "n_retained": len(retained),
        "label_distribution": {f"D={d},X={x},Y={y}": c for (d, x, y), c in label_counts.items()},
        "output_file": str(out_file),
    }
    print(f"    → n={n}  D̄={summary['discovery_rate']}  X̄={summary['crossing_rate']}"
          f"  Ȳ={summary['completion_rate']}"
          f"  excl={exclusion_rate}  retained_cov={retained_mean_coverage}"
          f"  ({summary['elapsed_seconds']}s)",
          flush=True)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Arm-M pilot loop.")
    parser.add_argument("--scenarios", nargs="+", default=["A", "B", "C", "D", "E", "F", "G"],
                        help="scenario ids to run (default: all 7)")
    parser.add_argument("--model", action="append", default=None,
                        help="model spec. Repeat for multiple. Default: single Haiku.")
    parser.add_argument("--episodes", type=int, default=20,
                        help="episodes per (scenario, model) cell. Default: 20 (pilot).")
    parser.add_argument("--turn-limit", type=int, default=20,
                        help="hard cap on tool-use turns per episode.")
    parser.add_argument("--output", type=Path, default=Path("data/pilot/latest"),
                        help="output directory for JSONL + summary.")
    args = parser.parse_args()

    models = args.model or ["anthropic/claude-haiku-4-5"]
    for m in models:
        ok, msg = _api_key_check(m)
        if not ok:
            print(f"ERROR: {m}: {msg}", file=sys.stderr)
            return 1

    args.output.mkdir(parents=True, exist_ok=True)
    print(f"Arm-M pilot: {len(args.scenarios)} scenarios × {len(models)} models "
          f"× {args.episodes} episodes = {len(args.scenarios) * len(models) * args.episodes} total")
    print(f"Output: {args.output}")
    print()

    summaries: list[dict] = []
    for model in models:
        print(f"Model: {model}")
        for scenario_id in args.scenarios:
            summary = run_cell(scenario_id, model, args.episodes, args.turn_limit, args.output)
            summaries.append(summary)

    # Write overall summary
    summary_file = args.output / "pilot_summary.json"
    with summary_file.open("w") as f:
        json.dump({
            "scenarios": args.scenarios,
            "models": models,
            "episodes_per_cell": args.episodes,
            "cells": summaries,
        }, f, indent=2)

    print()
    print(f"Wrote summary to {summary_file}")
    print()
    print("=" * 60)
    print("PILOT SUMMARY")
    print("=" * 60)
    print(f"{'scenario':10} {'model':40} {'n':>4} {'D̄':>6} {'X̄':>6} {'Ȳ':>6}")
    for s in summaries:
        d = "  n/a" if s["discovery_rate"] is None else f"{s['discovery_rate']:>6}"
        x = "  n/a" if s["crossing_rate"] is None else f"{s['crossing_rate']:>6}"
        y = "  n/a" if s["completion_rate"] is None else f"{s['completion_rate']:>6}"
        print(f"{s['scenario_id']:10} {s['model'][:38]:40} {s['n_episodes']:>4} "
              f"{d} {x} {y}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
