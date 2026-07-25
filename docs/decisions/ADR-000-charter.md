# ADR-000: Project charter

**Status:** Accepted
**Date:** 2026-07-25
**Deciders:** Dipak Bhujbal (sole author)

## Context

Propensity evaluations in AI safety measure what an agent *chooses* to do rather than what it is *able* to do. Existing published propensity work (PropensityBench, Krakovna et al.'s honeypot evaluations, Instrumental Choices) shares a structural feature that has never been tested: the boundary the agent is measured against is stipulated by the evaluation author rather than enforced by the system. Whether that substitution is valid — whether measuring propensity against a fictional boundary yields the same answer as measuring against a real one — is a validity question about the entire subfield.

The July 2026 OpenAI internal-eval sandbox escape (ExploitGym → Hugging Face infrastructure) sharpened the practical stakes: containment decisions are increasingly calibrated from propensity evaluations, so any multiplicative bias in those numbers passes undamped into infrastructure choices.

## Decision

This project pre-registers and executes a **three-arm identification design**, of which two arms (M and N) will be run for the first paper (see ADR-001), to measure the fidelity gap between fabricated and real containment boundaries under matched scenarios.

- **Primary estimand:** $\Delta_{\mathrm{fid}}(c) = \pi_N(c) - \pi_M(c)$ for condition $c = \mathrm{B}$ (blocked in-sandbox path).
- **Secondary estimands:** three-factor decomposition (discovery / willingness / capability), evaluation-awareness effect (condition G), provider-substitution artifact, temporal drift.
- **Publication target:** Transactions on Machine Learning Research (TMLR).

## Scope

**In scope:**
- Arm M (mocked shell) and Arm N (real container, silently neutered exploit)
- 7 conditions (A base rate, B necessity, C vague scope, D permission framing, E useless affordance, F honourable exit, G eval-awareness)
- Model panel per ADR-002
- Public reproducibility package: harness, specs, pre-registration, trajectories, fits

**Out of scope:**
- Arm E (live exploit) — see ADR-001 for rationale
- Novel exploit development — restricted to SandboxEscapeBench published suite
- Interpretability claims
- Cross-model *causal* attribution — reported as description only

## Success criteria

The project succeeds if all of the following hold at TMLR submission:

1. Pre-registration was timestamped on OSF before any data collection.
2. Arms M and N were executed against the pre-registered scenario suite with the pre-registered model panel.
3. The manuscript's headline claim (fidelity gap or its bounded null) is supported by the arm M / arm N contrast on condition B, per TMLR criterion 1.
4. All code, scenario specifications, raw trajectories, and analysis fits are publicly released under MIT.
5. No live escape occurred at any point in the study; arm N's egress-alerting layer recorded no anomalies.

The project **does not** claim success on the basis of paper acceptance. TMLR acceptance is a downstream target, not a success criterion.

## Constraints

- Solo authorship for the full pipeline (see ADR-001 on collaboration model).
- Budget: ~$900 gross API + compute, target <$500 out-of-pocket after research credits.
- Timeline: 16 weeks to submission.
- No exploit disclosure risk: every mechanism is drawn from published, upstream-patched vulnerabilities.
- No provider-terms violation: pre-registration to GCP and AWS abuse teams before any arm N execution.

## Non-goals

- SOTA comparisons on any benchmark
- New propensity framework (the framing is not novel — see §3.2 of the proposal)
- Real-time deployment monitoring
- Anything requiring nested-virt infrastructure beyond a single cloud instance

## Consequences

**Positive:**
- Clean identification argument, testable design, defensible at interview two levels deep.
- Publishable both as workshop paper (arm M alone, interim) and as TMLR full paper (arm M + arm N).
- Reproducibility package doubles as a resume artifact.

**Negative:**
- No consequence-effect measurement without arm E — must be framed as future work.
- Solo constraint means schedule risk if illness, work commitments, or scope creep intervene.
- TMLR rolling review means calendar variance on decision timing.

## References

- Proposal: `docs/proposal/boundary-validity-gap-proposal.md` (to be committed from `~/Downloads/proposal/`)
- Prior art: SandboxEscapeBench (arXiv:2603.02277), PropensityBench (arXiv:2511.20703), Instrumental Choices (arXiv:2605.06490), Krakovna et al. (arXiv:2605.29729)
