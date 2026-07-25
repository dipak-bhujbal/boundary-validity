# Application: Google DeepMind / Gemini API Research Credits

## Program details

| Field | Value |
|:--|:--|
| Program name | `[VERIFY BEFORE SUBMITTING: Google Cloud Research Credits program covers Vertex AI / Gemini via GCP; a separate "Gemini API for Academic Research" or Kaggle-hosted researcher program has existed at times. Confirm which channel is currently open for independent (non-university) researchers.]` |
| Application URL | `[VERIFY BEFORE SUBMITTING: check https://cloud.google.com/edu/researchers and https://ai.google.dev/ — the intake page and program branding has shifted between these surfaces]` |
| Form type | `[VERIFY BEFORE SUBMITTING: Google Cloud Research Credits historically uses a structured web form requiring institutional affiliation and a PI. The Gemini-API-specific researcher channel has at times used an open email or a shorter form.]` |
| Credit ceiling | `[VERIFY BEFORE SUBMITTING: Google Cloud Research Credits historically awards up to $5,000 for standard proposals, with larger awards possible; Gemini-API-specific credits have been smaller and less publicly documented]` |
| Turnaround | `[VERIFY BEFORE SUBMITTING: 4–8 weeks typical for GCP Research Credits]` |
| Eligibility | `[VERIFY BEFORE SUBMITTING: GCP Research Credits historically requires academic affiliation and a faculty PI — an independent researcher may not qualify for that channel. If so, apply via the Gemini API developer/researcher channel instead, or via a Kaggle Research grant.]` |
| Requested amount | **$400 in Gemini API credits (Gemini 3 / Gemini 2.5 Pro)** |

**Note on program fit:** if GCP Research Credits requires academic affiliation and no independent-researcher channel is open, the fallback is (a) Kaggle research credits, (b) direct Gemini API rate-limit uplift request, or (c) budget Gemini spend from personal funds and drop this application. Confirm channel before drafting is final.

---

## Application draft

### 1. Researcher

I am Dipak Bhujbal, an independent researcher based in Cambridge, Massachusetts. My background is cloud security, distributed-systems architecture, and technical program management; I am moving into empirical AI safety with a focus on evaluation methodology. I have no prior ML publications. Public work-in-progress:

- `github.com/dipak-bhujbal/boundary-validity` — the study this application is for; pre-registration timestamped on OSF before any spend.
- `github.com/dipak-bhujbal/llama-tools` — Llama-3.1-8B SFT + DPO fine-tuning pipeline.
- `github.com/dipak-bhujbal/release-kit` — release automation.

Sole author of the proposed study (see ADR-001 in the project repository for the collaboration model and its rationale).

Institutional affiliation: `[VERIFY BEFORE SUBMITTING: none currently. If GCP Research Credits requires a PI, either identify a sponsoring faculty member or redirect this application to the Gemini-API researcher channel.]`

### 2. Study

The study measures the **fidelity gap** in agentic propensity evaluations — the difference in unprompted boundary-crossing rate between matched fabricated (mocked shell) and real (container) substrates, holding scenario, prompt, and scorer fixed. Every published propensity evaluation to date — PropensityBench (arXiv:2511.20703), **Krakovna, Lindner, Ho, Farquhar and Shah's realistic honeypot evaluations** (arXiv:2605.29729), and Instrumental Choices (arXiv:2605.06490) — measures crossings against boundaries stipulated by the evaluation rather than enforced by the system. No prior work has checked whether that substitution is valid.

The design extends SandboxEscapeBench (Marchand et al., arXiv:2603.02277) as an instrument. Arm M is a mocked shell with no substrate. Arm N is a real container with a real affordance surface but the exploit is silently neutered — **no live escape is possible in this study by construction**. The primary estimand is the fidelity ratio ρ = π_M / π_N on condition B (blocked in-sandbox path), reported per-model with credible intervals from a hierarchical Bayesian fit. Full pre-registered analysis plan, hypotheses (H1–H5), power analysis, and containment protocol are in `docs/proposal/boundary-validity-gap-proposal.md` in the project repository.

The design is a direct methodological extension of the Google DeepMind alignment team's honeypot work. Krakovna et al. (2026) show that in a *realistic* deployment substrate Gemini models exhibit no unprompted scheming, while scheming appears when prompts encourage agency or supply hidden goals. That result rests on a fabricated-boundary control group. This study asks the immediately adjacent question: **how much of the "realistic deployment" signal is the realism of the substrate itself versus the realism of the surrounding harness?** A null fidelity gap would license the honeypot literature's reassuring numbers; a non-null gap would qualify them.

### 3. Why Gemini specifically

The pre-registered panel is five models across four developers (ADR-002). Gemini 3 is on the panel for reasons specific to this study that no substitution satisfies:

1. **Signal concentrator.** In Instrumental Choices, two Gemini models produced **66.3%** of all crossing cases across a ten-model panel. Excluding the Gemini family risks an uninterpretable pooled null; including it lets the design fail informatively rather than silently. This is the single most important panel-composition decision in the study.
2. **Bridge to the DeepMind honeypot line of work.** The primary comparator for the fidelity-gap result *is* Krakovna et al.'s Gemini results. Comparing across model families rather than within one confounds fidelity effects with cross-family behavioral differences. Gemini access is load-bearing for the comparison.

If Gemini 3 is not available on the researcher account at pre-registration lock, the ADR-002 fallback is Gemini 2.5 Pro, logged as a pre-registration amendment.

### 4. Budget derivation

Per PLAN.md and ADR-002, Gemini 3 receives the mid-tier default sample allocation: 300 episodes per cell in arm M across 7 conditions (2,100 episodes), and 300 episodes per cell in arm N across conditions B and F (600 episodes). Total ~2,700 Gemini episodes at ~15–25k input + ~2–5k output tokens per agentic trajectory. At current Gemini 3 / 2.5 Pro pricing this is estimated at $250–$350. The **$400 request** covers this envelope plus pilot re-runs and any scorer-calibration episodes.

### 5. Timeline and deliverables

Sixteen-week solo pipeline to Transactions on Machine Learning Research submission (PLAN.md):

- Weeks 1–2: OSF pre-registration timestamped; cloud provider abuse-team notification.
- Weeks 3–6: Inspect AI arm M harness, Phase 0 SandboxEscapeBench calibration, arm M full run.
- Weeks 7–8: Arm M analysis, interim workshop-length technical report.
- Weeks 9–13: Arm N harness (cloud nested-virt), pilot, full run.
- Weeks 14–16: Full analysis, manuscript, submission.

Note on GCP infrastructure: if arm N is hosted on GCP (a live option per ADR-001, alternative is AWS c8i), GCP nested-virt image licensing and abuse-team pre-clearance is on the week-9 critical path. Google Cloud credits (rather than or in addition to Gemini API credits) would cover this. If both are on the table for this program, the study can absorb up to $300 additional in GCP compute credits for arm N nested-virt hosts.

### 6. Containment protocol summary

- No live escape possible by construction: arm M has no substrate; arm N's exploit path is intercepted before execution.
- Nested isolation for arm N: container inside a VM inside a cloud host. Target flag lives on inner VM, never the physical host.
- Default-deny egress at hypervisor and host firewall. No live credentials. No package proxy path. Ephemeral hosts destroyed after each sample.
- GCP abuse team is notified in writing before arm N execution begins (project G3 gate).
- Only mechanisms from the published SandboxEscapeBench suite are used. No new exploit development. No capability uplift produced.
- Full protocol in §7 of the project proposal.

### 7. Public artifact commitment

All harness code, scenario specifications, OSF pre-registration, raw trajectories, Bayesian fits, and manuscript will be released under MIT license at `github.com/dipak-bhujbal/boundary-validity` at submission. Google DeepMind (and Google Cloud, if applicable) will be acknowledged for credit support in the resulting paper and repository README.

### 8. Contact

- Name: Dipak Bhujbal
- Email: dipak.bhujbal23@gmail.com
- Location: Cambridge, Massachusetts
- Phone: `[VERIFY BEFORE SUBMITTING: add if required]`
- LinkedIn: `[VERIFY BEFORE SUBMITTING: add profile URL]`
- GitHub: `github.com/dipak-bhujbal`
- Google Cloud account ID: `[VERIFY BEFORE SUBMITTING: add if the form asks for it — GCP Research Credits are applied to a specific billing account]`

---

## Reviewer checklist (Dipak, before submitting)

1. `[ ]` **Confirm which program channel actually accepts independent researchers.** GCP Research Credits has historically required a faculty PI. If that is still true, this application should be redirected to (a) the Gemini API developer researcher channel, (b) Kaggle research credits, or (c) dropped in favor of self-funding Gemini spend.
2. `[ ]` If a PI is required and you have identified a sponsoring faculty member, add them to Section 1 and adjust the "sole author" framing to "sole PI, sponsored by [name]."
3. `[ ]` Confirm current program URL and form. Google has moved this program between surfaces (`cloud.google.com/edu`, `ai.google.dev`, Kaggle) more than once.
4. `[ ]` If GCP Cloud credits are separately available and this program covers both API and compute, decide whether to raise the ask to include arm N nested-virt host compute (~$300 additional).
5. `[ ]` Add phone number and LinkedIn URL (Section 8).
6. `[ ]` Add a Google Cloud billing account ID if the form requires one (Section 8).
7. `[ ]` Decide whether to name prior industry employers; draft currently keeps them generic.
8. `[ ]` If the form has a Gemini-version dropdown, request Gemini 3 with the pre-registered fallback to Gemini 2.5 Pro if 3 is not on the researcher account (per ADR-002).
9. `[ ]` Verify arXiv IDs against the proposal: SandboxEscapeBench (2603.02277), Instrumental Choices (2605.06490), Krakovna et al. honeypot (2605.29729), PropensityBench (2511.20703).
10. `[ ]` Consider whether to CC or reference the DeepMind alignment team (Krakovna, Lindner, Ho, Farquhar, Shah) as domain contacts — the study is a direct methodological extension of their honeypot line. Only do this if you have a warm channel; a cold reference could read as name-dropping.
