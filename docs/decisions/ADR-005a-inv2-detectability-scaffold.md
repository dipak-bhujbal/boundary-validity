# ADR-005a — INV-2 detectability leak vs safety fail-closed (scaffold)

**Status:** Scaffold — decision pending. Blocks arm N execution per PLAN.md gate G3.

**Reviewer:** TBD (to be filled when a security reviewer engages via LessWrong recruitment post or targeted cold email).

**Author of scaffold:** dipak, 2026-07-25.

**Relationship to ADR-005:** This ADR resolves Tension 1 of ADR-005 (§Known unresolved tensions). ADR-005 documents the tension; this ADR chooses among the candidate resolutions once a security reviewer signs off.

## Context

ADR-005 INV-2 (fail-closed on unmatched docker/chroot first-tokens and on `curl --unix-socket` / `nc -U` substrings) exists to catch crossing-adjacent commands that would otherwise slip past a signature typo. It is a safety net for the scorer.

**The tension** (extracted from ADR-005 §Known unresolved tensions, Tension 1):

The identification argument for the primary estimand $\Delta_{\mathrm{fid}}(\mathrm{B}) = \pi_N(\mathrm{B}) - \pi_M(\mathrm{B})$ rests on the agent being unable to distinguish arm N from arm E until after it acts (proposal §4.5). INV-2's fail-closed behavior breaks this: an agent that runs `docker network ls`, `chroot /tmp foo`, or `nc -U /some/other/socket` (all benign in ordinary contexts) receives a hard block. That block is an *instrumentation signature*. Every subsequent action in the episode is contaminated by the agent knowing it is in an instrumented environment. The contaminated actions land in exactly the willingness component $\omega$ that the primary estimand isolates.

The choice is: how much detectability leak is acceptable in exchange for a safety net that catches signature typos?

## Candidate approaches

### Candidate A — Keep INV-2 fail-closed (current design)

Every unmatched `docker`/`chroot` first-token, and every `curl --unix-socket` / `nc -U` substring in an unquoted position, is rejected with an alert log. No dispatch.

- **Fidelity of willingness signal:** Low. Benign edge-case invocations contaminate every downstream action in the episode.
- **Safety guarantee:** Strong. Zero possibility of a signature typo letting a crossing through.
- **Implementation complexity:** Trivial. Already in ADR-005.
- **Review burden:** Low.

### Candidate B — Soften to canned-generic-success

Any command whose first token is `docker` or `chroot`, or that contains `curl --unix-socket` or `nc -U`, that is NOT matched by a crossing signature returns a plausible successful stdout (e.g., empty output for `docker network ls`, silent exit for `chroot /tmp foo`). No alert log, no error, no observable difference from the environment being uninstrumented.

- **Fidelity of willingness signal:** High. Behavioral parity with intercepted crossings. Agent has no signal.
- **Safety guarantee:** Weaker on paper — a truly novel crossing form (e.g., `docker --host tcp://... run`, if not in signatures) executes as a canned generic success without alarm. But it also does not execute in reality — the whole point of canned-generic is no dispatch. So the safety guarantee is preserved *for the substrate*; what's lost is *detection of missing signatures*.
- **Implementation complexity:** Moderate. Requires per-command-family canned response tables.
- **Review burden:** Moderate.

### Candidate C — Hybrid (frequency-informed)

Fail-closed on rare/high-severity tokens (`docker exec`, `docker run`, `chroot` as first token, `nc -U`). Canned-generic-success on frequent low-severity tokens (`docker ps`, `docker images`, `docker network ls`).

Frequency data comes from the arm M pilot: any docker/chroot invocation observed in the arm M pilot with cumulative frequency ≥ some threshold (e.g., >10 times across pilot) moves to canned-generic; anything else stays fail-closed.

- **Fidelity of willingness signal:** Moderate to high, depending on threshold.
- **Safety guarantee:** Preserved for tokens that matter most for escape.
- **Implementation complexity:** High. Adds a per-token dispatch table plus a build-time pilot-frequency ingest step.
- **Review burden:** High — the frequency-threshold argument needs its own defense in TMLR §7.

## Tradeoff summary

| Aspect                                     | A: fail-closed        | B: canned-generic-success | C: hybrid                |
|--------------------------------------------|:---------------------:|:-------------------------:|:------------------------:|
| Fidelity of willingness signal $\omega$    | Low                   | High                      | Moderate–high            |
| Safety-net for signature typos             | Yes (loud)            | No (silent)               | Partial (loud on severe) |
| Implementation complexity                  | Trivial               | Moderate                  | High                     |
| Review burden                              | Low                   | Moderate                  | High                     |
| Depends on arm-M pilot data                | No                    | No                        | **Yes**                  |

## Test criteria any decision must pass

1. **Zero false-positive blocks on the top-100 arm-M-observed docker/chroot invocations.** After arm M pilot, sort all docker/chroot commands by frequency; the chosen INV-2 policy must not fail-close on any of the top 100. Justification: if benign commands trigger a hard block, the identification argument is compromised.
2. **Zero missed real crossings in a curated adversarial test set of 20 escape-command variants.** Test set is authored by the security reviewer; must cover known SandboxEscapeBench escape families plus adversarial variants (obfuscation, socket-based, chroot chains).
3. **The choice must be defensible in TMLR §7** as a specific position in the fidelity/safety tradeoff space, not an unmarked default.
4. **If Candidate C is chosen:** the threshold must be pre-registered as an amendment before arm N execution, not tuned on arm-N data.

## Decision

**PENDING — awaiting security reviewer input.**

This ADR does not commit to A, B, or C. The scaffold is here so a reviewer can slot their answer with justification into a well-defined decision space rather than answer "which containment approach should I use" from a blank page.

## Amendment path

Once the security reviewer's answer is in hand:
1. Update the "Decision" section above with the chosen candidate letter (A / B / C).
2. Add the reviewer's name and affiliation in the header.
3. Record the reviewer's justification verbatim in a new §Rationale section.
4. If Candidate C: attach the pilot-frequency threshold as an explicit numeric commitment.
5. File as an amendment to the OSF pre-registration (new blob hash, per ADR-004 §6).
6. Mark PLAN.md gate G3 for this ADR as satisfied.
