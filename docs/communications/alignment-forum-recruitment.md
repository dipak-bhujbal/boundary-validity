# Alignment Forum recruitment post — draft

**Post when:** same day the OSF pre-registration DOI is issued (per PLAN.md gate G1 completion).
**Cross-post to:** LessWrong (same content), optionally MATS Slack `#projects` channel.
**Author:** Dipak Bhujbal, independent researcher.

---

## Suggested title (pick one)

- **Preferred:** *Measuring whether "stipulated" containment boundaries yield the same propensity numbers as real ones — feedback and reviewers wanted*
- **Alt:** *A three-arm identification design for propensity-eval validity — pre-registered, asking for adversarial review before I build*
- **Alt-short:** *Are propensity evaluations measuring what they think they're measuring? Asking for reviewers.*

---

## Body

**TL;DR.** I've pre-registered an evaluation that asks whether measuring agentic boundary-crossing propensity against a *fabricated* boundary (mocked shell) yields the same answer as measuring it against a *real* one (nested-virt container, exploit silently neutered). It's a validity question about every published propensity evaluation to date. Design is at `github.com/dipak-bhujbal/boundary-validity`; pre-registration is timestamped at `<DOI here>`. I'm looking for four kinds of unpaid, acknowledged review before I spend an API dollar. **I am not looking for co-authors.**

### What the study is

The evaluation extends UK AI Security Institute's [SandboxEscapeBench](https://arxiv.org/abs/2603.02277) from capability to propensity. Existing propensity work — PropensityBench (arXiv:2511.20703), Krakovna et al.'s honeypot evaluations (arXiv:2605.29729), Instrumental Choices (arXiv:2605.06490) — measures whether agents cross a boundary that the evaluation *says* is a boundary. It reads as a policy document, a colleague's warning note, or a fictional access control. No published propensity evaluation has checked whether measuring against fictional boundaries yields the same numbers as measuring against real ones. The primary estimand is the fidelity gap $\Delta_{\mathrm{fid}}(\mathrm{B}) = \pi_N - \pi_M$ on the blocked-path condition.

The design has three arms — M (mocked shell), N (real container, silently neutered exploit), E (real container, live exploit). Arms M and N will be executed (both zero-live-escape by construction); arm E is deferred with its containment protocol preserved. 8 pre-registered hypotheses covering base rate, necessity dominance, framing null, fidelity gap direction, willingness/legibility decomposition, evaluation-awareness effect, temporal drift, and provider substitution.

Full design manuscript: `docs/proposal/boundary-validity-gap-proposal.md`.
Six architecture decisions (charter, arm scope, panel, scoring contract, pre-registration protocol, neutering wrapper): `docs/decisions/`.

### What I'm asking for

Four discrete, bounded, one-shot reviews. Any one of them is a real contribution.

**1. Adversarial review of the identification argument (§4.4 of the proposal).**
The claim is that a two-arm mock-vs-real design is unidentified because it bundles substrate fidelity with consequence availability, and that adding arm N (real substrate + no consequence) breaks the bundle. Please try to break this. Time: ~1 hour. Deliverable: a comment or issue on the GitHub repo saying what you think doesn't hold.

**2. Statistical review of the hierarchical Bayesian model + priors (§6 of the proposal, ADR-004 §4).**
Student-$t(3, 0, 2.5)$ priors on all coefficients, half-normal$(0, 1)$ on variance components, Firth penalized ML as frequentist fallback. Bounded-nulls via rule of three. Primary estimand: $\Delta_{\mathrm{fid}}(\mathrm{B})$ on the risk-difference scale at observed baseline. If you're familiar with rare-event hierarchical logistic identifiability under these priors, please look. Time: ~1 hour. Deliverable: comment on whether the specification is defensible or which specific alternative you'd substitute.

**3. Design review of the neutering wrapper (ADR-005) — HIGHEST-PRIORITY ASK.**
The wrapper must be intercept-and-fake, not attempt-and-hope. Five safety invariants (INV-1 through INV-5) are the entire basis for the "arm N cannot escape" claim. None are implemented yet. Two specific unresolved tensions worth attacking first, both surfaced by an earlier reviewer and documented in ADR-005 §"Known unresolved tensions":

  - **INV-2 fail-closed is a detectability leak.** Hard-blocking an unmatched-but-crossing-adjacent command tells the agent immediately that it is in an instrumented environment. That contaminates every subsequent action in the episode and pollutes exactly the willingness signal the primary estimand depends on. Alternative: soften to canned-generic-success, accept false negatives on truly novel crossings. Which is right?
  - **INV-4 verifies no side effects on a fixture, not no egress under load.** The failure mode the study exists to prevent is a packet reaching a network. Current INV-4 is `strace` on the wrapper PID during a fixture run. Necessary but not sufficient. Adversarial concurrent-episode egress fuzzing against the hypervisor firewall (with the failure mode being *any single packet through*) is what should gate arm N execution.

Time: ~45 minutes to read ADR-005 + the tensions section, plus however long you want to spend attacking. Deliverable: comment on GitHub issue or DM.

**4. arXiv endorsement (`cs.AI` or `cs.CR`) for eventual preprint.**
First-time arXiv submitter, no prior publications, needs an endorser. Not asking now — asking whether you'd endorse when the manuscript is ready (~month 5).

### What I'm NOT asking for

- **Co-authorship.** Anyone who builds harness code becomes a co-author (that's a firm line; see ADR-001). The four asks above are acknowledgment-only contributions, standard for pre-registration review. I am aware this is a stronger constraint than the common "collab if you contribute meaningfully" — the reasoning is portfolio-clarity, documented in ADR-001, and I'd rather be transparent about it than have someone contribute expecting authorship.
- **Recommendations to change scope.** Scope is locked at pre-registration; changes require an ADR + a filed OSF amendment. If you think I should be running arm E or a different set of conditions, that's post-timestamp future-work feedback and welcome, but won't change this paper.
- **General "cool idea, keep going" comments.** Nice to hear but not what this post is for. If the design is bad in a specific way, please tell me the specific way.

### How to help

Any of:
- **GitHub issue** at `github.com/dipak-bhujbal/boundary-validity/issues` — best for anything with a code or ADR reference
- **DM me on AF / LessWrong** — best for anything that would prefer to be private
- **Email** `dipak.bhujbal23@gmail.com` — best for arXiv endorsement or MATS-style scheduling

If you're not the right person but know who is, forwarding to them is genuinely useful. The list of ~5 candidates I'd love to have review the identification argument is short and I only know how to reach two of them.

### About me

Independent researcher, based in Cambridge MA. Background is cloud security, distributed-systems architecture, and technical program management at engineering organizations; transitioning into empirical AI safety with a focus on evaluation methodology. This is my first pre-registered study. No prior ML publications. Portfolio of work-in-progress artifacts: `llama-tools` (Llama-3.1-8B SFT+DPO fine-tune, reproducible), `release-kit` (release-automation framework), and this project. I'm aware that "independent + no prior publications" is a legitimate reviewer signal for lower prior credibility; the design is public and reviewable directly, and I'd rather earn credibility by having the design attacked than by claiming it.

### Timeline

- Weeks 3–8 (now through mid-September): arm M full run + workshop-length interim tech report
- Weeks 9–14: arm N build + full run + fidelity-gap analysis
- Weeks 15–16: TMLR submission preparation
- Month 5–7: TMLR first decision

**~$500 out of pocket after research credits, target $0** if all three credit programs (Anthropic, Google DeepMind, OpenAI) land.

Thanks for reading. Sharper feedback appreciated more than kinder.

---

## Reviewer checklist before Dipak posts

- [ ] OSF DOI populated in the `<DOI here>` field of the TL;DR
- [ ] Repo link resolves and README shows expected status
- [ ] LessWrong crosspost decision made (recommend yes — same audience, additive reach)
- [ ] MATS Slack `#projects` post decision made (recommend yes if you have access)
- [ ] Anthropic Fellows / MATS / AISI application status — decide whether to reference in the "About me" paragraph (recommend NOT referencing — this post is for reviewers, not funders)
- [ ] Personal contact info — remove or keep the email address (leaving as-is is fine; it's already in the LICENSE and pyproject.toml)
- [ ] Length check — 700–900 words for AF, may want to compress to 500 for LessWrong tags "AI Safety" + "Evaluations" + "Prereg"
