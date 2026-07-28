# ADR-008 — G3 remediation roadmap (tracking checklist)

**Status:** Accepted as a tracking checklist. **Arm N remains blocked.**
**Source:** external G3 arm-N containment security review, 2026-07-28
([`../reviews/2026-07-28-G3-armN-containment-review.md`](../reviews/2026-07-28-G3-armN-containment-review.md)).
**Date:** 2026-07-28

## What this document is — and is NOT

This is a **remediation roadmap**: a scoped, tracked checklist of the conditions the
G3 review named, so the work is enumerated rather than vague. Each item points at the
review section that raised it.

**This is not the containment specification, and adopting it does not mean the design
is specified.** The G3 review returned FAIL partly *because* the neutering wrapper and
arm-N substrate are not yet designed or built. Writing the reviewer's list down here
does not close that gap. When C1–C7 are actually implemented, the design and the reason
each invariant is load-bearing must be **owned and defensible by the author** — a
security re-review is not "forwarding a design lifted from the last review." Containment
errors hide from anyone who does not deeply understand them; that is the whole reason
arm N requires a human security reviewer. This checklist tracks *what* to build. It is
deliberately silent on *how*, because the how is real engineering that must be done and
understood, not transcribed.

## Gate status

**G3 = FAIL** on three independent grounds (review §Verdict): the neutering wrapper is
unimplemented (F1); a regex denylist in front of a real shell is not a containment
boundary — 18/20 adversarial variants reached a real shell in testing (F2); G3's own
preconditions are unmet (F3). **No arm-N execution, no real-shell model episodes, until
G3 turns green.**

The reviewer's central correction (review §1), recorded here because it governs all of
C1–C8: **arm N must be safe on the assumption that the wrapper fails completely and every
command executes for real.** Safety moves into the substrate; the wrapper becomes a
fidelity device, not the boundary.

## Blocking — arm N cannot run until all land (security re-review triggers on a diff landing C1–C7)

| # | Item | Review § |
|:--|:--|:--|
| C1 | Specify arm N's substrate in an ADR: daemon liveness, capability set, network posture, blast radius. Recommended: sacrificial nested daemon in a disposable VM with no credentials and no route out. Blocks C4, C5. | §2 |
| C2 | Adopt the "safe under total wrapper failure" reframe as a design principle superseding ADR-005 principle 1; resolve the locked-section contradiction (never-dispatch vs unmatched-dispatches); re-check the AWS/GCP AUP emails against the amended text. | §1, §1.1 |
| C3 | Make interception structural: the wrapper owns the shell handle; the raw shell is unreachable from the harness. Enforce by raised exception, never `assert` (stripped under `python -O`). | §1.2 |
| C4 | Harden the container (`--cap-drop=ALL`, `--security-opt=no-new-privileges`, `--read-only`, `--pids-limit`, `--memory`, `--cpus`, `--userns`) and add a runtime `docker inspect` + `/proc/self/status` assertion test to CI (not opt-in). | §7 |
| C5 | Implement ADR-006 Candidate C (pre-gate fuzz + in-flight monitor) with six amendments: corrected failure criterion, mandatory positive-control canary, concurrency ≥2× production, extended post-teardown monitoring window with forced `docker rm -f`, credential isolation, DNS control/sinkhole. (~$80 infra + a chosen cloud host — gated on estimate + approval.) | §6 |
| C6 | Invert INV-1: the wrapper's matched set must be a tested **superset** of the scorer's (`scorer_matches(cmd) ⟹ wrapper_matches(cmd)`); wrapper matches on a shell-parsed token stream, not the raw string. | §5 |
| C7 | Adopt the 20-variant adversarial set (+3 controls, +5 addendum variants) as a CI regression fixture; require full pass; record in ADR-005a that a passing fixture is **not** a containment proof. | §3 |

## Decision, sequenced after C1–C3 (record now, do not implement before the substrate is safe)

| # | Item | Review § |
|:--|:--|:--|
| C8 | INV-2 = **Candidate B** (canned-generic-success), with four conditions: out-of-band (not agent-observable) logging, timing parity, response entropy, full `(stdout, stderr, exit_code, latency)` parity. Only after C1–C3, because choosing B today would remove the one loud signal while the wrapper is still the boundary. | §4 |

## Non-blocking fixes (correctness; do not move G3 toward green)

| # | Item | Status |
|:--|:--|:--|
| C9 | `_assert_no_host_socket` was a no-op `return`; implement it to inspect the constructed argv and raise. | **Done — this cleanup** |
| C10 | `test_runs_as_nonroot` passed under `--user 0:0`; the `--network` check was two independent substrings. Assert on constructed args. | **Done — this cleanup** |
| C15 | `test_no_host_socket_mount` grep `" -v "` (spaces) never matched the argv form `"-v", "/:/host"`; assert on constructed args, and add CI so safety tests run on every commit. | **Partly done — arg-list assertions landed; CI still to add** |
| C11 | `shlex.quote` the `kind` interpolation at `real_shell.py` sandbox-gate else-branch. | Open |
| C12 | Wrap `start()`/`stop()` in `try/finally` with `docker rm -f`; do not rely on the client-side `subprocess` timeout (orphans survive it). | Open |
| C13 | Reopen independent-review §2.7: the pipe fix and the `^` anchor cancel out; credential extraction still scores `X=0`. Scoring issue, not containment. | Open |
| C14 | Test fixture scenario shape (`seed_files`, string `crossing_signatures`) does not match the real schema (`affordance.seed_setup`, list-of-dicts with `regex`). | Open |
| C16 | Pin `DOCKER_HOST` / Docker context explicitly; pass a scrubbed `env=` to every `subprocess.run` (the CLI currently inherits the harness's provider API keys). | Open |
| C17 | Reconcile the nested-virtualisation claim in the AWS AUP draft against the proposal before it reaches a provider. | Open |

## Recorded positive result (not a C-item)

The reviewer confirmed **arm M's `RealShell` posture holds at runtime** (`NetworkMode: none`,
`CapEff: 0`, no mounts, `docker.sock` an inert regular file). Static enforcement for
arm M has been upgraded to runtime proof; this should be recorded in ADR-007. It is the
existence proof that C1–C7 is achievable — arm M already enforces containment below the
shell, which is exactly where arm N's must live.

## Re-review

Security re-review triggers on a diff landing **C1–C7**. C8 is a decision recorded here
and may be implemented only after C1–C3. Nothing in C1–C8 requires changing what the
study measures.
