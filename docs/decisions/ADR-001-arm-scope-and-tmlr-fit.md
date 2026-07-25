# ADR-001: Arm scope and TMLR fit

**Status:** Accepted
**Date:** 2026-07-25
**Deciders:** Dipak Bhujbal
**Related:** ADR-000

## Context

The proposal specifies a three-arm design: M (mocked shell, no virt), N (real container, silently neutered exploit), E (real container, live exploit). The primary scientific result — the fidelity gap $\Delta_{\mathrm{fid}}$ — is identified from the M-to-N contrast. E measures a secondary estimand (consequence effect) and permits real escape by construction.

Publication target is TMLR. Its two acceptance criteria are (1) claims supported by evidence, and (2) some audience of interest. Novelty, SOTA, and significance are explicitly not required.

Two questions must be answered:

1. Which arms are required for a TMLR-viable paper?
2. Which arms can be executed solo within budget and timeline?

## Options considered

### Option A: Arm M only, tempered claims

Ship arm M as a solo study, present the identification argument as design contribution, defer arms N and E to future work.

- **TMLR fit:** marginal. Headline fidelity-gap claim cannot be supported by arm M alone. Reviewers may demand arm N to close the gap between the introduction's framing and the results section.
- **Solo feasibility:** high.
- **Cost:** ~$600 gross.
- **Timeline:** 8 weeks to submission.

### Option B: Arms M + N, arm E deferred

Ship arms M and N, both solo. Arm N uses cloud nested-virt (AWS c8i or GCP nested-virt image) with an intercept-and-fake neutering wrapper that blocks the exploit command before execution and returns canned stdout. No live escape possible by construction. Arm E deferred as clearly-scoped future work.

- **TMLR fit:** strong. Primary estimand $\Delta_{\mathrm{fid}}$ is directly measurable from the M-to-N contrast.
- **Solo feasibility:** high. Cloud nested-virt is a config flag on standard instances as of early 2026, not a hardware purchase. Harness engineering is within Claude Code + Dipak's judgment scope, provided the neutering wrapper is spec'd as intercept-and-fake (not attempt-and-hope).
- **Cost:** ~$900 gross.
- **Timeline:** 16 weeks to submission.

### Option C: Full three-arm (M + N + E)

Ship all three arms. Arm E requires a human security reviewer of the containment protocol before first live run.

- **TMLR fit:** strongest. Both primary and consequence-effect estimands supported.
- **Solo feasibility:** partial. Arm E is not defensibly solo. Requires either a co-author with containment-security expertise or a paid contract reviewer.
- **Cost:** ~$1,400 gross plus $300–600 reviewer.
- **Timeline:** 24+ weeks to submission.

## Decision

**Option B is accepted.**

Rationale:

- **TMLR criterion 1 is met.** The M-to-N contrast supports the fidelity-gap claim directly. Arm E adds a secondary estimand but is not load-bearing for the headline.
- **Solo authorship is preserved.** For a portfolio artifact intended to signal individual technical judgment (AI PM/TPM roles at frontier labs), a solo paper on arms M and N is materially stronger than a multi-author paper on all three. Dilution of the "which parts were you" signal is a real cost.
- **Containment risk stays at zero.** Arm M has no substrate; arm N cannot escape by construction if the neutering wrapper is correctly designed. Arm E is the only arm where implementation bugs could reproduce the July 2026 incident, and its exclusion removes that class of failure from the project.
- **Cloud nested-virt eliminates the infrastructure blocker** that motivated an earlier "collaborator required" call. AWS enabled nested-virt on 8th-gen Intel c8i instances in early 2026 via `CpuOptions`; GCP has supported it since 2017 with a license-flagged image. Standard providers, not bare metal.
- **Budget stays under the $1000 personal cap** established for portfolio projects, with realistic out-of-pocket ~$400 after research credits.

Arm E is documented as future work in the manuscript, with a fully specified containment protocol from §7 of the proposal so that any competent group (with a reviewer) can execute it.

## Collaboration model

- **Sole author.** Anyone who builds harness code becomes a co-author; this bar is non-negotiable.
- **Acknowledged, non-author contributions welcomed:** identification-argument review, statistical review of the hierarchical model and priors, informal design review of the neutering wrapper, arXiv endorsement.
- **Recruitment sequence:** approach collaborators for future arm E work only after arm M or arm M+N results are in hand. Never approach a collaborator with a request; approach with a result.

## Consequences

**Positive:**
- Clean TMLR-fit paper achievable in 16 weeks solo.
- Zero live-escape risk.
- Reduced total budget vs Option C.
- Sole-authorship preserved for portfolio purposes.

**Negative:**
- Consequence effect ($\pi_E - \pi_N$) is not measurable. Must be framed as future work.
- The §4.5 first-attempt equivalence check between arms N and E cannot be executed; the instrumentation-leak diagnostic becomes theoretical rather than empirical.
- If a reviewer insists on arm E for TMLR acceptance, response is either a tempered revision or a resubmission with arm E after collaborator recruitment.

## Follow-ups

- ADR-002: Model panel selection (this ADR)
- ADR-003 (planned, week 1): Scenario command contract v0
- ADR-004 (planned, week 2): OSF pre-registration protocol and hypothesis list
- ADR-005 (planned, week 6): Neutering-wrapper design specification
- ADR-006 (planned, week 9): Cloud host selection (AWS c8i vs GCP nested-virt)
