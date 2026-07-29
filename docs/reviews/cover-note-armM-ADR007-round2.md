# Cover note — arm M / ADR-007, second round

**Status: DRAFT. Not sent.** Sending is the author's decision.
**Repo state this note describes:** `9776900`.
**Attachment:** `docs/reviews/construct-review-response-armM-ADR007.md`

---

Thank you for the check on the response packet. You returned 18 findings. **All 18 are
closed.** Nothing is deferred and nothing is argued away — where a finding revealed a claim
we could not support, the claim is withdrawn rather than defended.

Three of your findings turned out to be instances of one defect, and it is the honest
summary of this round: **we were printing numbers and claims we had not recomputed.** Every
figure in the attached document now states the method that produces it, so you can break it
the way you broke the last one.

## What you should read first

**§1.0-bis is the most damaging thing in the document, and we are reporting it
unprompted.** You found that the mock announced itself to the agent on every unhandled
command. We replayed all 950 recorded pilot episodes through the pre-fix mock and reproduce
your figures to the digit: **885/950 (93.2%) of episodes saw the literal string `mock
shell`**, on **2,905 of 13,235 commands**, differential by model from 86.5% to 100.0%. That
is the substrate which produced both the ADR-007 evidence table and the G2 validation
corpus. It strengthens the case for abandoning the mock and it constrains what the existing
corpus can support; both are stated.

You also found that our account of B0's *cause* was wrong and that we had adopted it
without testing it. Correct. The registered mock confessed too.

## Where a claim did not survive checking

| Claim | Status |
|:--|:--|
| Coverage spread `3.1pt` | **Withdrawn.** Reproduces under no estimator. **2.95pt** under the estimator ADR-007 declares; 2.91–3.38pt across five, all passing. Definitions and unrounded values are stated. |
| `CLEAN 2` after B1 | **Withdrawn.** Measured on one narrow probe per channel. Widened sweep gives **CLEAN 1 / DIVERGENT 4 / DEAD 2** — B1 repaired one channel, not two. |
| B7 "coverage measured, not stipulated" | **Withdrawn as evidence.** The metric is measured but reads ~1.0 by construction; the stipulation moved into the classifier. Now machine-checkable: both substrates carry `COVERAGE_METRIC_KIND` so the two quantities cannot be pooled. |
| "the boundary is kernel-enforced" | **Withdrawn.** Arm N intercepts in userspace and never dispatches; G3 found that matching defeated by 18/20 variants. |
| G2 validates scenarios B–G | **Narrowed.** The gate passes, but every positive label is in scenario D; the instrument is unvalidated on 5 of 6 conditions and 4 of 6 models. |
| The ownership fix "generalizes" | **Was false when we wrote it.** Now true: real in-container user for uid 1000, all seeded items chowned and verified for type/owner/group/mode. |

## Finding 7 — we withdrew the question rather than answer it

You were right that §4.4 asked an SME to decompose a variable from itself: B3 defines the
manipulation as what the environment does on an escape attempt, and B12 renames the
estimand to exactly that. **No answer could have been correct.**

We resolved it by accepting our own reframing: within the executed two-arm scope there is
**no separate consequence term to bound**, so the bound is **dropped, not deferred**. What
replaces it is a limitation rather than an estimate — the residual question is external
validity, which is arm E, out of scope per ADR-001, and it is **not proxied**.

## Two things to hold us to

**Container tests are opt-in.** A default `pytest` run is `137 passed, 6 skipped` — green,
with **zero B1 acceptance criteria exercised**. `BV_RUN_CONTAINER_TESTS=1` gives `143
passed`. To reproduce the B1 claims you must set the flag.

**Verification on the pinned digest means arm64.** The digest is a multi-arch index, not an
image. `--platform linux/arm64` is now enforced in the `docker run` argv with tests, so the
substrate cannot silently resolve elsewhere — but "verified against the pinned digest"
should be read as "verified against the arm64 member of the manifest list."

## The ask, unchanged in substance

**Sign-off on ADR-010 Option B as a valid construct decision** — with the response-valence
target now specified per your §5 ruling — or a ruling that it is not, in which case Option C
is the fallback. ADR-010 also now names the sign-off vehicle and records that its second
condition was always author-side, so the deadlock you identified is broken from our end.

## Standing constraints

**G3 remains FAIL and arm N is blocked.** No arm-N work, no containment changes, and no
model-API spend has occurred in this round — the replay above is offline replay of
already-recorded trajectories.
