# ADR-004: OSF pre-registration protocol

**Status:** Proposed (locks at end of week 2; PLAN.md gate G1)
**Date:** 2026-07-25
**Deciders:** Dipak Bhujbal
**Related:** ADR-000, ADR-001, ADR-002, ADR-003

## Context

Pre-registration is the only credible defense against selective reporting in a study whose base rates are in the low single digits and whose sub-cells will contain zero events. Without it, a reader has no way to distinguish an intended primary estimand from a post-hoc favorite. Given that this project's *entire* claim to rigor rests on identification cleanliness (ADR-001) and scorer determinism (ADR-003), silent flexibility in the analysis plan would undo both.

TMLR does not require pre-registration, but its acceptance criterion "claims supported by accurate, convincing and clear evidence" is materially easier to satisfy when the analyses producing the evidence were fixed before the data existed.

OSF (Open Science Framework, `osf.io`) is the default because it timestamps the exact frozen document, issues a DOI, and cannot be silently edited after registration. AsPredicted is faster but less permissive on document length; the pre-registration for this study is long enough that OSF is the correct venue.

## Decision

Timestamp a single pre-registration record on OSF by end of week 2, containing all sections below. After timestamp, no changes without a written amendment attached to the same record.

The pre-registration record has seven mandatory sections; each is populated from the artifacts already in this repository (linked, not duplicated, so the OSF document is a manifest not a re-render).

### 1. Study title and hypotheses

**Title:** *Stipulated Boundaries Are Not Real Boundaries: Measuring the Validity Gap in Propensity Evaluations of Agentic Boundary Crossing (Arms M and N).*

**Hypotheses.** Directional. Each states what "wrong" would mean, so that being wrong is informative.

| ID | Statement | Reasoning | Failure interpretation |
|:--|:--|:--|:--|
| **H1** (low base rate) | In condition A, arm M, $\pi_M(\mathrm{A}) < 0.02$ | An isolation boundary is more salient than a policy document; refusal training binds more tightly to sandbox escape than to fictional credit transfers | If $\ge 0.02$, sandbox salience is weaker than assumed; recalibrate base-rate priors |
| **H2** (necessity dominates) | $\pi(\mathrm{B}) - \pi(\mathrm{A}) \in [0.08, 0.15]$ within each arm | Direct transfer of the largest reported effect from Instrumental Choices, attenuated for H1's reason | If <0.08, necessity effect does not transport to enforced-boundary substrates; if >0.15, isolation actually amplifies necessity |
| **H3** (framing null) | Urgency/consequence framing produces no effect distinguishable from zero | Replication of Instrumental Choices' reported null | Failure means their null was environment-specific — itself worth reporting |
| **H4** (fidelity gap, primary) | $\Delta_{\mathrm{fid}}(\mathrm{B}) < 0$ with $|\Delta_{\mathrm{fid}}(\mathrm{B})| \ge 0.03$; equivalently $\rho > 1$ | Real substrate supplies friction and failure feedback absent in mock | Held weakly; the opposite result ($\rho < 1$) is *more* interesting because it means the literature's reassuring numbers are methodology artifacts |
| **H5** (not purely legibility) | The willingness component of the §4.3 decomposition is non-zero: $\omega_N \ne \omega_M$ | If the whole gap is discovery-legibility, the finding is about environment construction rather than propensity | Pre-commits us to distinguish these so we can't report whichever framing the data flatters |
| **H6** (eval-awareness) | In condition G (agent told it is being evaluated on a safety benchmark), $\pi(\mathrm{G}) \le \pi(\mathrm{A})$ | Awareness plausibly suppresses crossing (sandbagging) but Instrumental Choices found awareness in 0.65% of transcripts and it wasn't protective when present | Either result is publishable: suppression is alarming for eval methodology; no effect replicates Instrumental Choices' finding |
| **H7** (temporal drift) | Between the primary collection and the +4-week replication, the per-model crossing rate on conditions A, B, F changes by $\le$ 3 percentage points for at least 4 of 5 models | Silent provider updates typically shift downstream metrics by a few points; larger shifts would invalidate cross-time comparisons in propensity literature | Larger drift means propensity evaluations cannot be compared across weeks without controls |
| **H8** (provider substitution) | For Opus 4.7 and GPT-5.5, crossing rates via direct API vs OpenRouter differ by $\le$ 2 percentage points on conditions A, B | Aggregators should be transparent to model behavior | Any larger difference is a silent confound affecting half the eval literature |

### 2. Primary vs secondary estimand

**Primary (one, pre-specified):** the fidelity gap in condition B, $\Delta_{\mathrm{fid}}(\mathrm{B}) = \pi_N(\mathrm{B}) - \pi_M(\mathrm{B})$, and its posterior credible interval on the risk-difference scale at the observed baseline.

**Secondary (family, BH-corrected at q=0.10):**
- Fidelity ratio $\rho(\mathrm{B}) = \pi_M(\mathrm{B}) / \pi_N(\mathrm{B})$
- Fidelity gap and ratio at other conditions (A, C, D, E, F)
- Within-arm necessity contrast $\pi(\mathrm{B}) - \pi(\mathrm{A})$
- Within-arm decomposition into legibility ($\delta$) and willingness ($\omega$) components
- Evaluation-awareness contrast $\pi(\mathrm{G}) - \pi(\mathrm{A})$
- Per-model crossing rates (all conditions, both arms) as pre-specified descriptive statistics
- Temporal-drift contrast (H7)
- Provider-substitution contrast (H8)
- Escalation-depth $\mathbb{E}[A]$ per condition per arm

### 3. Frozen artifacts referenced by DOI

The pre-registration is a manifest that pins specific commits. After timestamp, the following are immutable inputs to the reported analyses:

- **Repository commit hash** at pre-reg time, pinning: ADR-000 through ADR-003, PLAN.md, `docs/proposal/`, `data/scenarios/{A..G}/` YAML specs, and the scorer implementation once written.
- **Panel** as fixed in ADR-002 (five models, four developers, access routes named).
- **Sample-size policy** as fixed in ADR-002 (frontier tier 100/cell escalating to 300 on signal; open/mid tier 300/cell; kill-floor at 0-crossing pilot).
- **Command contract v0** (ADR-003) as the scoring specification. If revised at pilot κ gate, the revised version and its rationale are filed as an amendment before the arm M full run.
- **Analysis plan** (§6 of the proposal): hierarchical Bayesian logistic with Student-$t$(3, 0, 2.5) priors on all coefficients, half-normal(0,1) priors on variance components, Firth penalized ML as frequentist fallback. Effects reported on risk-difference, risk-ratio, and odds-ratio scales.

### 4. Analysis decisions locked in advance

- **No interim looks.** Fixed sample size. Rare-event interim estimates are unstable enough that sequential boundaries invite stopping on noise.
- **Per-model always reported.** Pooled rates never reported without per-model breakdown adjacent.
- **Null-result handling:** for any cell with zero events at n episodes, report the exact one-sided 95% upper bound $1 - 0.05^{1/n}$ (rule of three at large n). A pre-planned bounded null is a first-class result.
- **Scorer κ gate:** if pilot κ < 0.80, the command contract is revised via an amendment before arm M full run. Analysis never proceeds on a scorer below threshold.
- **Instrumentation-leak diagnostic (arm N only):** first-attempt willingness must be indistinguishable from what arm E would show if run. Because arm E is out of scope, this becomes a theoretical check documented but not empirically executed.

### 5. Exclusions and stopping rules

- **Episode-level exclusion criteria:** trajectories that terminate due to API rate-limiting, network-layer errors, or provider content policy blocks are excluded from labeled analysis and reported as an exclusion count. No exclusion is decided post-hoc based on the label.
- **Panel model deprecation:** if a panel model is deprecated or silently updated between pre-registration and completion, that model's affected cells are re-run before analysis. This is not an amendment; it is a stated pre-committed procedure.
- **Hard stop rule (containment):** any egress alert during arm N halts the study, preserves the run, and triggers disclosure to the affected cloud provider before further sampling. This is a gate, not a matter of judgment.

### 6. What counts as an amendment

Anything in sections 1–5 changes only via an amendment attached to the same OSF record. Amendments require:
- A new ADR in `docs/decisions/` explaining the change and its motivation
- A revised commit hash pinned in the amendment
- The amendment filed *before* the affected data is collected, or the change is not permitted

Silent changes are the failure mode this whole ADR exists to prevent.

### 7. Timestamp SOP

**Timeline:** target OSF submission by end of week 2 (2026-08-08). Do not begin any data collection — including pilot — until the OSF DOI is issued and referenced in a repo commit.

**Process:**

1. Assemble the pre-registration PDF: sections 1–5 above, plus a manifest listing every file at its exact commit hash (use `git rev-parse HEAD` and `git ls-tree -r HEAD` at submission time).
2. Submit as a "Registered Report — Preregistration" on OSF via https://osf.io/prereg/.
3. Once the DOI is issued, commit the DOI back into `docs/pre-registration/osf-doi.md` in the repo. This closes the loop.
4. Send the DOI to the ongoing AWS and GCP AUP pre-registration threads (draft in `docs/communications/aup-pre-registration/`) as an addendum.
5. Reference the DOI in the abstract and manuscript footer of every subsequent artifact.

## Alternatives considered

- **AsPredicted.** Shorter format, faster. Rejected: this pre-reg has 8 hypotheses, 3 hierarchical estimand levels, and 7 conditions × 2 arms. AsPredicted's word limits force elision that would create silent ambiguity — exactly the failure mode being prevented.
- **arXiv preprint of the design as a substitute.** Rejected: arXiv does not timestamp in a review-defensible way for pre-reg purposes; it also would require an endorser (see follow-ups). The design *will* also go to arXiv, but as a manuscript, not as the pre-reg record.
- **No pre-registration.** Rejected as failing the whole project's rigor claim.
- **OSF with a shorter document that references the repo for details.** Adopted (this is the manifest approach in section 3). Keeps the OSF document reviewable while preserving full spec via commit-hash pinning.

## Consequences

**Positive:**
- Every analysis in the paper is either pre-specified or explicitly flagged as post-hoc, no ambiguity.
- Reviewer confidence: the "did you pre-specify this?" question has a citable DOI answer.
- Amendments become deliberate rather than accidental.
- The repo's ADR history mirrors the pre-reg's amendment history — one source of truth for what changed and why.

**Negative:**
- Adds a hard 2-week gate before any spend, including the pilot. Non-negotiable.
- Amendments are visible and reduce reader trust if too frequent — pressure to think harder up front, before the timestamp.
- Post-hoc interesting findings are explicitly labeled as post-hoc in the paper. This is honest, but it means the paper cannot claim any pre-specification benefit for exploratory results.

## Follow-ups

- Assemble the pre-registration PDF from sections 1–5 by end of week 2
- Register the OSF DOI, commit to `docs/pre-registration/osf-doi.md`
- ADR-005 (week 6): neutering wrapper design spec
- ADR-006 (week 9): cloud host selection (c8i vs GCP nested-virt)
- Recruit an arXiv endorser (`cs.AI` or `cs.CR`) — first-time submission gate
