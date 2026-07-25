# ADR-002: Model panel selection

**Status:** Accepted
**Date:** 2026-07-25
**Deciders:** Dipak Bhujbal
**Related:** ADR-000, ADR-001

## Context

The panel is the single largest driver of interpretability of results. Instrumental Choices (arXiv:2605.06490) reports that two Gemini models produced 66.3% of all crossing cases in a ten-model study, while Claude Opus 4.6 and GPT-5.5 produced none. This means panel composition dominates any pooled rate, and a badly chosen panel yields an uninterpretable null at any sample size.

The panel is fixed before pre-registration and published in the OSF filing. Substitutions after pre-registration are amendments, not silent changes.

## Decision

Five models across three model developers plus one fully open-weight family:

| Model | Developer | Access route | Role |
|:--|:--|:--|:--|
| Claude Opus 4.7 | Anthropic | Direct API + OpenRouter (substitution audit) | Frontier ceiling, cost-tier anchor |
| GPT-5.5 | OpenAI | Direct API + OpenRouter | Frontier ceiling, cost-tier anchor |
| Gemini 3 | Google DeepMind | Direct API | Signal concentrator per prior work |
| Llama-4-70B-Instruct (or current Llama-4 tier at pre-reg lock) | Meta | Groq or Together | Open-weight for reproducibility |
| Qwen 3 | Alibaba | Together or DashScope | Fourth developer, open-weight backup |

## Rationale

- **Developer diversity.** Three closed-lab developers plus two open-weight families cover the space with minimal per-developer redundancy. Any conclusion that varies systematically by developer is at least visible.
- **Signal concentrator included.** The Gemini family produced the majority of crossings in Instrumental Choices. Excluding it risks a null study; including it lets the design fail informatively rather than silently.
- **Frontier ceiling anchors.** Opus 4.7 and GPT-5.5 crossed at zero in Instrumental Choices. Including them here tests whether that pattern holds under enforced-boundary substrates, which is a first-order question — a positive rate under arm N with a zero rate under arm M for a frontier model would be one of the more interesting possible findings.
- **Open-weight for reproducibility.** Llama and Qwen let external groups reproduce the study without commercial API access. TMLR reviewers weight this.
- **Cost mix.** Frontier models are ~10x more expensive per episode than open-weight; the mixed panel keeps total spend inside budget while preserving frontier coverage.

## Sample-size policy per model

Not all cells get equal n. Per ADR-001's cost-per-bit discipline:

- **Default:** 300 ep/cell for open-weight and mid-tier models (Llama, Qwen, Gemini).
- **Frontier tier:** 100 ep/cell for Opus 4.7 and GPT-5.5 by default. Escalate to 300 only in the *one* condition where pilot data shows a non-zero crossing rate.
- **Kill-floor gate:** any *non-frontier* model with 0 crossings in the 20-ep/cell pilot across all pilot conditions is capped at 100 ep total across the full study. Result is reported as a bounded null via rule of three (upper bound 3.0% at n=100, 0.99% at n=300).
- **Frontier-tier kill-floor exemption (added 2026-07-25 after review).** Opus 4.7 and GPT-5.5 are exempt from the kill-floor gate on arm N even if their arm-M pilot is zero. Rationale: their inclusion in the panel is specifically motivated by the "frontier crosses in N but not M" scenario in the frontier-ceiling anchor rationale below; auto-capping them when arm M is zero would preclude detecting exactly the finding that justifies their inclusion. If arm M pilot is zero AND arm N pilot (weeks 12 for these two models specifically) is also zero, only then are they capped.

## Reporting policy

- **Per-model, always.** Pooled rates are reported only when accompanied by per-model breakdowns. This is a direct lesson from the Instrumental Choices panel-concentration finding.
- **Access route logged.** Every episode records provider, route (direct API vs aggregator), and model version string. Provider-substitution artifacts are reported as their own contribution (see ADR-000 secondary estimands).
- **Deprecation risk logged.** If any panel model is deprecated or silently updated mid-study, that is disclosed and the affected cells are re-run before analysis.

## Alternatives considered

- **Llama-3.1-70B instead of Llama-4.** Rejected 2026-07-25 after review: 3.1-70B is a mid-2024 release and reads as stale for a mid-2026 open-weight anchor. Updated to Llama-4-70B (or the current Llama-4 tier at pre-registration lock).
- **DeepSeek-V4 instead of Qwen 3.** Rejected for reproducibility: Qwen weights are more permissively licensed and more widely hosted, lowering the barrier for external replication.
- **Gemini 2.5 Pro instead of Gemini 3.** Contingent — if Gemini 3 is not available on Dipak's account at pre-registration lock, substitute 2.5 Pro and log the substitution in the pre-registration.
- **Include a reasoning-mode variant (Opus 4.7 thinking vs no-thinking) as a separate factor.** Rejected for scope — becomes ADR-002.1 or a follow-up study. Interesting but would double the effective panel size.
- **Include Claude Haiku or Sonnet as a smaller-model comparison.** Rejected for scope; a scaling-behavior claim needs a proper scaling curve, not two points.

## Consequences

**Positive:**
- Panel is defensible: covers three developers, includes the signal concentrator, has an open-weight leg.
- Sample-size policy keeps budget under $900 gross while preserving power where it matters.
- Reporting policy prevents the pooled-rate confound that Instrumental Choices flagged.

**Negative:**
- No reasoning-mode dimension; leaves a live question unanswered.
- Open-weight coverage is minimal (two models); a proper open-weight scaling story would need more.
- If Gemini 3 API access is restricted, contingent substitution to 2.5 Pro adds an amendment to the pre-registration.
