"""Real-model smoke test for arm M.

Runs a single arm-M episode with a real Anthropic model. Intended purely to
verify the plumbing (Inspect AI + tool + scorer + registry) works against a
non-mock model, before any full pilot run.

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python -m boundary_validity.arm_m.real_model_smoke --scenario A \\
      --model anthropic/claude-haiku-4-5

Cost cap: single episode, turn_limit=10, expected total spend < $0.10.
"""

from __future__ import annotations

import argparse
import os
import sys

from inspect_ai import eval as inspect_eval
from inspect_ai.model import GenerateConfig

from .task import arm_m_task, reset_shell_registry


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Arm-M smoke test with a real model. Runs one episode."
    )
    parser.add_argument("--scenario", default="A",
                        help="scenario id (A, B, C, D, E, F, G). Default: A")
    parser.add_argument("--model", default="anthropic/claude-haiku-4-5",
                        help="Inspect AI model spec. Default: cheapest Haiku")
    parser.add_argument("--turn-limit", type=int, default=20,
                        help="hard cap on tool-use turns per episode (was 10, bumped to 20 after real-model observation)")
    args = parser.parse_args()

    # Provider-specific env-var check (only Anthropic wired here; expand later).
    if args.model.startswith("anthropic/") and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        print("Set it with: export ANTHROPIC_API_KEY=sk-ant-...", file=sys.stderr)
        return 1

    reset_shell_registry()
    task_obj = arm_m_task(args.scenario)

    print(f"Running arm-M scenario {args.scenario} with model {args.model}...")
    print(f"(turn limit: {args.turn_limit}, single episode)")
    print()

    logs = inspect_eval(
        task_obj,
        model=args.model,
        display="rich",
        limit=1,
        message_limit=args.turn_limit * 2,  # tool call + result = 2 messages per turn
    )

    log = logs[0]
    sample = log.samples[0]
    score = sample.scores.get("trajectory_scorer")
    if score is None:
        print("ERROR: no score produced.", file=sys.stderr)
        return 2

    print()
    print("=" * 60)
    print(f"Scenario:   {args.scenario}")
    print(f"Model:      {args.model}")
    print(f"D:          {score.value['D']}")
    print(f"X:          {score.value['X']}")
    print(f"Y:          {score.value['Y']}")
    print(f"manual_flag:{score.value['manual_flag']}")
    print(f"num_cmds:   {score.metadata.get('num_commands')}")
    print(f"crossings:  {score.metadata.get('crossing_attempts')}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
