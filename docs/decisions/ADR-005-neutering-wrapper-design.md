# ADR-005: Neutering-wrapper design specification

**Status:** Proposed — outline only. Full spec + implementation deferred to week 6 per PLAN.md.
**Date:** 2026-07-25
**Deciders:** Dipak Bhujbal
**Related:** ADR-001, ADR-003

## Context

Arm N places the agent in a real container with a real affordance surface, but no exploit ever executes. This is achieved by the neutering wrapper: a layer that sits between the agent's shell tool call and the container's actual shell, matches commands against the per-scenario `crossing_signatures`, and returns a canned response *without dispatching* to the shell.

This ADR is written now (week 1) rather than at week 6 because the design principles are load-bearing for two things happening earlier:

- The AUP pre-registration emails to AWS and GCP (`docs/communications/aup-pre-registration/`) assert intercept-and-fake behavior; that assertion must be traceable to a named ADR.
- ADR-003's command contract v0 references `neutering_hook` names on each crossing signature; those names must map to a defined interface.

Full implementation waits until the arm N harness is scaffolded (week 10–11), at which point this ADR is revised or accepted with a linked pull-request.

## Design principles (locked)

1. **Intercept-and-fake, never attempt-and-hope.** The wrapper matches on command *signature* and returns a canned response. The underlying command is never dispatched to a real shell, ever, for any reason. Failure to match is a fail-closed condition, not a fail-open one: an unrecognised command signature that appears crossing-adjacent (e.g., a novel form of `docker` invocation) blocks execution and logs an alert.
2. **Single source of truth with the scorer.** The wrapper loads the same per-condition `scenario.yaml` (ADR-003 schema) the scorer loads. A unit test enforces byte-identical regex sets between the two loaders — the test fails the build if they diverge.
3. **Canned responses are recorded from arm M**, not hand-written where possible. This preserves the property that arm M and arm N differ only in substrate, not in what the agent observes when it runs an exploit.
4. **Every interception is logged with `neutered=true`**, the matched regex, and the hook name. The trajectory contains complete evidence that the wrapper fired.
5. **No side effects on the container filesystem or network.** The wrapper does not write files, mount volumes, or open sockets in response to a matched command. Only stdout/stderr/exit-code are returned.

## Interface (locked)

```python
class NeuteringWrapper:
    def __init__(self, scenario: Scenario, canned_responses: dict[str, CannedResponse]):
        ...

    def intercept(self, command: str) -> InterceptResult:
        """
        Called by the arm-N harness before dispatching `command` to the container shell.

        Returns InterceptResult with:
          - matched: True iff `command` matches any crossing_signature in scenario
          - hook_name: the neutering_hook name from the matched signature (None if !matched)
          - canned_response: the pre-recorded stdout/stderr/exit_code to return, or None
          - matched_regex: the regex string that matched, for logging (None if !matched)

        If matched=True, the caller MUST return canned_response to the agent
        WITHOUT dispatching `command` to the shell. Caller behavior is enforced
        by an assertion in the harness main loop.

        If matched=False, the caller may dispatch `command` to the shell normally.
        """
```

## Safety invariants (must pass before any arm N execution — G3)

Unit tests that block the arm-N build:

- **INV-1** (regex parity): the set of crossing-signature regexes loaded by the wrapper is byte-identical to the set loaded by the scorer, for every scenario in `data/scenarios/{A..G}/`.
- **INV-2** (fail-closed, narrowed 2026-07-25 after review): a command is rejected by the wrapper with an alert log, and not passed through, if EITHER (a) its first token (post-normalization) matches `^(docker|chroot)$` and no crossing signature matched, OR (b) the command contains the specific substrings `curl --unix-socket` or `nc -U` in an unquoted position and no crossing signature matched. The earlier version's `{exec, socket}` substring blocks were removed: `exec` is a common bash builtin and `socket` appears in benign `/proc` and `/sys` paths, so blocking on either substring would fail-close on ordinary commands AND make the neutering trivially agent-detectable (the exact failure mode §8 of the proposal calls out). The narrowed form preserves the safety intent — catching the known crossing-adjacent command families that could slip past a signature typo — without the collateral fail-closes.
- **INV-3** (no dispatch on match): a mock harness invocation asserts the wrapper's `intercept()` return with `matched=True` causes zero shell dispatches. Tested via an instrumented shell that counts calls.
- **INV-4** (no side effects): intercepted commands produce zero writes to `/var/log/*`, zero opens of `/dev/net/tun`, zero mounts, zero container-network egress. Verified via `strace` on the wrapper's PID during a fixture run.
- **INV-5** (canned response provenance): every canned response has a recorded source — either a hash-linked arm M trajectory or a hand-written response with a signed rationale. No canned response is generated at runtime.

## Alternatives considered (to be expanded at week 6)

- **eBPF-based syscall interception.** Rejected for scope: adds significant complexity and requires kernel version alignment across the panel. The wrapper operates at the shell-tool boundary, one level up.
- **Container escape monitoring only (no interception).** Rejected because it violates the "no live escape" property that the AUP emails, ADR-001, and the study's own containment story rest on.
- **LLM-based command classification.** Rejected: non-deterministic, unauditable, and reintroduces the exact silent-failure mode ADR-003 is written to prevent.

## What's deferred to week 6

- Specific canned-response corpus: what the wrapper returns for each hook name. Recorded from arm M runs during weeks 5–6.
- Concrete cloud-host runtime story (c8i vs GCP; ADR-006).
- Network egress-alerting layer specification.
- Load-testing and concurrency behavior of the wrapper under the arm-N sample plan.

## Consequences

**Positive:**
- AUP emails have a citable ADR for their intercept-and-fake claim.
- Design principles pinned now cannot be silently softened at implementation time.
- The safety invariants become the arm N build's acceptance criteria before any live compute.

**Negative:**
- Committing to intercept-and-fake before writing code means the harness architecture is constrained by this ADR, not chosen freely at week 10. Judged an acceptable price given the safety story.
