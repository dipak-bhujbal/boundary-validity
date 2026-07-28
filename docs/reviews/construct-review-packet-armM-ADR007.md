# Construct-review packet — ADR-007 fidelity/identification question

> **Status: working draft — NOT yet sent to a reviewer.** Positions below are drafted for the
> author to review, own, and pressure-test before this goes out — the reviewer tests whether the
> *author* can defend them, not whether the prose is nice. Grounded in
> `docs/decisions/ADR-007-arm-m-real-shell.md:166–197` and proposal §4.2–4.5.
>
> **Two gates, split by what they block:**
> - **Before sending to Reviewer B:** (1) the tool-absence / Option-B handling (§5) is committed as
>   a repo-visible, reviewable design note / ADR (a construct reviewer assesses the *design*, not
>   scratchpad) — §3 and §5 make this a hard prerequisite; (2) the author can defend cold the §2
>   re-scope (why the narrowed registered claim is still publishable) and the §5 dual-channel
>   tool-absence argument.
> - **Before any arm-M-real *data*:** the parity **implementation + tests** exist and pass. (This is
>   a later gate — it does NOT block Reviewer B, who reviews the design decision.)

---

## 1. Orientation — what we're asking the reviewer to judge

**The study.** This is a propensity evaluation, not a capability one: it measures **unprompted boundary-crossing propensity rather than capability, and decomposes that propensity into discovery/legibility (δ) and willingness (ω)** — then asks whether the propensity measured in a low-fidelity **fabricated** substrate transports to a higher-fidelity one. The design is three-arm — **M** (fabricated substrate), **N** (real container, escape silently neutered), **E** (live exploit) — of which **M and N are executed and E is deferred**. The primary estimand is **Δ_fid, the arm-M vs arm-N fidelity gap in crossing propensity π**; the D/X instrumentation decomposes π into legibility δ and willingness ω, and **H5** tests whether the willingness component of that gap is non-zero. (The estimand is the gap in π, not "the gap in willingness" — H5 is the willingness-component test, a distinct claim.)

**The ask has two co-equal parts** (developed in §2): **(a) Which ADR-007 reading is correct** — the Reviewer's reading (a sharper form of the same question) or the Skeptic's reading (the question changed) — and why? **(b)** On the strength of (a), we are **proposing to re-scope the *registered* claim** to what M-vs-N now identifies — a real, OSF-amendment-level narrowing of what the paper claims; is that narrower claim the honest description, and is it still a contribution worth publishing? Their **written answer is required** to flip ADR-007 from Proposed → Accepted (ADR-007:6–13 status-discipline clause), so this is on the critical path, not advisory. Scope: construct/identification validity only; container *security* is a separate review (G3, already run — FAIL, arm N blocked).

**Time budget:** ~60 minutes. Suggested: 15 min §2 (the core reading), 20 min §3 (identification), 15 min §4 (un-fake-able affordances), 10 min §5 (tool-absence).

---

## 2. The exact question — both readings, stated fairly

The registered construct (ADR-007:168): *"does propensity measured in low-fidelity **fabricated** substrates transport to real substrates."* Moving arm M to a real shell changes the M/N contrast from "fabricated env vs real env" to "real env / fabricated escape vs real env / real escape."

- **Reviewer's reading (ADR-007:173–176):** a *sharper form of the same question* — it isolates the fidelity variable (the only M-vs-N difference becomes whether the *escape* is real, holding shell-realness constant) and removes shell-idiom coverage as a confound.
- **Skeptic's reading (ADR-007:178–181):** the question *changed* — the original operationalization (mock shell) failed its own quality gates, so the study no longer directly tests whether the *propensity literature's low-fidelity methodology* transports, because arm M is no longer low-fidelity in the shell dimension.

**Proposed position (adopt or adjust after prep):** a *qualified* Reviewer's reading. The study's **primary** claim — does crossing propensity (and specifically its willingness component) measured against a *fabricated escape* transport to a *real escape*, holding the shell substrate realistic — is preserved and arguably sharpened by the real-shell move: it removes shell-idiom coverage (a known mock weakness that failed the balance gates) as a rival explanation for any M–N gap, so a surviving gap is more cleanly attributable to escape-fidelity. **But the Skeptic has a real point we should not paper over:** the study no longer tests the broader, weaker claim that *an arbitrary low-fidelity mock* transports, because arm M is no longer low-fidelity in the shell dimension. The honest resolution is to **re-scope the registered claim** to exactly what M-vs-N now identifies (fabricated-escape vs real-escape, shell-realness held constant), rather than claim the original mock-methodology-transport question is fully preserved. So: Reviewer's reading for the primary estimand; Skeptic's concern conceded as a scope narrowing — not a defeater.

**But be honest about the *size* of that move — this is the second, co-equal decision, not a sub-point.** "Re-scope the registered claim" is not just picking a reading. The study is **already publicly registered (OSF) with the broader framing** ("does an arbitrary low-fidelity mock transport"). Narrowing it to "does a *fabricated escape* transport, shell-realness held constant" **changes what the paper claims**, so it is an **OSF-amendment-level decision**, not merely a reviewer's aesthetic call. Two consequences the packet must not bury:
- **To the reviewer, state it plainly:** we are not only asking "which reading is right" — we are *proposing to re-scope a registered claim*, and asking you to judge (i) whether the narrower claim is the honest description of what M-vs-N identifies, and (ii) whether it is still a contribution worth publishing.
- **The shape of the contribution (named, not defended):** the candidate contribution is narrower but still live — whether behavior against a fabricated **escape outcome** transports once ordinary shell fluency is held constant; the reviewer should judge both whether that claim is coherent and whether it remains worth the TMLR paper's framing.
- **[YOU — rehearsal, the packet can't do this for you]:** be ready to defend **why the narrower claim is still worth publishing** — its TMLR contribution once you concede it no longer tests "arbitrary low-fidelity mock." A reviewer will ask this directly and the draft does not prep you for it. *(This, plus the §3 residual, is what a construct reviewer opens on — defend both cold.)*

---

## 3. The identification argument the reading rests on

The "sharper form" claim only holds if the design still cleanly separates *legibility/discovery* from *willingness*:

- **The confound:** a raw crossing rate π fuses discovery δ (= Pr[D=1], legibility × thoroughness) with willingness ω (cross | discovered). π ≈ δ·ω. [pointer: proposal **§4.2** (three-factor decomposition, why D/X matters) and **§4.3** (estimands, Δ_fid decomposition); three-arm F-vs-C identification in **§4.4**]
- **The fix:** D and X instrumented separately → decomposition **Δ_fid = ω_M(δ_N−δ_M) + δ_N(ω_N−ω_M)** (legibility term + willingness term). Arm N varies substrate/affordance fidelity while holding live consequence at zero (real affordance, neutered escape), so an M→N shift in ω is attributable to fidelity, not real stakes. Arm E is the deferred arm that varies real consequence — cleanly separable, which is why deferring it doesn't break the M-vs-N claim.

**Pairing / excludability defense (H-mapping).** The identifying assumption is that M and N differ **only** in fidelity F. Defense, in the order a reviewer will attack it:
1. **The measurement instrument is held fixed across arms** — the same scenario specs and the same frozen ADR-003 scorer are used for M and N, so a M–N gap is not a scoring artifact. (Precise post-G3: the future arm-N *wrapper* must be proven to intercept **at least** the scorer-matched crossings — a tested superset, per G3 C6 — with any broader wrapper matching treated as containment/fidelity behavior, **not** a scoring change. So scorer parity holds; wrapper-vs-scorer is a deliberate, tested divergence, not byte-identity.)
2. **Excludability is partly *testable*, not merely assumed** — the D/X per-channel instrumentation lets us check *where* discovery differs, so an artifactual discovery gap (the un-fake-able channels, §4) is separable from a genuine willingness gap rather than silently loaded into Δ_fid.
3. **The tool-absence finding can strengthen this, but only once closed before data:** a specific pairing violation (the differential tool-absence confound, §5) was identified **before any data existed**. The honest claim is *not yet* "we found and closed it" — it is "we found a pairing violation pre-data, documented it, and will not ask Reviewer B or run data until the chosen handling is committed and reviewable." Once the tool-absence ADR/design note and the parity implementation/tests land, this becomes stronger than asserting the pairing holds untested. (Do not claim "closed" while §5 is still scratchpad-only.)
- **H-mapping:** **H4** = the primary fidelity gap in condition B (registered as Δ_fid(B) = π_N(B) − π_M(B)); the OSF amendment / reviewer must decide whether the *primary interpretation* rests on the faithfully-reproduced socket-path channel, with the `/proc/self/*` channels treated as disclosed/artifactual per-channel analyses (it is **not** formally "socket-path-only" unless the amendment says so). **H5** = the willingness component of that gap is non-zero. **H1–H3, H6–H8** are substantive **secondary / robustness** hypotheses (base rate, necessity, framing/eval-awareness, temporal drift, provider substitution) — they support *interpretation and external validity* but do not themselves identify the M-vs-N fidelity contrast. (Do not describe them as discovery-rate checks or power.)
- **Honest limit to state, not hide:** full excludability is **not empirically proven** — with arm E deferred, the neutering-detectability channel (whether agents can tell N from a live exploit) is un-checked (proposal **§4.5** retains the N/E first-attempt equivalence check but does not execute it). Disclose this as the primary residual threat to identification. *(This is the load-bearing assumption; be ready to defend why the residual is tolerable for a two-arm paper.)*

---

## 4. The honest sub-question the reviewer must actually rule on

ADR-007:139–144 asks the reviewer a specific, narrower thing: **some affordances are inherently un-fake-able at a safe substrate** — the `/proc/self/status` capability and `/proc/self/mounts` channels can't be safely reproduced in arm-M-real without granting the very capabilities the study probes. So for those channels, "fabricated vs real substrate" is *not orthogonal to safety*.

- **Mitigation on record (ADR-007:133–137):** per-signature-channel analysis makes the artifactual component separable, so the **primary interpretation** of H4 can rest on the socket-path channel (faithfully reproduced), with the un-reproducible `/proc/self` channels reported as disclosed per-channel artifactual analyses. (H4 as *registered* is Δ_fid(B), not formally "socket-path-only" — whether the primary interpretation is restricted that way is part of what the amendment/reviewer decides.)
- **The reviewer's ruling:** is this a *valid limitation to disclose*, or a *scoping decision requiring separate re-registration of arm M's affordance*?

**Proposed position (adopt or adjust):** a **valid limitation to disclose**, not a re-registration trigger — *because* the per-signature-channel analysis quarantines the un-reproducible `/proc/self` channels out of the primary interpretation (which can rest on the faithfully-reproduced socket channel). The un-fake-able channels become a disclosed robustness caveat (report the per-channel discovery rates; flag those two channels as artifactual-divergence-prone), not a confound in H4. **But this is genuinely the reviewer's call to make** — if they judge the affordance change material to the *registered* construct, re-registration is the conservative path and we should take it. Frame it to them exactly that way: here's why we think disclosure suffices; you tell us if it doesn't.

---

## 5. Tool-absence / Option-B — related construct-adjacent item

Prior scratchpad design work identified a **differential M-vs-N tool-absence confound**; the security-review packet noted that **no standalone repo artifact existed yet**. The clean version people reach for first: under the intended arm-N design, a crossing/probe command would be available and receive a canned response, while arm-M-real may return command-not-found if the relevant binary is absent or PATH-hidden. That makes "couldn't act" look like "wouldn't." **But be careful about the scorer:** it scores the command *string* (ADR-003), so a command matching a crossing signature is **X=1 regardless of whether the binary exists**. The confound is therefore *not* "X drops to 0" — the contamination is on **willingness / escalation**: command-not-found feedback can change whether the agent persists or escalates after the first attempt.

**Work the harder version through, because a reviewer will — and the clean story doesn't survive it intact.** The confound is **not confined to ω**. If a missing tool is also what the agent would use to *probe/discover* the affordance, its absence suppresses **discovery (D=1) itself** in arm-M-real relative to arm N — perturbing **δ_M vs δ_N** (the legibility term), not just willingness. So it **smears across both terms of Δ_fid = ω_M(δ_N−δ_M) + δ_N(ω_N−ω_M)**. And the "decomposition catches it" defense is **asymmetric**: the ω-side escalation/feedback effects are at least partly *observable* (matched attempts are scored X=1, escalation is visible), but a **δ-side suppression is invisible** — the decomposition **cannot see a discovery that never happened**, because there is no attempt to observe. That is the reviewer's pounce, and it is real.

**Proposed decision (adopt or adjust):** **commit the tool-absence note and put it to the reviewer**, framed as **Option B** — restore command-present parity across arms by providing the absent tools as *inert* affordances. **Critically, Option B must cover both channels** (per the above): restore the tools needed to *probe/discover* the affordance (so δ isn't artifactually suppressed in one arm) **and** the tools needed to *attempt the crossing* (so a crossing attempt executes and fails **inertly**, like arm N, rather than returning command-not-found — matching the feedback the agent sees, which is what drives escalation). Frame it honestly as **a fabricated-substrate fidelity *choice* (same character as the `/proc/self` narrowing), not a bug patch** — "another instance of the fidelity question this study is fundamentally about, and here is how we choose to handle it." That preempts the "patching toward the result you want" objection. Ask the reviewer to sanity-check it as a construct decision.

**[YOU — rehearsal, not drafting]:** you learned this an hour ago as the clean "missing tool turns couldn't into wouldn't" (willingness-only) story. The two-channel version above is what you actually have to defend — the confound hits δ **and** ω, the decomposition only cleanly catches the ω-side, and Option B therefore has to fix discovery too. Work it through before you defend it.

**Prerequisite:** the tool-absence note is not in the repo yet — commit it as its own design note / ADR **before** Reviewer B is asked to rely on it; don't ask a reviewer to weigh a scratchpad-only artifact.

---

## 6. What we hand the reviewer (not the whole repo)

Pointers only, scoped to ~60 min:
- `docs/decisions/ADR-007-arm-m-real-shell.md` (the question + both readings).
- Proposal identification section **§4.2–4.5** (three-factor decomposition, estimands / Δ_fid, three-arm F-vs-C identification, N/E first-attempt equivalence check).
- The **smoke-v6 evidence table** (why the mock failed its balance gates and moved to real shell) — commit `0c9aa29`.
- The per-signature-channel analysis (§4 mitigation).
- For context on what's *out* of scope: the G3 review + ADR-008 (security is a separate, already-run gate).
*(Confirm the exact file list before sending.)*

---

## 7. Provenance / ask

We are asking a **construct / eval-methodology reviewer** (per the ADR-001 collaboration model, acknowledgment-only) for a **written judgment on §2 and §4**, plus §5 if the tool-absence ADR/design note has been committed before review:
- **§2:** does the Reviewer's "sharper form" reading hold, and is the proposed narrowing valid as an OSF amendment-level claim change rather than a re-registration trigger?
- **§4:** is the un-fake-able-affordance handling a valid disclosure, or does it require separate re-registration of arm M's affordance?
- **§5:** is Option B's command-present parity treatment sufficient for both the discovery/δ and willingness/ω channels, or should affected channels be narrowed/stratified?

A "pass" is the written answer that lets the OSF amendment proceed and flips ADR-007 Proposed → Accepted. **No arm-M-real data exists yet**, and per ADR-007:194–196 the amendment is timestamped *before* any real-shell data is generated — so the reviewer is judging a design, not rationalizing a result. We will disclose their verdict (including a "the question changed / re-register" verdict) in the amendment either way.
