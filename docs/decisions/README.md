# Architecture Decision Records

Every material decision in this project gets an ADR. ADRs are append-only: to change a past decision, write a new ADR that supersedes it and mark the old one Superseded.

## Status legend

- **Accepted** — decision is in force
- **Proposed** — under review, not in force
- **Superseded** — replaced by a later ADR (linked)
- **Deprecated** — no longer relevant

## Index

| ID | Title | Status |
|:--|:--|:--|
| [ADR-000](ADR-000-charter.md) | Project charter | Accepted |
| [ADR-001](ADR-001-arm-scope-and-tmlr-fit.md) | Arm scope and TMLR fit | Accepted |
| [ADR-002](ADR-002-panel-selection.md) | Model panel selection | Accepted |
| [ADR-003](ADR-003-command-contract-v0.md) | Scoring command contract v0 | Proposed (revised at pilot κ gate) |
| [ADR-004](ADR-004-osf-preregistration-protocol.md) | OSF pre-registration protocol | Proposed (locks at end of week 2) |
| [ADR-005](ADR-005-neutering-wrapper-design.md) | Neutering-wrapper design (principles + interface) | Proposed — full spec at week 6 |
| [ADR-005a](ADR-005a-inv2-detectability-scaffold.md) | INV-2 detectability leak vs safety fail-closed (scaffold) | Scaffold — decision pending (blocks arm N / G3) |
| [ADR-006](ADR-006-egress-under-load-scaffold.md) | Egress-under-load verification for arm N (scaffold) | Scaffold — decision pending (blocks arm N / G3) |
| [ADR-007](ADR-007-arm-m-real-shell.md) | Arm M substrate — mock shell to real containerized shell | Proposed — blocks on OSF amendment |

## Gate reviews

- **G3 (arm-N containment) — 2026-07-28: FAIL.** External security review returned FAIL on three independent grounds (the neutering wrapper is unimplemented; a regex denylist in front of a real shell is not a containment boundary — 18/20 adversarial variants reached a real shell in testing; G3's own preconditions are unmet). **Arm N remains blocked; no arm-N execution.** Full review: [`../reviews/2026-07-28-G3-armN-containment-review.md`](../reviews/2026-07-28-G3-armN-containment-review.md).
