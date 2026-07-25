"""Inspect AI task wrapper for arm M.

Wires the frozen scorer (boundary_validity.scoring) into an Inspect AI
`@task` such that each episode:
  1. Presents the scenario's task.prompt to the model
  2. Gives the model a single `shell` tool backed by MockShell
  3. Records every command
  4. On completion, computes Y from MockShell's virtual FS state
  5. Runs commands through the frozen ADR-003 scorer → (D, X, X_manual_flag)
  6. Emits a Score
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import Score, Target, scorer, mean
from inspect_ai.solver import TaskState, generate, use_tools
from inspect_ai.tool import ToolResult, tool

from boundary_validity.scoring import load_scenario, score_trajectory

from .mock_shell import MockShell


# One MockShell instance per episode, keyed by sample id.
_SHELL_REGISTRY: dict[str, MockShell] = {}


def _shell_key(state: TaskState) -> str:
    return f"{state.sample_id}"


@tool
def mock_shell_tool(scenario: dict[str, Any]):
    """Inspect tool wrapping MockShell.execute.

    The tool is scenario-bound at task construction time. Every episode gets
    its own MockShell instance stored in _SHELL_REGISTRY, keyed by sample_id
    so the scorer can retrieve it.
    """
    async def execute(command: str) -> ToolResult:
        """Execute a shell command in the mock shell. Returns stdout on success.

        Args:
          command: The shell command to execute.
        """
        # Look up (or lazily create) the MockShell for this episode.
        # We can't cleanly get sample_id from here, so we use a per-scenario
        # instance and rely on the caller resetting it per episode.
        key = scenario.get("id", "default")
        shell = _SHELL_REGISTRY.get(key)
        if shell is None:
            shell = MockShell(scenario)
            _SHELL_REGISTRY[key] = shell
        result = shell.execute(command)
        if result.exit_code == 0:
            return result.stdout
        return f"[exit {result.exit_code}] {result.stderr}"

    return execute


@scorer(metrics=[mean()])
def trajectory_scorer(scenario: dict[str, Any]):
    """Extract commands from state.messages, compute Y, run ADR-003 scorer."""
    async def score(state: TaskState, target: Target) -> Score:
        key = scenario.get("id", "default")
        shell = _SHELL_REGISTRY.get(key)
        # Extract every shell tool call from the trajectory.
        commands: list[str] = []
        for msg in state.messages:
            tool_calls = getattr(msg, "tool_calls", None) or []
            for tc in tool_calls:
                # tc.arguments is a dict
                cmd = (tc.arguments or {}).get("command")
                if cmd:
                    commands.append(cmd)

        # Y from mock shell's virtual FS state
        y = False
        if shell is not None:
            accept = scenario.get("task", {}).get("accept_end_state", []) or []
            y = shell.check_end_state(accept)

        # Frozen ADR-003 scoring
        labels = score_trajectory(commands, scenario, y_reached=y)

        return Score(
            value={
                "D": int(labels.D),
                "X": int(labels.X),
                "Y": int(labels.Y),
                "manual_flag": int(labels.manual_review_flag),
            },
            metadata={
                "commands": commands,
                "manual_review_reasons": list(labels.manual_review_reasons),
                "crossing_attempts": list(shell.crossing_attempts) if shell else [],
                "num_commands": len(commands),
            },
        )

    return score


@task
def arm_m_task(scenario_id: str = "A") -> Task:
    """Build an Inspect AI task for one arm-M scenario."""
    scenario_path = _find_scenario_yaml(scenario_id)
    scenario = load_scenario(scenario_path)

    # Reset the shell registry for this scenario (fresh state per task build).
    _SHELL_REGISTRY.pop(scenario.get("id", "default"), None)

    system_prompt = scenario["task"]["prompt"]

    sample = Sample(
        id=f"arm_m_{scenario_id}",
        input=system_prompt,
        target="task_complete",
    )

    return Task(
        dataset=[sample],
        solver=[use_tools(mock_shell_tool(scenario)), generate()],
        scorer=trajectory_scorer(scenario),
    )


def _find_scenario_yaml(scenario_id: str) -> Path:
    """Locate scenario YAML by ID (A, B, C, D, E, F, G) or file path."""
    p = Path(scenario_id)
    if p.exists():
        return p
    # Try data/scenarios/<ID>/scenario.yaml relative to project root
    root = Path(__file__).resolve().parents[3]
    candidate = root / "data" / "scenarios" / scenario_id.upper() / "scenario.yaml"
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"scenario yaml not found for id={scenario_id}")


def reset_shell_registry() -> None:
    """Clear the per-scenario shell state. Call between episodes in tests."""
    _SHELL_REGISTRY.clear()


def get_shell(scenario_id_key: str) -> MockShell | None:
    """Return the MockShell instance for a scenario id (post-eval inspection)."""
    return _SHELL_REGISTRY.get(scenario_id_key)


def run_arm_m_episode(scenario_id: str, model) -> dict[str, Any]:
    """Run a single arm-M episode and return the score value + metadata.

    Convenience for tests. Uses inspect_ai.eval synchronously.
    """
    from inspect_ai import eval as inspect_eval

    reset_shell_registry()
    task_obj = arm_m_task(scenario_id)
    logs = inspect_eval(task_obj, model=model, display="none")
    # inspect_eval returns a list of EvalLog; one per Task
    log = logs[0]
    sample = log.samples[0]
    return {
        "score": sample.scores["trajectory_scorer"].value,
        "metadata": sample.scores["trajectory_scorer"].metadata,
    }
