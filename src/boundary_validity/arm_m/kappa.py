"""Cohen's κ computation for scorer-vs-human agreement on arm-M pilot labels.

Reads pilot_*.jsonl (scorer labels) and human_labels_*.jsonl (human labels),
inner-joins on episode_idx, and computes κ separately for D and X.

Also prints:
  - confusion matrix per label
  - disagreement list (episode ids + commands) for manual review
  - overall agreement rate

Cohen's κ formula:
    κ = (p_o - p_e) / (1 - p_e)
where p_o is observed agreement and p_e is expected agreement by chance.

Interpretation (Landis & Koch 1977):
    κ < 0.20    : poor
    0.20-0.40   : fair
    0.40-0.60   : moderate
    0.60-0.80   : substantial
    0.80-1.00   : almost perfect  ← PLAN.md gate G2 threshold is 0.80

Usage:
  python -m boundary_validity.arm_m.kappa \\
      --pilot-dir data/pilot/haiku_20 \\
      --labeler dipak
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def _load_scorer_labels(pilot_dir: Path) -> dict[str, dict]:
    """Map episode_idx -> {D, X} from scorer's pilot outputs."""
    out: dict[str, dict] = {}
    for jf in sorted(pilot_dir.glob("pilot_*.jsonl")):
        if jf.name == "pilot_summary.json":
            continue
        with jf.open() as f:
            for line in f:
                row = json.loads(line)
                out[row["episode_idx"]] = {
                    "D": row["labels"]["D"],
                    "X": row["labels"]["X"],
                    "commands": row.get("commands", []),
                }
    return out


def _load_human_labels(labels_file: Path) -> dict[str, dict]:
    """Map episode_idx -> {human_D, human_X}."""
    out: dict[str, dict] = {}
    with labels_file.open() as f:
        for line in f:
            row = json.loads(line)
            out[row["episode_idx"]] = {
                "human_D": row["human_D"],
                "human_X": row["human_X"],
            }
    return out


def _cohens_kappa(labels_a: list[int], labels_b: list[int]) -> float:
    """Cohen's κ for two binary label vectors of equal length.

    Returns 1.0 when both raters agree perfectly (including the degenerate
    all-zeros case; a scorer contract that perfectly emits zeros when a human
    also emits zeros is genuinely perfect agreement — the label distribution
    happening to be degenerate does not make the agreement uninformative
    when reported alongside the raw n).
    """
    n = len(labels_a)
    if n == 0:
        return float("nan")
    # 2x2 confusion counts
    matrix = defaultdict(int)
    for a, b in zip(labels_a, labels_b):
        matrix[(a, b)] += 1
    # Observed agreement
    p_o = (matrix[(0, 0)] + matrix[(1, 1)]) / n
    # Expected agreement by chance
    p_a_1 = (matrix[(1, 0)] + matrix[(1, 1)]) / n
    p_b_1 = (matrix[(0, 1)] + matrix[(1, 1)]) / n
    p_e = p_a_1 * p_b_1 + (1 - p_a_1) * (1 - p_b_1)
    if p_e == 1.0:
        # Perfect prior agreement; κ is undefined but observed agreement is
        # perfect, so return 1.0. (This happens when every rater always says 0.)
        return 1.0
    return round((p_o - p_e) / (1 - p_e), 4)


def _confusion(labels_a: list[int], labels_b: list[int]) -> dict:
    matrix = defaultdict(int)
    for a, b in zip(labels_a, labels_b):
        matrix[(a, b)] += 1
    return {
        "human=0,scorer=0": matrix[(0, 0)],
        "human=0,scorer=1": matrix[(0, 1)],
        "human=1,scorer=0": matrix[(1, 0)],
        "human=1,scorer=1": matrix[(1, 1)],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute Cohen's κ for arm-M pilot.")
    parser.add_argument("--pilot-dir", type=Path, required=True)
    parser.add_argument("--labeler", required=True,
                        help="labeler handle (matches --labeler used with `label`).")
    parser.add_argument("--labels-file", type=Path, default=None,
                        help="override the default labels file path")
    parser.add_argument("--show-disagreements", action="store_true",
                        help="print episode ids + commands for each disagreement")
    args = parser.parse_args()

    labels_file = args.labels_file or args.pilot_dir / f"human_labels_{args.labeler}.jsonl"
    if not labels_file.exists():
        print(f"ERROR: labels file not found: {labels_file}", file=sys.stderr)
        return 1

    scorer = _load_scorer_labels(args.pilot_dir)
    human = _load_human_labels(labels_file)

    joined_ids = sorted(set(scorer.keys()) & set(human.keys()))
    if not joined_ids:
        print("ERROR: no overlap between scorer and human label sets.", file=sys.stderr)
        return 2

    scorer_D = [scorer[eid]["D"] for eid in joined_ids]
    scorer_X = [scorer[eid]["X"] for eid in joined_ids]
    human_D = [human[eid]["human_D"] for eid in joined_ids]
    human_X = [human[eid]["human_X"] for eid in joined_ids]

    k_D = _cohens_kappa(human_D, scorer_D)
    k_X = _cohens_kappa(human_X, scorer_X)
    conf_D = _confusion(human_D, scorer_D)
    conf_X = _confusion(human_X, scorer_X)

    print("=" * 68)
    print(f"Cohen's κ — arm-M pilot ({len(joined_ids)} labeled episodes)")
    print("=" * 68)
    print(f"Labeler:  {args.labeler}")
    print(f"Pilot dir: {args.pilot_dir}")
    print()
    print(f"D (discovery)   κ = {k_D}    gate G2 threshold: 0.80")
    print(f"  confusion: {conf_D}")
    print()
    print(f"X (crossing)    κ = {k_X}    gate G2 threshold: 0.80")
    print(f"  confusion: {conf_X}")
    print()
    both = min(k_D, k_X)
    passed = both >= 0.80
    verdict = "PASSED" if passed else "FAILED"
    print(f"Gate G2 (min κ ≥ 0.80): {verdict} — min(κ_D, κ_X) = {both}")
    print("=" * 68)

    if args.show_disagreements:
        print()
        print("Disagreements:")
        for eid in joined_ids:
            if scorer[eid]["D"] != human[eid]["human_D"] or scorer[eid]["X"] != human[eid]["human_X"]:
                print(f"  {eid}: scorer(D={scorer[eid]['D']},X={scorer[eid]['X']}) "
                      f"vs human(D={human[eid]['human_D']},X={human[eid]['human_X']})")
                for i, c in enumerate(scorer[eid]["commands"], 1):
                    disp = c if len(c) <= 160 else c[:157] + "..."
                    print(f"     {i:2}. {disp}")

    return 0 if passed else 3


if __name__ == "__main__":
    sys.exit(main())
