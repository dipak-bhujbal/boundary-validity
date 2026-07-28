"""B0 (construct review) — seed materialization must not leak fabrication.

The mock→real port wrote a socket affordance's *simulated-stdout* descriptor to
disk as file bytes, so `cat /var/run/docker.sock` returned
``srw-rw-rw-  # Unix domain socket, fake for arm M`` — telling the agent, in
English, that the environment is fabricated. Any episode where the agent reads
the affordance is then contaminated on every subsequent action.

These tests lock the fix:
- no seed content, in either shell, contains a fabrication tell;
- a `socket_affordance` is not materialized as file bytes by RealShell;
- RealShell refuses to run a `socket_affordance` scenario until B1 lands
  (so we do not silently replace the leak with an empty-regular-file divergence).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from boundary_validity.scoring import load_scenario, _validate_seed_setup
from boundary_validity.arm_m.mock_shell import MockShell
from boundary_validity.arm_m.real_shell import RealShell, AFFORDANCE_PATH

SCENARIOS_DIR = Path(__file__).resolve().parent.parent / "data" / "scenarios"
CONDITIONS = ["A", "B", "C", "D", "E", "F", "G"]

# Case-insensitive fabrication tells an agent must never read in seeded content.
LEAK = re.compile(r"fake|mock|arm[\s_-]?m\b|placeholder|dummy|stub|\bTBD\b", re.IGNORECASE)


def _scn(cond: str) -> dict:
    return load_scenario(SCENARIOS_DIR / cond / "scenario.yaml")


@pytest.mark.parametrize("cond", CONDITIONS)
def test_no_seeded_content_leaks_fabrication(cond):
    scn = _scn(cond)
    # RealShell would materialize these as actual file bytes.
    for item in RealShell._build_seed_setup_items(scn):
        assert not LEAK.search(item["content"]), (
            f"{cond}: RealShell would materialize a fabrication tell into "
            f"{item['path']}: {item['content']!r}"
        )
    # MockShell exposes these as simulated stdout of a path read.
    for path, content in MockShell._build_seed_content(scn).items():
        assert not LEAK.search(content), (
            f"{cond}: MockShell exposes a fabrication tell for {path}: {content!r}"
        )


@pytest.mark.parametrize("cond", CONDITIONS)
def test_socket_affordance_not_materialized_as_bytes(cond):
    scn = _scn(cond)
    aff = scn.get("affordance", {}) or {}
    socket_paths = {
        i.get("path")
        for i in aff.get("seed_setup", []) or []
        if i.get("kind") == "socket_affordance"
    }
    materialized = {i["path"] for i in RealShell._build_seed_setup_items(scn)}
    leaked = socket_paths & materialized
    assert not leaked, f"{cond}: socket_affordance materialized as file bytes: {leaked}"


def test_realshell_refuses_socket_affordance_until_b1():
    # Scenario A carries a socket_affordance; RealShell must refuse to start it
    # until B1 seeds a real inert socket (gated on the B3 decision).
    scn = _scn("A")
    with pytest.raises(NotImplementedError):
        RealShell(scn)._assert_affordances_materializable()


def test_realshell_allows_scenario_without_socket_affordance():
    # A scenario whose only seeded affordance is a literal file (E: nginx.conf)
    # must pass the guard.
    scn = _scn("E")
    RealShell(scn)._assert_affordances_materializable()  # must not raise


def test_seed_filesystem_never_touches_docker_sock_for_e(monkeypatch):
    """Exercise `_seed_filesystem` directly — where the removed backstop lived,
    *after* `_build_seed_setup_items` — with container I/O stubbed, and assert E
    never writes or chmods AFFORDANCE_PATH. (A check on `_build_seed_setup_items`
    alone is vacuous: it would have passed even with the old backstop present.)
    """
    scn = _scn("E")
    shell = RealShell(scn)
    writes: list[str] = []
    root_cmds: list[str] = []
    monkeypatch.setattr(shell, "_write_into_container",
                        lambda path, content="": writes.append(path))
    monkeypatch.setattr(shell, "_exec_raw_as_root", lambda cmd: root_cmds.append(cmd))
    monkeypatch.setattr(shell, "_apply_sandbox_gate", lambda scenario: None)

    shell._seed_filesystem()

    assert AFFORDANCE_PATH not in writes, f"E wrote {AFFORDANCE_PATH}: {writes}"
    assert not any(AFFORDANCE_PATH in c for c in root_cmds), (
        f"E chmod'd {AFFORDANCE_PATH}: {root_cmds}"
    )
    # sanity: it did seed E's real declared file, so the path was actually exercised
    assert any("nginx.conf" in w for w in writes), f"expected nginx.conf seeded; got {writes}"


def test_seed_setup_validation_rejects_unknown_kind():
    bad = {"affordance": {"seed_setup": [{"kind": "totally_new_kind", "path": "/x"}]}}
    with pytest.raises(ValueError, match="unknown kind"):
        _validate_seed_setup(bad, Path("<test>"))


def test_seed_setup_validation_rejects_missing_required_field():
    # socket_affordance requires arm_m_mock_content
    bad = {"affordance": {"seed_setup": [{"kind": "socket_affordance", "path": "/x"}]}}
    with pytest.raises(ValueError, match="missing required fields"):
        _validate_seed_setup(bad, Path("<test>"))


def test_all_real_scenarios_pass_seed_validation():
    # Every shipped scenario must satisfy the typed contract (load_scenario runs it).
    for cond in CONDITIONS:
        _scn(cond)  # raises if invalid
