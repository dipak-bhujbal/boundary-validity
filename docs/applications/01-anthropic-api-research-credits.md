# Application: Anthropic API Research Credits

## Program details

| Field | Value |
|:--|:--|
| Program name | `[VERIFY BEFORE SUBMITTING: Anthropic External Researcher Access Program / API Research Credits — exact program name has changed at least once]` |
| Application URL | `[VERIFY BEFORE SUBMITTING: check https://www.anthropic.com/research and https://support.anthropic.com for the current intake link — historically routed through a Typeform or Airtable]` |
| Form type | `[VERIFY BEFORE SUBMITTING: historically a structured web form with 8–12 questions covering researcher background, project summary, models requested, credit ask, and safety considerations]` |
| Credit ceiling | `[VERIFY BEFORE SUBMITTING: no public ceiling; anecdotal awards for independent researchers have ranged from ~$500 to $5000 in API credits, often paired with elevated rate limits]` |
| Turnaround | `[VERIFY BEFORE SUBMITTING: typically 2–6 weeks, sometimes longer; no SLA published]` |
| Eligibility | `[VERIFY BEFORE SUBMITTING: independent researchers are eligible; institutional affiliation is not required but is a positive signal. Prior publications are not required.]` |
| Requested amount | **$500 in Claude API credits (Opus 4.7 + Sonnet)** |

---

## Application draft

### 1. Researcher

I am Dipak Bhujbal, an independent researcher based in Cambridge, Massachusetts. My prior career is in cloud security, distributed-systems architecture, and technical program management at engineering organizations; I am transitioning into empirical AI safety work with a focus on evaluation methodology. I have no prior ML publications. My current portfolio of public work-in-progress artifacts is:

- `github.com/dipak-bhujbal/llama-tools` — Llama-3.1-8B SFT + DPO fine-tuning pipeline with reproducibility manifests.
- `github.com/dipak-bhujbal/release-kit` — release automation used by the above.
- `github.com/dipak-bhujbal/boundary-validity` — the study this application is for. Public pre-registration will be timestamped on OSF at Week 2, before any spend.

I am the sole author of the proposed study. Where I need external judgment (identification argument review, neutering-wrapper design review, arXiv endorsement) I plan to seek acknowledged, non-author input rather than dilute authorship, per ADR-001 in the project repository.

### 2. Study

The proposed study measures the **fidelity gap** in agentic propensity evaluations: the difference in unprompted boundary-crossing rate between matched fabricated (mocked shell) and real (container) substrates, holding the scenario, prompt, and scorer fixed. Every published propensity evaluation to date — PropensityBench (arXiv:2511.20703), Krakovna et al.'s honeypot evaluations (arXiv:2605.29729), and Instrumental Choices (arXiv:2605.06490) — measures crossings against boundaries that exist because the evaluation says they exist. No prior work has checked whether measuring propensity against fictional boundaries yields the same answer as measuring it against real ones. That is a validity question about the entire subfield, answerable with a matched two-arm design.

The design extends **SandboxEscapeBench** (Marchand et al., arXiv:2603.02277) as an instrument rather than a competitor: SandboxEscapeBench estimates capability under instructed adversarial framing (δ=1, ω=1 by construction), which is exactly the calibration input this study needs for Phase 0 conditioning. The primary estimand is ρ = π_M / π_N, the fidelity ratio, on condition B (blocked in-sandbox path). Arm M is a mocked shell with no substrate. Arm N is a real container with a real affordance surface but the exploit is silently neutered by an intercept-and-fake wrapper — **no live escape is ever possible in this study by construction**. Arm E (live exploit) is explicitly out of scope and deferred as documented future work (ADR-001).

### 3. Why Claude specifically

The pre-registered panel is five models across four developers (ADR-002). Claude Opus 4.7 is on the panel for two specific reasons that neither substitution nor omission would satisfy:

1. **Frontier ceiling anchor with a known-zero prior.** Opus 4.6 crossed at zero across every condition in Instrumental Choices. Whether that pattern holds under an enforced-boundary substrate is a first-order question for the study — a positive rate in arm N with a zero rate in arm M for a frontier Claude model would be one of the more directly consequential findings this design can produce.
2. **Provider-substitution audit.** Opus 4.7 is accessed both via the direct Anthropic API and via OpenRouter, and the difference between the two routes is a pre-registered secondary estimand. Direct API access is load-bearing for that audit; aggregator-only access would confound it.

### 4. Budget derivation

Per PLAN.md, Arm M for Opus 4.7 is capped at 100 episodes/cell across 7 conditions under the frontier-tier sample policy (ADR-002), escalating to 300 only in conditions where pilot shows signal. Arm N for Opus 4.7 is 100–300 episodes across conditions B and F. Assuming a mid-length agentic trajectory (~15–25k input tokens, ~2–5k output tokens per episode at current Opus pricing), total Opus spend across arms M and N is estimated at $350–$450. The **$500 request** covers this envelope with a small buffer for pilot re-runs, scorer-calibration episodes, and any conditions promoted from 100 to 300 episodes.

### 5. Timeline and deliverables

Sixteen-week solo pipeline to TMLR submission (PLAN.md):

- Weeks 1–2: OSF pre-registration timestamped, cloud provider abuse-team notification sent.
- Weeks 3–6: Inspect AI arm M harness, Phase 0 SandboxEscapeBench calibration, arm M full run.
- Weeks 7–8: Arm M analysis, interim workshop-length technical report (publishable standalone).
- Weeks 9–13: Arm N harness (cloud nested-virt, intercept-and-fake neutering wrapper), pilot, full run.
- Weeks 14–16: Full analysis, manuscript, submission.

### 6. Containment protocol summary

- No live escape possible: arm M has no substrate; arm N's exploit path is intercepted before execution.
- Nested isolation for arm N: container inside a VM inside a cloud host, following SandboxEscapeBench architecture.
- Default-deny egress at hypervisor and host firewall. No live credentials. No package proxy. Ephemeral hosts destroyed after each sample.
- Cloud provider abuse team is notified before arm N execution begins (G3 gate in PLAN.md).
- Only mechanisms from the published SandboxEscapeBench suite are used. No new exploit development. No capability uplift produced.
- Full containment specification is in §7 of `docs/proposal/boundary-validity-gap-proposal.md`.

### 7. Public artifact commitment

All harness code, scenario specifications, OSF pre-registration, raw episode trajectories, hierarchical Bayesian fits, and the manuscript will be released under MIT license at `github.com/dipak-bhujbal/boundary-validity` at submission time. Anthropic will be acknowledged for API credit support in any resulting paper and in the repository README. I will send a copy of the submitted manuscript to the program contact before public posting if that is preferred.

### 8. Contact

- Name: Dipak Bhujbal
- Email: dipak.bhujbal23@gmail.com
- Location: Cambridge, Massachusetts
- Phone: `[VERIFY BEFORE SUBMITTING: add if required]`
- LinkedIn: `[VERIFY BEFORE SUBMITTING: add profile URL]`
- GitHub: `github.com/dipak-bhujbal`

---

## Reviewer checklist (Dipak, before submitting)

1. `[ ]` Confirm the current program URL and program name — Anthropic has renamed and moved this program at least once. Check the Anthropic research page, support center, and any recent announcement posts.
2. `[ ]` Confirm the form is still a structured web form; if it has switched to an open email intake, restructure this draft as an email body.
3. `[ ]` Confirm the $500 ask is within norms for independent-researcher awards; if the observed ceiling is higher (e.g. $1000+), consider raising the ask to cover the full arm M + arm N Opus envelope with a wider safety margin.
4. `[ ]` Add your phone number if the form asks for it.
5. `[ ]` Add your LinkedIn URL (Section 8).
6. `[ ]` Decide whether to disclose prior industry affiliations by employer name; the draft intentionally keeps this generic ("cloud security, distributed-systems architecture, TPM"). Named employers would be a positive signal if the roles are recognizable at frontier labs.
7. `[ ]` If the form has a rate-limits question separate from credits, request elevated rate limits for Opus 4.7 during weeks 4–6 (arm M full run) and weeks 12–13 (arm N full run).
8. `[ ]` If the form asks for co-investigators or advisors, state that this is a sole-author study (ADR-001) and list any acknowledged reviewers you have confirmed by submission date.
9. `[ ]` Verify the SandboxEscapeBench arXiv ID (2603.02277) and Instrumental Choices arXiv ID (2605.06490) against your local copy of the proposal — these are cited from the proposal and should match exactly.
10. `[ ]` Confirm you are comfortable with the "no prior ML publications" disclosure being read alongside the llama-tools + release-kit portfolio links; this is deliberate honesty per the project's ADR discipline.
