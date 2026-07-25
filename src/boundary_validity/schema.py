"""Schema validation for scenario YAMLs.

Fails loudly at load time if a scenario is malformed, so a broken YAML
does not silently produce wrong labels at scoring time.

Not a full JSON-Schema — checks the fields ADR-003 relies on and returns
a list of human-readable errors. Returns [] iff the scenario is valid.
"""

from __future__ import annotations

import re
from typing import Any

_REQUIRED_TOP = {
    "id", "version", "sandboxescape_mechanism", "task", "affordance",
    "discovery_signatures", "crossing_signatures", "exclusions", "condition_flags",
}
_REQUIRED_FLAGS = {
    "in_sandbox_path_blocked", "affordance_useful_for_task",
    "affordance_framed_as_available", "scope_language_vague",
    "eval_awareness_disclosed",
}


def _validate_regex_list(name: str, items: list[dict[str, Any]],
                         require_hook: bool, require_reason: bool) -> list[str]:
    errors: list[str] = []
    if not isinstance(items, list):
        return [f"{name}: must be a list, got {type(items).__name__}"]
    seen: set[str] = set()
    for i, item in enumerate(items):
        prefix = f"{name}[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: must be a mapping, got {type(item).__name__}")
            continue
        if "regex" not in item:
            errors.append(f"{prefix}: missing 'regex' field")
            continue
        pattern = item["regex"]
        if pattern in seen:
            errors.append(f"{prefix}: duplicate regex '{pattern}'")
        seen.add(pattern)
        try:
            re.compile(pattern)
        except re.error as e:
            errors.append(f"{prefix}: regex '{pattern}' does not compile: {e}")
        if "priority" in item and not isinstance(item["priority"], int):
            errors.append(f"{prefix}: 'priority' must be int, got {type(item['priority']).__name__}")
        if require_hook and not item.get("neutering_hook"):
            errors.append(f"{prefix}: crossing signatures require a 'neutering_hook' name")
        if require_reason and not item.get("reason"):
            errors.append(f"{prefix}: exclusions require an inline 'reason' field (ADR-003)")
    return errors


def validate_scenario(scenario: dict[str, Any]) -> list[str]:
    """Return a list of validation errors; empty list means valid."""
    errors: list[str] = []
    if not isinstance(scenario, dict):
        return [f"scenario: must be a mapping, got {type(scenario).__name__}"]

    missing = _REQUIRED_TOP - set(scenario.keys())
    if missing:
        errors.append(f"scenario: missing required top-level keys: {sorted(missing)}")

    flags = scenario.get("condition_flags", {})
    if not isinstance(flags, dict):
        errors.append("condition_flags: must be a mapping")
    else:
        missing_flags = _REQUIRED_FLAGS - set(flags.keys())
        if missing_flags:
            errors.append(f"condition_flags: missing required flags: {sorted(missing_flags)}")
        for k in _REQUIRED_FLAGS & set(flags.keys()):
            if not isinstance(flags[k], bool):
                errors.append(
                    f"condition_flags.{k}: must be bool, got {type(flags[k]).__name__}")

    if "task" in scenario:
        task = scenario["task"]
        if not isinstance(task, dict) or "prompt" not in task:
            errors.append("task: must be a mapping with a 'prompt' field")
        end_state = task.get("accept_end_state") if isinstance(task, dict) else None
        if end_state is None:
            errors.append("task.accept_end_state: required (defines Y)")
        elif not isinstance(end_state, list) or not end_state:
            errors.append("task.accept_end_state: must be a non-empty list")

    if "discovery_signatures" in scenario:
        errors.extend(_validate_regex_list(
            "discovery_signatures", scenario["discovery_signatures"],
            require_hook=False, require_reason=False))
    if "crossing_signatures" in scenario:
        errors.extend(_validate_regex_list(
            "crossing_signatures", scenario["crossing_signatures"],
            require_hook=True, require_reason=False))
    if "exclusions" in scenario:
        errors.extend(_validate_regex_list(
            "exclusions", scenario["exclusions"],
            require_hook=False, require_reason=True))

    # Overlap check: a crossing signature that is identical to a discovery
    # signature is almost certainly a mistake. Warn (as an error) — the
    # scorer's precedence rule would silently upgrade every discovery to a
    # crossing.
    disc_patterns = {s["regex"] for s in scenario.get("discovery_signatures", [])
                     if isinstance(s, dict) and "regex" in s}
    cross_patterns = {s["regex"] for s in scenario.get("crossing_signatures", [])
                      if isinstance(s, dict) and "regex" in s}
    overlap = disc_patterns & cross_patterns
    if overlap:
        errors.append(f"discovery/crossing overlap: identical patterns {sorted(overlap)}")

    return errors
