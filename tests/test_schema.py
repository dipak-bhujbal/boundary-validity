"""Tests for the scenario schema validator."""

from pathlib import Path

import pytest

from boundary_validity.schema import validate_scenario
from boundary_validity.scoring import load_scenario

SCENARIOS_DIR = Path(__file__).parent.parent / "data" / "scenarios"


def _load(cond: str) -> dict:
    return load_scenario(SCENARIOS_DIR / cond / "scenario.yaml")


@pytest.mark.parametrize("cond", ["A", "B", "C", "D", "E", "F", "G"])
def test_all_scenarios_validate(cond):
    """Every committed scenario must validate cleanly. This is the primary
    guard against ADR-003 schema drift as conditions are added or edited."""
    errors = validate_scenario(_load(cond))
    assert errors == [], f"condition {cond}: {errors}"


class TestValidatorCatchesBrokenScenarios:
    def _base(self):
        # Minimal valid scenario as a baseline.
        return {
            "id": "test",
            "version": 0,
            "sandboxescape_mechanism": "test_mech",
            "task": {
                "prompt": "do the thing",
                "accept_end_state": [{"kind": "file_exists", "path": "/x"}],
            },
            "affordance": {"description": "..."},
            "discovery_signatures": [
                {"regex": r"^ls\s", "priority": 10, "label": "ls"},
            ],
            "crossing_signatures": [
                {"regex": r"^docker\s", "priority": 20, "label": "docker",
                 "neutering_hook": "hook"},
            ],
            "exclusions": [
                {"regex": r"^ls /work$", "reason": "task activity"},
            ],
            "condition_flags": {
                "in_sandbox_path_blocked": False,
                "affordance_useful_for_task": True,
                "affordance_framed_as_available": False,
                "scope_language_vague": False,
                "eval_awareness_disclosed": False,
            },
        }

    def test_baseline_is_valid(self):
        assert validate_scenario(self._base()) == []

    def test_missing_top_level_key(self):
        s = self._base()
        del s["affordance"]
        errors = validate_scenario(s)
        assert any("affordance" in e for e in errors)

    def test_bad_regex(self):
        s = self._base()
        s["discovery_signatures"][0]["regex"] = "(unclosed"
        errors = validate_scenario(s)
        assert any("does not compile" in e for e in errors)

    def test_crossing_without_hook_rejected(self):
        s = self._base()
        del s["crossing_signatures"][0]["neutering_hook"]
        errors = validate_scenario(s)
        assert any("neutering_hook" in e for e in errors)

    def test_exclusion_without_reason_rejected(self):
        s = self._base()
        del s["exclusions"][0]["reason"]
        errors = validate_scenario(s)
        assert any("reason" in e for e in errors)

    def test_missing_condition_flag_rejected(self):
        s = self._base()
        del s["condition_flags"]["eval_awareness_disclosed"]
        errors = validate_scenario(s)
        assert any("eval_awareness_disclosed" in e for e in errors)

    def test_priority_type_check(self):
        s = self._base()
        s["discovery_signatures"][0]["priority"] = "10"  # string, not int
        errors = validate_scenario(s)
        assert any("priority" in e for e in errors)

    def test_duplicate_regex_flagged(self):
        s = self._base()
        s["discovery_signatures"].append(
            {"regex": r"^ls\s", "priority": 10, "label": "dup"})
        errors = validate_scenario(s)
        assert any("duplicate" in e for e in errors)

    def test_discovery_crossing_overlap_flagged(self):
        s = self._base()
        s["discovery_signatures"][0]["regex"] = r"^docker\s"  # collides with crossing
        errors = validate_scenario(s)
        assert any("overlap" in e for e in errors)
