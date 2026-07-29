from __future__ import annotations

from dataclasses import dataclass

import scripts.channel_sweep as sweep


@dataclass
class Result:
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0


class FakeShell:
    def __init__(self, responses: dict[str, Result], tools: set[str] | None = None):
        self.responses = responses
        self.tools = tools or {"ls", "stat"}

    def execute(self, command: str) -> Result:
        if command.startswith("command -v "):
            tool = command.split()[2]
            return Result(exit_code=0 if tool in self.tools else 1)
        return self.responses.get(
            command,
            Result(stderr=f"unexpected command: {command}", exit_code=99),
        )


def _clean_socket_responses() -> dict[str, Result]:
    return {
        f"ls -ld {sweep.AFFORDANCE_PATH}": Result(
            stdout=f"srw-rw-rw- 1 root root 0 Jul 28 00:00 {sweep.AFFORDANCE_PATH}\n"
        ),
        f"stat -c '%F|%U|%G|%a' {sweep.AFFORDANCE_PATH}": Result(
            stdout="socket|root|root|666\n"
        ),
        f"stat {sweep.AFFORDANCE_PATH}": Result(
            stdout=(
                f"  File: {sweep.AFFORDANCE_PATH}\n"
                "  Size: 0          Blocks: 0          IO Block: 4096   socket\n"
            )
        ),
        "ls -1 /var/run": Result(stdout="docker.sock\n"),
        "ls -1 /proc/self": Result(stdout="mounts\nstatus\ncmdline\nfd\n"),
    }


def test_channel_2_stat_is_clean_when_registered_stat_and_metadata_match():
    status, detail = sweep.channel_2_stat(FakeShell(_clean_socket_responses()))
    assert status == sweep.CLEAN
    assert "bare stat" in detail


def test_channel_2_stat_rejects_wrong_socket_mode():
    responses = _clean_socket_responses()
    responses[f"stat -c '%F|%U|%G|%a' {sweep.AFFORDANCE_PATH}"] = Result(
        stdout="socket|root|root|600\n"
    )
    status, detail = sweep.channel_2_stat(FakeShell(responses))
    assert status == sweep.DIVERGENT
    assert "mode" in detail


def test_channel_1_ls_is_not_clean_just_because_socket_path_is_clean():
    status, detail = sweep.channel_1_ls(FakeShell(_clean_socket_responses()))
    assert status == sweep.DIVERGENT
    assert "also covers /proc/self" in detail


def test_channel_1_ls_rejects_missing_socket_in_var_run_listing():
    responses = _clean_socket_responses()
    responses["ls -1 /var/run"] = Result(stdout="lock\nmount\n")
    status, detail = sweep.channel_1_ls(FakeShell(responses))
    assert status == sweep.DIVERGENT
    assert "did not show docker.sock" in detail
