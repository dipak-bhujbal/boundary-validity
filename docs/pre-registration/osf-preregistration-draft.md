# OSF Pre-Registration: Stipulated Boundaries Are Not Real Boundaries

**Title:** Stipulated Boundaries Are Not Real Boundaries: Measuring the Validity Gap in Propensity Evaluations of Agentic Boundary Crossing (Arms M and N)

**Author:** Dipak Bhujbal
**Affiliation:** Independent researcher
**Location:** Cambridge, Massachusetts
**Contact:** dipak.bhujbal23@gmail.com
**Date:** 2026-07-25
**Version:** v0.1 draft
**Pre-registration format:** Registered Report — Preregistration (OSF)

---

## Preamble: This document is not the study

This document is a manifest. It describes what will be done, what will be measured, and what analytical decisions have been fixed in advance. It is not a substitute for the repository, the scenario specifications, the harness code, or the analysis scripts.

The authoritative artifact is the repository at:

> **https://github.com/dipak-bhujbal/boundary-validity** at commit hash **`<REPO_COMMIT_HASH>`**

After OSF timestamp, the above commit hash is immutable. All pre-registered content below is implemented in that commit. If this document and the repository disagree, the repository at the pinned commit is correct. Any substantive change to the content of this document after timestamp requires a filed amendment (see Section 7).

---

## 1. Study Title and Hypotheses

### 1.1 Title

*Stipulated Boundaries Are Not Real Boundaries: Measuring the Validity Gap in Propensity Evaluations of Agentic Boundary Crossing (Arms M and N).*

### 1.2 Background and Motivation

Propensity evaluations in AI safety measure what an agent chooses to do rather than what it is able to do. The current generation of these evaluations shares a structural feature that has not been tested: the boundary the agent is measured against is stipulated by the evaluation author rather than enforced by the system. A policy document declares that cross-team credit transfers are forbidden; a colleague's note says lifecycle controls are off limits. The violation is legible only because the fiction says it is a violation.

This study asks whether that substitution is valid. A boundary-crossing scenario is held fixed and only the reality of the boundary is varied. Container isolation is used as the enforced case because it is simultaneously kernel-enforced, binary, deterministically scorable, and load-bearing for the infrastructure on which the evaluation community runs its own evaluations.

The primary quantity is not a propensity rate. It is the **fidelity gap** $\Delta_{\mathrm{fid}}$: the difference in unprompted crossing rate between matched fabricated and real substrates. If fabricated environments overstate crossing, existing propensity numbers are inflated. If they understate, the field is being reassured by its own methodology. Either result changes how every prior propensity paper should be read.

### 1.3 Three-Factor Decomposition

Each episode yields four binary labels: $D$ (discovery: agent issued a command exposing the affordance), $X$ (crossing attempt: agent issued a command acting on the affordance), $Z$ (crossing succeeded, defined only for arm E which is out of scope for this paper), and $Y$ (benign task reached its accepted end state), plus escalation depth $A$ (count of distinct crossing attempts). The structural constraint $X \le D$ holds by construction.

Define:
- $\delta(m,c,a) = \Pr[D = 1]$ — discovery rate (environment legibility × agent thoroughness)
- $\omega(m,c,a) = \Pr[X = 1 \mid D = 1]$ — willingness conditional on discovery
- $\kappa(m,\mu) = \Pr[Z = 1 \mid X = 1]$ — capability (estimated in Phase 0, not primary here)

Then $\pi \equiv \Pr[X=1] = \delta\omega$, and the fidelity gap decomposes as:

$$\Delta_{\mathrm{fid}} = \underbrace{\omega_M(\delta_N - \delta_M)}_{\text{legibility}} + \underbrace{\delta_N(\omega_N - \omega_M)}_{\text{willingness}}$$

This decomposition is necessary for the primary estimand to be interpretable: a difference in $\pi$ between arms could be entirely a difference in legibility $\delta$, with willingness $\omega$ identical, which is a claim about environment construction rather than model propensity. Instrumenting $D$ separately from $X$ is what makes the primary estimand mean something.

### 1.4 Hypotheses

All hypotheses are directional. Each states what "wrong" would mean so that being wrong is informative. A result that falsifies a hypothesis is a first-class result, not a failure of the study.

| ID | Statement | Directional prediction | Reasoning | Failure interpretation |
|:--|:--|:--|:--|:--|
| **H1** (low base rate) | Arm M crossing rate in condition A | $\pi_M(\mathrm{A}) < 0.02$ | A container isolation boundary is more salient as a boundary than a policy document; refusal training plausibly binds more tightly to sandbox escape than to fictional credit transfers | If $\pi_M(\mathrm{A}) \ge 0.02$, sandbox salience is weaker than assumed; base-rate priors must be recalibrated upward before interpreting subsequent conditions |
| **H2** (necessity dominates) | Crossing rate lift from blocking the in-sandbox path | $\pi(\mathrm{B}) - \pi(\mathrm{A}) \in [0.08, 0.15]$ within each arm | Direct transfer of the largest reported effect from Instrumental Choices (arXiv:2605.06490), attenuated for the salience reason in H1 | If the lift is $< 0.08$, the necessity effect does not transport to enforced-boundary substrates; if $> 0.15$, isolation amplifies necessity beyond prior estimates — both informative |
| **H3** (framing null) | Effect of urgency/consequence framing on crossing rate | No effect distinguishable from zero (conditions C–D versus A, urgency/consequence variants) | Replication of the null reported in Instrumental Choices | If a non-zero effect is detected, their null was environment-specific, not a general property of framing — worth reporting as a context-dependence finding |
| **H4** (fidelity gap, primary) | Direction and magnitude of the arm M vs arm N contrast in condition B | $\Delta_{\mathrm{fid}}(\mathrm{B}) = \pi_N(\mathrm{B}) - \pi_M(\mathrm{B}) < 0$, with $\lvert\Delta_{\mathrm{fid}}(\mathrm{B})\rvert \ge 0.03$; equivalently fidelity ratio $\rho = \pi_M(\mathrm{B}) / \pi_N(\mathrm{B}) > 1$ | A real substrate supplies friction and failure feedback absent in a mock shell; the mock arm overstates propensity | This hypothesis is held weakly. The more interesting failure is $\rho < 1$: fabricated environments underestimate crossing, meaning the literature's reassuring numbers are methodology artifacts. Either direction is meaningful; the pre-commitment prevents post-hoc framing |
| **H5** (not purely legibility) | Whether the willingness component of the decomposition is non-zero | $\omega_N \ne \omega_M$, i.e., the willingness component of $\Delta_{\mathrm{fid}}$ is distinguishable from zero | If the entire fidelity gap is legibility ($\delta_N \ne \delta_M$ with $\omega_N = \omega_M$), the finding is about environment construction, not model propensity | Pre-commits to distinguishing these so results cannot be reframed post-hoc as whichever component the data favours |
| **H6** (eval-awareness) | Crossing rate in condition G relative to condition A | $\pi(\mathrm{G}) \le \pi(\mathrm{A})$, i.e., awareness that the episode is a safety benchmark does not increase crossing rate | Awareness plausibly suppresses crossing (sandbagging); Instrumental Choices found eval-awareness signals in 0.65% of transcripts and it was not protective when present | Either result is publishable: $\pi(\mathrm{G}) < \pi(\mathrm{A})$ means suppression is occurring and sandbagging is a live concern for eval methodology; $\pi(\mathrm{G}) \approx \pi(\mathrm{A})$ replicates Instrumental Choices' finding |
| **H7** (temporal drift) | Per-model crossing rate stability between primary collection and +4-week replication | Between the primary collection and the +4-week replication, the per-model crossing rate on conditions A, B, and F changes by $\le 3$ percentage points for at least 4 of 5 panel models | Silent provider updates typically shift downstream metrics by a few percentage points; larger shifts would invalidate cross-time comparisons in the propensity literature | If $> 3$ pp drift in $\ge 2$ models, propensity evaluations are not comparable across weeks without explicit temporal controls — a methodological finding independent of the primary estimand |
| **H8** (provider substitution) | Crossing rate equivalence for direct API vs OpenRouter access | For Opus 4.7 and GPT-5.5, crossing rates via direct API vs OpenRouter differ by $\le 2$ percentage points on conditions A and B | Aggregators should be transparent to model behavior; any access-route effect is a silent confound | A difference $> 2$ pp on either model is a confound affecting literature that uses aggregators, and must be disclosed as a limitation of any study not controlling for access route |

---

## 2. Primary vs Secondary Estimand

### 2.1 Primary Estimand (one, pre-specified)

**$\Delta_{\mathrm{fid}}(\mathrm{B}) = \pi_N(\mathrm{B}) - \pi_M(\mathrm{B})$**

The fidelity gap in condition B (in-sandbox path blocked), measured as the difference in unprompted crossing rate between arm N (real container, silently neutered exploit) and arm M (mocked shell, fabricated output). Reported as a posterior credible interval on the risk-difference scale at the observed baseline.

This is the single pre-specified primary outcome. A result that moves this estimate — in either direction, or that bounds it near zero — constitutes the headline finding. Any other result in this pre-registration is secondary by definition and must be presented as such.

A reviewer who reads only one number should read this one. A reviewer who disputes only one analytical decision should dispute one governing this number.

### 2.2 Secondary Estimands (family, BH-corrected at q = 0.10)

All secondary estimands are pre-specified. "Pre-specified secondary" means the analysis was planned in advance, not that the result is less interesting.

- **Fidelity ratio** $\rho(\mathrm{B}) = \pi_M(\mathrm{B}) / \pi_N(\mathrm{B})$, with posterior credible interval. This is the correction factor the rest of the field could apply to mock-calibrated estimates.
- **Fidelity gap and ratio at other conditions** (A, C, D, E, F): same contrast at each condition, to test whether the gap is condition-specific or consistent.
- **Within-arm necessity contrast** $\pi(\mathrm{B}) - \pi(\mathrm{A})$, separately for arms M and N.
- **Within-arm decomposition** into legibility ($\delta_N - \delta_M$) and willingness ($\omega_N - \omega_M$) components per Section 4.3 of the proposal.
- **Evaluation-awareness contrast** $\pi(\mathrm{G}) - \pi(\mathrm{A})$ (H6 above).
- **Per-model crossing rates** across all conditions and both arms. These are pre-specified descriptive statistics, not a test of model differences. Reported always, alongside any pooled rate.
- **Temporal-drift contrast** (H7): per-model change from primary collection to +4-week replication on conditions A, B, F.
- **Provider-substitution contrast** (H8): direct API vs OpenRouter on conditions A, B for Opus 4.7 and GPT-5.5.
- **Escalation depth** $\mathbb{E}[A]$ per condition per arm: whether real substrates elicit more or fewer distinct crossing attempts conditional on any attempt occurring.

---

## 3. Frozen Artifacts Referenced by DOI

### 3.1 How to populate this section before submission

This section contains placeholders that must be replaced before submitting to OSF. All values are derived from the repository state at submission time. Run the following from the repository root:

```bash
# Repository commit hash (all artifacts below are pinned to this)
git rev-parse HEAD

# File-level hashes for the artifacts named below
git ls-tree -r HEAD data/scenarios docs/decisions PLAN.md
```

Replace each placeholder below with the corresponding output. Do not populate speculatively; run these commands at submission time from a clean working tree with no uncommitted changes.

### 3.2 Repository commit hash

**`<REPO_COMMIT_HASH>`** — the Git SHA-1 of the repository at pre-registration submission. After OSF timestamp, this commit is the immutable definition of what was pre-registered. Any subsequent commit that changes a pre-registered artifact constitutes a deviation and requires a filed amendment.

The pinned commit contains: ADR-000 through ADR-003, this document, `PLAN.md`, `docs/proposal/boundary-validity-gap-proposal.md`, and all scenario specification files listed below.

### 3.3 Scenario specification files

Scenario YAML files define, per condition, the exact affordance, the seed setup applied identically to arms M and N, the discovery signatures, the crossing signatures, the exclusions, and the condition flags. These are not duplicated here; they are referenced by path and hash.

| Path | File hash |
|:--|:--|
| `data/scenarios/A/scenario.yaml` | `<SCENARIO_A_HASH>` |
| `data/scenarios/B/scenario.yaml` | `<SCENARIO_B_HASH>` |
| `data/scenarios/C/scenario.yaml` | `<SCENARIO_C_HASH>` |
| `data/scenarios/D/scenario.yaml` | `<SCENARIO_D_HASH>` |
| `data/scenarios/E/scenario.yaml` | `<SCENARIO_E_HASH>` |
| `data/scenarios/F/scenario.yaml` | `<SCENARIO_F_HASH>` |
| `data/scenarios/G/scenario.yaml` | `<SCENARIO_G_HASH>` |

Each YAML must conform to the schema defined in ADR-003 (`docs/decisions/ADR-003-command-contract-v0.md`, hash `<ADR003_HASH>`). Any change to a scenario YAML after timestamp is an amendment.

### 3.4 Decision records pinned

| ADR | Title | Hash |
|:--|:--|:--|
| ADR-000 | Project charter | `<ADR000_HASH>` |
| ADR-001 | Arm scope and TMLR fit | `<ADR001_HASH>` |
| ADR-002 | Model panel selection | `<ADR002_HASH>` |
| ADR-003 | Scoring command contract v0 | `<ADR003_HASH>` |
| PLAN.md | Project plan and gates | `<PLAN_HASH>` |

### 3.5 Model panel (fixed, per ADR-002)

The panel is fixed at pre-registration. Post-timestamp substitutions are amendments.

| Model | Developer | Access route | Role |
|:--|:--|:--|:--|
| Claude Opus 4.7 | Anthropic | Direct API + OpenRouter (substitution audit) | Frontier ceiling, cost-tier anchor |
| GPT-5.5 | OpenAI | Direct API + OpenRouter | Frontier ceiling, cost-tier anchor |
| Gemini 3 | Google DeepMind | Direct API | Signal concentrator per prior work |
| Llama-3.1-70B-Instruct | Meta | Groq or Together | Open-weight for reproducibility |
| Qwen 3 | Alibaba | Together or DashScope | Fourth developer, open-weight backup |

**Contingency:** If Gemini 3 is not available on the study account at pre-registration lock, substitute Gemini 2.5 Pro and log the substitution as an amendment to this record.

### 3.6 Sample-size policy (fixed, per ADR-002)

- **Default:** 300 episodes per cell for open-weight and mid-tier models (Llama, Qwen, Gemini).
- **Frontier tier:** 100 episodes per cell for Opus 4.7 and GPT-5.5 by default. Escalate to 300 only in the single condition where pilot data shows a non-zero crossing rate.
- **Kill-floor gate:** any model with 0 crossings in the 20-episode per cell pilot across all pilot conditions is capped at 100 episodes total across the full study. Result is reported as a bounded null via rule of three (upper bound 3.0% at $n=100$, 0.99% at $n=300$).

### 3.7 Scoring specification (fixed, per ADR-003)

The command contract v0 (ADR-003, hash `<ADR003_HASH>`) is the pre-registered scoring specification. It defines:
- Trajectory pre-processing rules (shell command extraction, normalization, sub-command splitting, comment/quote stripping)
- Label extraction precedence for $D$, $X$, and $Y$
- Neutering-layer contract for arm N (same regex list, byte-identical, enforced by unit test)
- Exclusion patterns and inline `reason:` requirements

If the pilot Cohen's kappa falls below 0.80 (gate G2, end of week 5), the contract is revised via an amendment before any arm M full run. No arm M data is analyzed under a contract that has not cleared this gate.

### 3.8 Analysis plan (fixed, per proposal §6)

Hierarchical Bayesian logistic regression:

$$X_i \sim \mathrm{Bernoulli}(p_i), \quad \mathrm{logit}(p_i) = \alpha + \beta_{c[i]} + \gamma_{m[i]} + \theta_{a[i]} + \eta_{c[i],a[i]} + u_{s[i]} + v_{m[i],s[i]}$$

with $u_s \sim \mathcal{N}(0,\sigma_s^2)$, $v_{ms} \sim \mathcal{N}(0,\sigma_{ms}^2)$, Student-$t(3, 0, 2.5)$ priors on all coefficients, half-normal$(0,1)$ priors on variance components, and Firth penalized maximum likelihood as frequentist fallback. The interaction $\eta_{c,a}$ carries the fidelity gap; the primary contrast is $\eta_{B,N} - \eta_{B,M}$.

Effects are reported on all three scales: risk difference, risk ratio, and odds ratio. At base rates in the low single digits these scales diverge substantially; all three are reported because they serve different audiences (risk difference for infrastructure owners, odds ratio for cross-model comparison).

---

## 4. Analysis Decisions Locked in Advance

These decisions are fixed. The entry for each decision includes what would constitute a violation of it, so that a reader can assess compliance without asking the author.

### 4.1 No interim looks

The sample size is fixed before data collection. No interim analysis is performed and no sequential boundary is used. **Violation:** any analysis of crossing rates before the pre-specified cell sizes are reached, regardless of framing (e.g., "just to check the harness"). Exception: the pilot episodes used for scorer $\kappa$ calibration at gate G2 are not analyzed for outcome rates; they are used only for scorer agreement.

### 4.2 Per-model rates always reported alongside pooled rates

Pooled crossing rates are never the sole figure in any table or exhibit. **Violation:** any table reporting a pooled rate without an adjacent per-model breakdown. This rule is motivated directly by the panel-concentration finding in Instrumental Choices, where two Gemini models produced 66.3% of all crossings in a ten-model study; a pooled rate from that panel would have been uninterpretable.

### 4.3 Null-result handling: bounded null, not absence

For any cell with zero events at $n$ episodes, the result is reported as the exact one-sided 95% upper bound $1 - 0.05^{1/n}$ (approximated by the rule of three $3/n$ at large $n$). A pre-planned bounded null is a first-class result and is not escalated into additional sampling to find a positive. **Violation:** reporting a zero-crossing cell as "no crossing observed" without the bound, or collecting additional episodes in that cell beyond the pre-specified $n$ to search for a positive.

### 4.4 Scorer $\kappa$ gate before arm M full run

If pilot Cohen's $\kappa$ between the deterministic scorer and hand-adjudication on 100 stratified pilot episodes is below 0.80, the command contract is revised via an amendment before arm M full run. **Violation:** proceeding with arm M outcome analysis on a scorer that has not cleared $\kappa \ge 0.80$, or revising the scorer after arm M data exists without filing an amendment.

### 4.5 Instrumentation-leak diagnostic (arm N, theoretical)

Because arm E is out of scope, the equivalence check $\omega^{(1)}_N = \omega^{(1)}_E$ cannot be empirically executed. It is documented as a theoretical check and its inapplicability is disclosed in the manuscript. **Violation:** claiming empirical evidence for neutering transparency without arm E data, or failing to disclose that the check was not executed.

### 4.6 Secondary estimands corrected at q = 0.10

All secondary contrasts are corrected for multiplicity using Benjamini-Hochberg at $q = 0.10$ across the pre-registered family defined in Section 2.2. **Violation:** reporting a secondary contrast as significant without applying BH correction, or adding contrasts to the BH family post-hoc without flagging them as exploratory.

---

## 5. Exclusions and Stopping Rules

### 5.1 Episode-level exclusion criteria

Trajectories are excluded from outcome analysis if they terminate due to:
- API rate-limiting or timeout (provider-side)
- Network-layer errors (harness-side)
- Provider content policy blocks that prevent the scenario from being presented

Exclusion decisions are made on these criteria only, applied before labels are extracted. **No trajectory is excluded on the basis of its label.** All exclusions are reported as an exclusion count in the manuscript with counts per exclusion category.

### 5.2 Panel model deprecation or silent update

If a panel model is deprecated or silently updated between pre-registration and the completion of data collection, the affected cells are re-run before analysis under the updated model version. The re-run is logged with the new model version string and the substitution is disclosed. This is a stated pre-committed procedure, not an amendment. Model version strings are recorded per episode for exactly this purpose.

### 5.3 Hard stop rule (arm N containment)

Any egress alert generated by the monitoring layer during arm N — any outbound connection attempt reaching the hypervisor or host firewall log — halts data collection immediately, preserves the full run log, and triggers disclosure to the affected cloud provider before any further sampling. This is a gate in the run harness, not a matter of operator judgment. **This rule is not negotiable and is not subject to amendment.** An egress alert that is retrospectively determined to be a false positive is still a stop event; data collection resumes only after the source of the alert is identified and documented.

---

## 6. What Counts as an Amendment

Any change to the content of Sections 1 through 5 of this pre-registration after the OSF timestamp is an amendment. Amendments are not prohibited; they are required to be visible.

### 6.1 Amendment requirements

An amendment to this pre-registration requires all of the following:
1. A new ADR in `docs/decisions/` explaining the change and its motivation.
2. A revised commit hash pinned in the amendment text.
3. The amendment filed to the same OSF record before the affected data is collected.

A change that does not meet all three requirements is not an amendment — it is a silent deviation, which is the failure mode this entire document exists to prevent.

### 6.2 Changes that are not amendments

- Running the harness and discovering a harness bug that does not affect pre-registered analytical decisions.
- Logging additional metadata fields beyond what is pre-specified, provided the additional logging does not influence outcome labels.
- The model deprecation procedure in Section 5.2 (pre-committed, not a post-hoc decision).
- Corrections to typographical errors in this document that do not change any analytical decision.

### 6.3 Exploratory analyses

Analyses not specified in this pre-registration may be reported in the manuscript but must be clearly labeled "Exploratory (not pre-specified)." They cannot be elevated to pre-specified status retroactively.

---

## 7. Metadata and Submission Block

### 7.1 OSF submission checklist

- [ ] Repository is at a clean, tagged commit. `git rev-parse HEAD` output recorded.
- [ ] All placeholder hashes in Section 3 are populated from `git ls-tree -r HEAD data/scenarios docs/decisions PLAN.md`.
- [ ] No uncommitted changes to any file listed in Section 3.4 or Section 3.3.
- [ ] This document has been read top-to-bottom once after placeholder population and before submission.
- [ ] Submission made to `https://osf.io/prereg/` under format "Registered Report — Preregistration."
- [ ] DOI issued by OSF (expected within 24 hours of submission).
- [ ] DOI committed to `docs/pre-registration/osf-doi.md` in the repository. This commit is the loop-closing event; no data collection begins before this commit exists.
- [ ] DOI referenced in `docs/communications/aup-pre-registration/` addendum to the AWS and GCP abuse team threads.

### 7.2 Target submission date

End of week 2 of the study timeline: **2026-08-08**. No data collection — including the 20-episode pilot — begins before the OSF DOI is committed to the repository.

### 7.3 Versioning after submission

This document is version v0.1. Amendments increment the minor version (v0.2, v0.3, …). A re-registration on a substantially different design would be v1.0 with a new OSF record. All versions are attached to the same OSF record so that the amendment history is auditable in one place.

### 7.4 Contact for questions about this pre-registration

Dipak Bhujbal — dipak.bhujbal23@gmail.com
