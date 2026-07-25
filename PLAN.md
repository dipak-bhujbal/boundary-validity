# PLAN — boundary-validity

Live plan through TMLR submission. 16 solo weeks to submission, +6-week median first decision. Amend in-place as the project progresses; do not delete history — supersede.

## Milestones

| Phase | Weeks | Deliverable | Cost gate |
|:--|:--|:--|:--|
| 0 Foundation | 1 | Repo, ADR-000/001/002, PLAN, LICENSE, .gitignore | $0 |
| 1 Pre-registration | 2 | 7 scenario specs (A–G), command contract v1, OSF pre-reg timestamped, research-credit applications submitted, cloud-provider AUP pre-registration sent | $0 |
| 2 Arm M harness | 3–4 | Inspect AI mock-shell harness, Phase 0 SandboxEscapeBench calibration on panel, eval-awareness scanner | ~$100 |
| 3 Arm M pilot | 5 | 20 ep/cell × 3 cond × 5 models pilot, Cohen κ ≥ 0.80 scorer gate, contract v2 | ~$30 |
| 4 Arm M full run | 6 | 10,500 episodes (7 cond × mixed n × 5 models), checkpointed | ~$500 |
| 5 Arm M analysis | 7–8 | Hierarchical Bayesian fit, per-model report, decomposition, bounded-nulls, workshop-length interim tech report | $0 |
| 6 Arm N design | 9 | Neutering-wrapper spec (intercept-and-fake), containment ADR, cloud host chosen (c8i vs GCP), abuse-team clearance confirmed | ~$0 |
| 7 Arm N harness | 10–11 | Nested-virt harness, silent-neutering layer with unit tests, network-egress alerting, informal design review | ~$50 |
| 8 Arm N pilot | 12 | 20 ep/cell × conditions B, F × 3 models pilot, equivalence check on §4.5 leak-test | ~$30 |
| 9 Arm N full run | 13 | ~6,000 episodes (cond B, F × 5 models × 300 ep, adaptive) | ~$300 |
| 10 Full analysis | 14 | Fidelity-gap fit, decomposition into legibility vs willingness, drift subset re-run, provider-substitution audit | $0 |
| 11 Manuscript | 15 | TMLR-format draft, reproducibility statement, ethics + containment appendix, limitations | $0 |
| 12 Submission | 16 | External review from acknowledged reviewers, final revisions, OpenReview submission | ~$0 |

Gross budget target: **$900** (with research credits: ~$400 out-of-pocket).

## Cost-per-bit discipline (inherited from llama-tools)

- Any pilot with 0 crossings across all conditions → cap that model at 100 ep total, report bounded null via rule of three.
- Any model at frontier-tier API cost gets 100 ep/cell by default; escalate to 300 only in conditions where pilot shows signal.
- Kill any experiment that costs more than $50 per bit of expected reportable finding, unless load-bearing for the primary estimand.

## Gates that pause execution

- **G1 (end week 2):** OSF pre-registration timestamped and abuse-team clearance email sent. No spend until both are green.
- **G2 (end week 5):** Cohen κ ≥ 0.80 on scorer against hand adjudication. If not met, revise contract before full-run spend.
- **G3 (end week 9):** Neutering-wrapper reviewed informally and network-egress alerting verified. No arm N execution until both are green.
- **G4 (end week 14):** If arm N fidelity gap is null with bound above 3 pts, publish anyway (bounded-null is a result); do not chase power.

## Non-goals

- Arm E (live exploit): explicitly out of scope for this paper. See ADR-001.
- New exploit development: use SandboxEscapeBench published suite only.
- Interpretability: branching-entropy attribution is at most a section, not a claim.
- SOTA comparisons: TMLR does not require, not this paper's contribution.

## Log

Append-only. Do not edit past entries; add corrections as new entries.

- **2026-07-25** — Repo created. Scaffold committed. Panel locked (Opus 4.7, GPT-5.5, Gemini 3, Llama-3.1-70B, Qwen 3). Scope reduced from three-arm to M+N after TMLR-fit audit and second-advisor review. See ADR-000, ADR-001, ADR-002.
- **2026-07-25** — Week 1 completed same day. Independent adversarial review conducted; all 3 §2 load-bearing items and 9/10 §3 should-fix items resolved. Test suite at 52 passing (scorer + schema + adversarial regressions). Panel updated to Llama-4. ADRs 003, 004, 005 shipped; scenarios A-G committed; scorer + CLI + schema validator live. Manual-review flag for obfuscation added to scoring contract.
- **2026-07-25** — Week 2 OSF submission prep started. Blob hashes populated in OSF draft; ADR-004/005 added to pinned decision records; `docs/pre-registration/SUBMISSION.md` SOP written; `docs/pre-registration/manifest.md` generated (49 files); `scripts/gen-manifest.py` for regeneration. Pandoc→PDF pipeline verified pending xelatex install.
