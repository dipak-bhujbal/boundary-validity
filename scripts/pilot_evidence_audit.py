"""Post-amendment pilot evidence audit + summary regeneration.

Motivation
----------
The OSF amendment for DOI 10.17605/OSF.IO/2KH7B (filed 2026-07-25) pins commit
d023f8f and references data/pilot/smoke_v6/pilot_summary.json as evidence for a
four-model n=10 smoke_v6 study. At d023f8f, that file summarized only the
GPT-5-mini subset (2 of 8 cells). Raw JSONLs for the other 6 cells exist locally
with mtimes 20:22-20:39 EDT on 2026-07-25, predating the amendment filing
(commit d023f8f was created at 22:05:18 EDT, so amendment filing >= 22:05).

This script:
  1. Emits a machine-readable audit table for every file under data/pilot/.
     Columns: dir, filename, tracked_at_d023f8f, mtime, n_rows_or_cells,
     scenarios, models.
  2. Regenerates the complete pilot_summary.json for smoke_v6 (8 cells) and
     multi (all cells present locally) from the raw JSONLs, matching the exact
     schema produced by src/boundary_validity/arm_m/pilot.py._cell_summary.
  3. Writes outputs to data/pilot/audit_20260726/ so codex can diff+recompute
     before anything gets committed.

Fields we cannot reconstruct from JSONL:
  - elapsed_seconds: only known at run time. Set to null with a note.
  - per_channel_rates: populated only when matched_signatures is present in the
    JSONL. Current smoke_v6 and multi pilot JSONLs do not contain that field, so
    regenerated summaries omit per-channel rates.

Usage: run from repo root:
    python scripts/pilot_evidence_audit.py
"""
from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PILOT = REPO / "data" / "pilot"
OUT = PILOT / "audit_20260726"
PIN_COMMIT = "d023f8f33744a831ed9dbe88e34c5bffaa67eacb"


def tracked_at(path: Path, commit: str) -> bool:
    rel = path.relative_to(REPO)
    r = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}:{rel}"],
        cwd=REPO, capture_output=True,
    )
    return r.returncode == 0


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _infer_scenario_model_from_filename(out_file_rel: str) -> tuple[str | None, str | None]:
    """Parse `pilot_<SCEN>_<provider>_<model-slug>.jsonl` back to (scenario, model)."""
    stem = Path(out_file_rel).stem  # pilot_A_google_gemini-2.5-flash
    parts = stem.split("_", 3)
    if len(parts) < 4 or parts[0] != "pilot":
        return None, None
    scenario = parts[1]
    provider_and_slug = parts[2] + "_" + parts[3]  # google_gemini-2.5-flash
    if "_" not in provider_and_slug:
        return scenario, None
    provider, slug = provider_and_slug.split("_", 1)
    return scenario, f"{provider}/{slug}"


def cell_summary(rows: list[dict], out_file_rel: str) -> dict:
    """Reproduce src/boundary_validity/arm_m/pilot.py._cell_summary exactly,
    minus elapsed_seconds (unrecoverable from JSONL)."""
    n = len(rows)
    if n == 0:
        scenario, model = _infer_scenario_model_from_filename(out_file_rel)
        return {
            "scenario_id": scenario,
            "model": model,
            "n_episodes": 0,
            "elapsed_seconds": None,
            "output_file": out_file_rel,
            "empty_note": (
                "raw JSONL exists but contains zero episode rows; "
                "this cell was attempted but produced no data (likely provider error, "
                "quota, or unavailable SKU at run time)"
            ),
        }

    scenario_ids = {r["scenario_id"] for r in rows}
    models = {r["model"] for r in rows}
    assert len(scenario_ids) == 1, f"mixed scenarios in {out_file_rel}: {scenario_ids}"
    assert len(models) == 1, f"mixed models in {out_file_rel}: {models}"

    label_counts: Counter = Counter()
    for r in rows:
        label_counts[(r["labels"]["D"], r["labels"]["X"], r["labels"]["Y"])] += 1

    out = {
        "scenario_id": next(iter(scenario_ids)),
        "model": next(iter(models)),
        "n_episodes": n,
        "elapsed_seconds": None,
        "elapsed_seconds_note": (
            "unrecoverable from JSONL; original run-time value not preserved"
        ),
        "discovery_rate": round(sum(r["labels"]["D"] for r in rows) / n, 4),
        "crossing_rate": round(sum(r["labels"]["X"] for r in rows) / n, 4),
        "completion_rate": round(sum(r["labels"]["Y"] for r in rows) / n, 4),
        "manual_flag_rate": round(sum(r["labels"]["manual_flag"] for r in rows) / n, 4),
        "label_distribution": {
            f"D={d},X={x},Y={y}": c for (d, x, y), c in label_counts.items()
        },
        "output_file": out_file_rel,
    }

    has_coverage = all("coverage_ok" in r["labels"] and "coverage_rate" in r for r in rows)
    if has_coverage:
        retained = [r for r in rows if r["labels"]["coverage_ok"] == 1]
        coverage_clean_rate = round(sum(r["labels"]["coverage_ok"] for r in rows) / n, 4)
        mean_coverage_rate = round(sum(r["coverage_rate"] for r in rows) / n, 4)
        retained_mean_coverage = round(
            sum(r["coverage_rate"] for r in retained) / len(retained), 4
        ) if retained else None
        exclusion_rate = round(1 - coverage_clean_rate, 4)
        out.update({
            "coverage_clean_episode_rate": coverage_clean_rate,
            "mean_command_coverage": mean_coverage_rate,
            "retained_mean_coverage": retained_mean_coverage,
            "exclusion_rate": exclusion_rate,
            "n_retained": len(retained),
        })
    else:
        out["coverage_fields_note"] = (
            "coverage_ok / coverage_rate / retention not in this JSONL's schema; "
            "predates coverage instrumentation added in commit eabc2e8"
        )

    if all("matched_signatures" in r for r in rows):
        channel_counts: Counter = Counter()
        for r in rows:
            seen = {s.get("label", "?") for s in r.get("matched_signatures", []) if s.get("label")}
            for lbl in seen:
                channel_counts[lbl] += 1
        out["per_channel_rates"] = {lbl: round(c / n, 4) for lbl, c in channel_counts.items()}

    return out


def audit_dir(subdir: Path) -> list[dict]:
    rows_audit = []
    for p in sorted(subdir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(REPO)
        entry = {
            "path": str(rel),
            "tracked_at_d023f8f": tracked_at(p, PIN_COMMIT),
            "size_bytes": p.stat().st_size,
        }
        if p.suffix == ".jsonl":
            try:
                rows = load_jsonl(p)
                entry["n_rows"] = len(rows)
                entry["scenarios"] = sorted({r.get("scenario_id") for r in rows})
                entry["models"] = sorted({r.get("model") for r in rows})
            except Exception as e:
                entry["parse_error"] = str(e)
        elif p.suffix == ".json":
            try:
                data = json.loads(p.read_text())
                entry["schema"] = "pilot_summary"
                entry["scenarios_in_summary"] = data.get("scenarios")
                entry["models_in_summary"] = data.get("models")
                entry["n_cells"] = len(data.get("cells", []))
            except Exception as e:
                entry["parse_error"] = str(e)
        rows_audit.append(entry)
    return rows_audit


def build_summary_for(subdir: Path) -> dict:
    jsonls = sorted(subdir.glob("pilot_*.jsonl"))
    cells = []
    scenarios = set()
    models = set()
    ns = set()
    for p in jsonls:
        rows = load_jsonl(p)
        s = cell_summary(rows, out_file_rel=str(p.relative_to(REPO)))
        cells.append(s)
        if s["n_episodes"]:
            scenarios.add(s["scenario_id"])
            models.add(s["model"])
            ns.add(s["n_episodes"])
    episodes_per_cell = ns.pop() if len(ns) == 1 else sorted(ns)
    return {
        "scenarios": sorted(scenarios),
        "models": sorted(models),
        "episodes_per_cell": episodes_per_cell,
        "regenerated_from": "raw JSONLs on disk",
        "regenerated_note": (
            "Post-amendment audit regen; original pilot_summary.json at commit "
            f"{PIN_COMMIT} was incomplete relative to the raw JSONLs present locally. "
            "This regenerated summary covers every raw JSONL under the directory. "
            "elapsed_seconds fields cannot be reconstructed and are null."
        ),
        "cells": cells,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    # 1. Full audit table
    all_audit = []
    for sub in sorted(PILOT.iterdir()):
        if not sub.is_dir() or sub.name == OUT.name:
            continue
        all_audit.extend(audit_dir(sub))
    (OUT / "pilot_evidence_audit.json").write_text(
        json.dumps({"pin_commit": PIN_COMMIT, "entries": all_audit}, indent=2)
    )
    print(f"wrote {OUT/'pilot_evidence_audit.json'} ({len(all_audit)} entries)")

    # 2. Regenerated summaries
    for name in ("smoke_v6", "multi"):
        sub = PILOT / name
        if not sub.exists():
            print(f"skip {name}: dir missing")
            continue
        summary = build_summary_for(sub)
        out_path = OUT / f"{name}_pilot_summary_regen.json"
        out_path.write_text(json.dumps(summary, indent=2))
        n_cells = len(summary["cells"])
        n_models = len(summary["models"])
        n_scen = len(summary["scenarios"])
        print(f"wrote {out_path}  cells={n_cells} models={n_models} scenarios={n_scen}")

    # 3. Coverage delta: what was in tracked summary vs what's in regen
    print("\n=== coverage delta ===")
    for name in ("smoke_v6", "multi"):
        try:
            tracked_summary = json.loads(
                subprocess.check_output(
                    ["git", "show", f"{PIN_COMMIT}:data/pilot/{name}/pilot_summary.json"],
                    cwd=REPO,
                )
            )
            tracked_cells = {(c["scenario_id"], c["model"]) for c in tracked_summary["cells"]}
        except Exception as e:
            print(f"  {name}: tracked summary unreadable: {e}")
            continue
        regen = json.loads((OUT / f"{name}_pilot_summary_regen.json").read_text())
        regen_cells = {(c["scenario_id"], c["model"]) for c in regen["cells"] if c.get("n_episodes")}
        added = regen_cells - tracked_cells
        dropped = tracked_cells - regen_cells
        print(f"  {name}: tracked={len(tracked_cells)} regen={len(regen_cells)} "
              f"added={len(added)} dropped={len(dropped)}")
        for s, m in sorted(added):
            print(f"    + ({s}, {m})")
        for s, m in sorted(dropped):
            print(f"    - ({s}, {m})")


if __name__ == "__main__":
    main()
