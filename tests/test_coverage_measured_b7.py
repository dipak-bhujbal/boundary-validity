"""B7 (construct review §5.3) — the coverage guard must be able to fire.

`coverage_rate` returned the literal `1.0` and `unparsed_commands` returned `[]`,
so `coverage_ok = coverage >= 0.80` was unconditionally true and no arm-M-real
episode could ever be flagged. The "retained guard" ADR-007:60 promises did not
exist.

The construct stake, not just hygiene: the justification for the real-shell switch
is that idiom-coverage bias is eliminated *by construction*. Hardcoding the metric
eliminates it *by stipulation* and destroys the evidence for the claim.

These tests therefore assert both directions — the guard reads ~1.0 on a healthy
substrate (so the claim is observed, not assumed) AND drops below the gate when the
substrate misbehaves (so it can actually fire). A test of only the first direction
would have passed against the old hardcoded implementation.

No container required: substrate behavior is injected at _exec_raw.
"""

from __future__ import annotations

import subprocess

import pytest

from boundary_validity.arm_m.real_shell import RealShell, ShellResult

SCENARIO = {"id": "A", "affordance": {"seed_setup": []}}


def _shell(monkeypatch, responder, container_running=False):
    s = RealShell(SCENARIO)
    s._started = True  # skip container start; we inject substrate behavior below
    monkeypatch.setattr(s, "_exec_raw", responder)
    # Liveness ADJUDICATES the substrate-failure call (stderr markers only screen).
    monkeypatch.setattr(s, "_container_is_running", lambda: container_running)
    return s


def test_healthy_substrate_reads_full_coverage(monkeypatch):
    s = _shell(monkeypatch, lambda cmd: ShellResult(stdout="ok\n", exit_code=0))
    for cmd in ("ls", "stat /x", "cat /y"):
        s.execute(cmd)
    assert s.coverage_rate == 1.0
    assert s.unparsed_commands == []
    assert s.handled_commands == ["ls", "stat /x", "cat /y"]


def test_in_container_failures_still_count_as_handled(monkeypatch):
    """command-not-found and permission-denied are REAL substrate responses and
    part of what the study measures. Counting them as coverage misses would make
    the guard fire on exactly the observations we want to collect."""
    s = _shell(monkeypatch, lambda cmd: ShellResult(
        stderr="bash: docker: command not found\n", exit_code=127))
    s.execute("docker ps")
    s.execute("cat /root/secret")
    assert s.coverage_rate == 1.0
    assert s.unparsed_commands == []


def test_substrate_failure_drops_coverage_below_gate(monkeypatch):
    """The direction the old implementation could not express. A dead container
    must pull coverage under the 0.80 gate so the episode is flagged."""
    calls = {"n": 0}

    def responder(cmd):
        calls["n"] += 1
        if calls["n"] == 1:
            return ShellResult(stdout="ok\n", exit_code=0)
        return ShellResult(
            stderr="Error response from daemon: container is not running\n",
            exit_code=1)

    s = _shell(monkeypatch, responder, container_running=False)
    for cmd in ("ls", "stat /x", "cat /y", "id", "mount"):
        s.execute(cmd)

    assert s.coverage_rate == pytest.approx(0.2)
    assert s.coverage_rate < 0.80, "guard must be able to fire"
    assert len(s.unparsed_commands) == 4


def test_exec_exception_is_recorded_as_unparsed(monkeypatch):
    """An exec timeout raises rather than returning; it must be counted, not
    propagated as an episode crash."""
    def responder(cmd):
        raise subprocess.TimeoutExpired(cmd="docker exec", timeout=30)

    s = _shell(monkeypatch, responder)
    r = s.execute("sleep 999")
    assert r.exit_code == 127
    assert s.unparsed_commands == ["sleep 999"]
    assert s.coverage_rate == 0.0


def test_coverage_is_not_hardcoded():
    """Direct anti-regression for the exact defect: a shell with commands counted
    but none recorded as handled must NOT report 1.0."""
    s = RealShell(SCENARIO)
    s.commands_total = 10
    assert s.coverage_rate != 1.0, "coverage_rate is stipulated, not measured"
    assert s.coverage_rate == 0.0


def test_empty_episode_reads_one():
    """Degenerate case: no commands means no evidence of a miss, not a miss."""
    assert RealShell(SCENARIO).coverage_rate == 1.0


def test_inner_docker_daemon_error_counts_as_handled(monkeypatch):
    """Regression for the B2 collision (codex-2 cross-review).

    Once B2 restores `docker` INSIDE the container, an in-container `docker ps`
    against an absent daemon emits "Cannot connect to the Docker daemon" — the same
    string an outer delivery failure produces. bash executed that command perfectly,
    and its response is precisely what the study measures, so it MUST count as
    handled. Stderr markers screen; container liveness adjudicates.
    """
    s = _shell(
        monkeypatch,
        lambda cmd: ShellResult(
            stderr="Cannot connect to the Docker daemon at unix:///var/run/docker.sock.\n",
            exit_code=1),
        container_running=True,   # the container is alive; only the inner tool failed
    )
    s.execute("docker ps")
    assert s.unparsed_commands == [], "inner daemon error must not count as a coverage miss"
    assert s.coverage_rate == 1.0


def test_same_stderr_counts_as_unparsed_when_container_is_gone(monkeypatch):
    """The discriminating half: identical stderr, dead container -> unparsed. Proves
    the classifier keys on liveness rather than on the marker text."""
    s = _shell(
        monkeypatch,
        lambda cmd: ShellResult(
            stderr="Error response from daemon: container is not running\n",
            exit_code=1),
        container_running=False,
    )
    s.execute("docker ps")
    assert s.unparsed_commands == ["docker ps"]
    assert s.coverage_rate == 0.0


def test_successful_command_is_never_a_substrate_failure(monkeypatch):
    """exit 0 short-circuits before any marker check — a succeeding command whose
    output happens to quote a daemon error must stay handled."""
    s = _shell(
        monkeypatch,
        lambda cmd: ShellResult(
            stdout="Error response from daemon: ...\n", exit_code=0),
        container_running=False,
    )
    s.execute("cat /work/logs/daemon-errors.txt")
    assert s.unparsed_commands == []


# ---------------------------------------------------------------------------
# B7 homonym guard (construct-review check §3, finding 6).
#
# `coverage_rate` names two different quantities depending on substrate:
#   mock substrate       -> idiom parse rate (0.85-0.88, moves with idiom coverage)
#   real-shell substrate -> container delivery rate (~1.0 by construction)
# The review found them tabulated under one name in a document we called
# corrigendum-grade. These tests make the distinction machine-checkable so a
# report cannot pool them by accident.
# ---------------------------------------------------------------------------


def test_substrates_declare_distinct_coverage_metric_kinds():
    """The two shells must not claim to measure the same thing."""
    from boundary_validity.arm_m.mock_shell import MockShell

    assert MockShell.COVERAGE_METRIC_KIND == "idiom_parse"
    assert RealShell.COVERAGE_METRIC_KIND == "container_delivery"
    assert MockShell.COVERAGE_METRIC_KIND != RealShell.COVERAGE_METRIC_KIND


def test_real_shell_exposes_delivery_rate_as_the_honest_name(monkeypatch):
    """`delivery_rate` is the preferred name and must agree with the alias."""
    s = _shell(monkeypatch, lambda cmd: ShellResult(stdout="ok\n", exit_code=0),
               container_running=True)
    s.execute("echo ok")
    assert s.delivery_rate == s.coverage_rate


def test_scorer_emits_coverage_metric_kind_next_to_coverage_rate():
    """A report reading `coverage_rate` must always be able to see which
    quantity it got. Missing the field is the failure mode this guards."""
    import inspect

    from boundary_validity.arm_m import task as task_module

    src = inspect.getsource(task_module)
    assert '"coverage_metric_kind"' in src, (
        "task.py must emit coverage_metric_kind alongside coverage_rate so the "
        "mock idiom-parse rate and the real-shell delivery rate are never pooled."
    )
    # Default backend is the mock, so the default kind must be the mock's.
    assert '"idiom_parse"' in src
