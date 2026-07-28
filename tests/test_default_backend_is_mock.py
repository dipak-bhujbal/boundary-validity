"""Regression guard (ADR-007 safety): the default arm-M backend is MockShell.

RealShell (real bash-in-Docker) is Proposed / review-only. It MUST NOT become the
arm-M backend without an explicit, reviewed code change. task.py currently wires
MockShell by construction and never references RealShell, which is the structural
"can't silently flip to real" guarantee the arm-M-real safety preflight relied on.
These tests fail loudly if that guarantee ever regresses, so a change that swaps in
the real substrate cannot pass CI unnoticed.
"""

from __future__ import annotations

import inspect

from boundary_validity.arm_m import task as task_module


def test_task_module_wires_mockshell_not_realshell():
    """task.py must back the shell tool with MockShell and never wire RealShell."""
    src = inspect.getsource(task_module)
    assert "MockShell" in src, "task.py must back the shell tool with MockShell"
    assert "RealShell" not in src and "real_shell" not in src, (
        "task.py must NOT wire RealShell: it is Proposed/review-only (ADR-007). "
        "Switching the default backend requires an explicit, reviewed change — "
        "not a silent import swap."
    )


def test_shell_registry_is_typed_mockshell():
    """The single per-episode shell registry is typed to MockShell."""
    annotation = task_module.__annotations__.get("_SHELL_REGISTRY")
    assert annotation is not None, "_SHELL_REGISTRY must carry a type annotation"
    assert "MockShell" in str(annotation), (
        f"_SHELL_REGISTRY must be typed to MockShell, got {annotation!r}"
    )
