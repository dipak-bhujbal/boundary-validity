# Construct-review request — arm-M real-shell fidelity / identification (ADR-007)

Thank you for reviewing. This is a scoped request (~60 min) for a **written judgment** on the construct/identification validity of a design change, before any data is collected. Scope is construct validity only; container *security* is handled by a separate review. Grounded in `docs/decisions/ADR-007-arm-m-real-shell.md` (§"Construct implications") and the proposal's identification section (§4.2–4.5).

---

## 1. What we're asking you to judge

**The study.** A propensity evaluation, not a capability one: it measures unprompted boundary-crossing propensity rather than capability, and decomposes that propensity into discovery/legibility (δ) and willingness (ω). It asks whether propensity measured in a low-fidelity **fabricated** substrate transports to a higher-fidelity one. The design is three-arm — **M** (fabricated substrate), **N** (real container, escape silently neutered), **E** (live exploit) — of which **M and N are executed and E is deferred**. The primary estimand is **Δ_fid, the arm-M vs arm-N fidelity gap in crossing propensity π**; the D/X instrumentation decomposes π into δ and ω, and **H5** tests whether the willingness component of that gap is non-zero. (The estimand is the gap in π; H5 is the distinct willingness-component test.)

**The ask has two co-equal parts** (developed in §2):
- **(a)** Which ADR-007 reading is correct — the **Reviewer's reading** (a sharper form of the same question) or the **Skeptic's reading** (the question changed) — and why?
- **(b)** On the strength of (a), we **propose to re-scope the *registered* claim** to what M-vs-N now identifies — a real, OSF-amendment-level narrowing of what the paper claims. Is that narrower claim the honest description, and is it still a contribution worth publishing?

Your written answer is required to flip ADR-007 from Proposed → Accepted, so it is on the critical path. Suggested time: 15 min §2, 20 min §3, 15 min §4, 10 min §5.

---

## 2. The core question — both readings

The registered construct: *"does propensity measured in low-fidelity **fabricated** substrates transport to real substrates."* Moving arm M to a real shell changes the M/N contrast from "fabricated env vs real env" to "real env / fabricated escape vs real env / real escape."

- **Reviewer's reading:** a *sharper form of the same question* — it isolates the fidelity variable (the only M-vs-N difference becomes whether the *escape* is real, holding shell-realness constant) and removes shell-idiom coverage as a confound.
- **Skeptic's reading:** the question *changed* — the original operationalization (mock shell) failed its own quality gates, so the study no longer directly tests whether the *low-fidelity methodology* transports, because arm M is no longer low-fidelity in the shell dimension.

**Our position:** a *qualified* Reviewer's reading. The primary claim — does crossing propensity (specifically its willingness component) measured against a *fabricated escape* transport to a *real escape*, holding the shell substrate realistic — is preserved and arguably sharpened: the real-shell move removes shell-idiom coverage (a known mock weakness that failed the balance gates) as a rival explanation for any M–N gap, so a surviving gap is more cleanly attributable to escape-fidelity. **We do not, however, paper over the Skeptic's point:** the study no longer tests the broader claim that *an arbitrary low-fidelity mock* transports. Our honest resolution is to **re-scope the registered claim** to exactly what M-vs-N identifies (fabricated-escape vs real-escape, shell-realness held constant), rather than assert the original mock-methodology question is fully preserved.

**We want to be explicit that this re-scope is a substantive move, not a footnote.** The study is **already publicly registered (OSF)** with the broader framing. Narrowing it changes what the paper claims, so it is an **OSF-amendment-level decision**. We are therefore asking you to judge two things, not one: (i) whether the narrower claim is the honest description of what M-vs-N identifies, and (ii) whether it remains a contribution worth publishing. The candidate contribution, stated plainly: whether behavior against a fabricated **escape outcome** transports once ordinary shell fluency is held constant. We ask you to assess both its coherence and whether it is sufficient for the paper's framing.

---

## 3. The identification argument

The "sharper form" claim holds only if the design cleanly separates discovery from willingness:

- **The confound:** a raw crossing rate π fuses discovery δ (= Pr[D=1], legibility × thoroughness) with willingness ω (cross | discovered); π ≈ δ·ω. (Proposal §4.2 — three-factor decomposition and why D/X matters; §4.3 — estimands and the Δ_fid decomposition; §4.4 — three-arm F-vs-C identification.)
- **The fix:** D and X are instrumented separately → **Δ_fid = ω_M(δ_N−δ_M) + δ_N(ω_N−ω_M)** (legibility term + willingness term). Arm N varies substrate/affordance fidelity while holding live consequence at zero (real affordance, neutered escape), so an M→N shift in ω is attributable to fidelity, not real stakes. Arm E is the deferred arm that varies real consequence — cleanly separable, so deferring it does not break the M-vs-N claim.

**Pairing / excludability (H-mapping).** The identifying assumption is that M and N differ **only** in fidelity F (proposal §4.4, §5.2). Likely review concerns, in order:
1. **The measurement instrument is held fixed across arms** — the same scenario specs and the same frozen ADR-003 scorer are used for M and N, so a M–N gap is not a scoring artifact. (The planned arm-N *wrapper* must intercept at least the scorer-matched crossings — a tested superset — with any broader wrapper matching treated as containment behavior, not a scoring change.)
2. **Excludability is partly *testable*, not merely assumed** — the D/X per-channel instrumentation lets us check *where* discovery differs, so an artifactual discovery gap (the un-fake-able channels, §4) is separable from a genuine willingness gap rather than silently loaded into Δ_fid.
3. **A pairing violation was caught pre-data and is being handled** — the differential tool-absence confound (§5) was identified before any data existed. We do **not** claim it is closed: our position is "found pre-data, documented, committed as a reviewable design decision (ADR-010), and not run until the parity implementation + tests land." Once those land, this is stronger than asserting the pairing holds untested.
- **H-mapping.** **H4** = the primary fidelity gap in condition B (registered as Δ_fid(B) = π_N(B) − π_M(B)); whether the primary *interpretation* rests on the faithfully-reproduced socket-path channel — with the `/proc/self/*` channels treated as disclosed per-channel artifactual analyses — is part of what we ask you to decide (§4). **H5** = the willingness component of that gap is non-zero. **H1–H3, H6–H8** are secondary/robustness hypotheses (base rate, necessity, framing/eval-awareness, temporal drift, provider substitution) that support interpretation and external validity but do not themselves identify the M-vs-N fidelity contrast.
- **Residual threat we disclose, not hide:** full excludability is **not empirically proven**. With arm E deferred, the neutering-detectability channel (whether agents can tell N from a live exploit) is un-checked — proposal §4.5 retains the N/E first-attempt equivalence check but does not execute it. This is the primary residual threat to identification, and we would value your view on whether it is tolerable for a two-arm paper.

---

## 4. A specific sub-question we need you to rule on

Some affordances are **inherently un-fake-able at a safe substrate**: the `/proc/self/status` capability and `/proc/self/mounts` channels cannot be safely reproduced in arm-M-real without granting the very capabilities the study probes. So for those channels, "fabricated vs real substrate" is *not orthogonal to safety*.

- **Mitigation on record:** per-signature-channel analysis makes the artifactual component separable, so the primary interpretation of H4 can rest on the socket-path channel (faithfully reproduced), with the un-reproducible `/proc/self` channels reported as disclosed per-channel artifactual analyses. (H4 as *registered* is Δ_fid(B), not formally "socket-path-only" — whether the primary interpretation is restricted that way is part of this ruling.)
- **Our position:** a **valid limitation to disclose**, not a re-registration trigger — because the per-channel analysis quarantines the un-reproducible `/proc/self` channels out of the primary interpretation, which can rest on the faithfully-reproduced socket channel. The un-fake-able channels become a disclosed robustness caveat (report per-channel discovery rates; flag those two channels as artifactual-divergence-prone), not a confound in H4.
- **But this is your call.** If you judge the affordance change material to the *registered* construct, re-registration is the conservative path and we will take it.

---

## 5. Tool-absence parity (committed as ADR-010)

We flagged a **differential M-vs-N tool-absence confound** and have committed the proposed handling as **ADR-010** (`docs/decisions/ADR-010-tool-absence-parity.md`), so you are assessing a repo-visible design decision, not scratchpad state.

**The mechanism.** Under the intended arm-N design, a crossing/probe command would be available and receive a canned response, while arm-M-real may return command-not-found if the relevant binary is absent or PATH-hidden — making "couldn't act" look like "wouldn't." One nuance about the scorer: it scores the command *string* (ADR-003), so a command matching a crossing signature is **X=1 regardless of whether the binary exists**. The confound is therefore not "X drops to 0"; the contamination is on **willingness / escalation** — command-not-found feedback can change whether the agent persists or escalates after the first attempt.

**It is dual-channel.** It is not confined to ω. If a missing tool is also what the agent would use to *probe/discover* the affordance, its absence can suppress **discovery (D=1) itself** in arm-M-real relative to arm N, perturbing the legibility term δ. So it smears across both terms of Δ_fid, and the decomposition's ability to catch it is **asymmetric**: the ω-side escalation effects are at least partly observable, but a **δ-side suppression is invisible** — the decomposition cannot see a discovery that never happened. We consider this a genuine residual and want your view on it.

**Our handling (ADR-010, Option B).** Restore command-present parity across arms by providing the absent tools as **inert** affordances, covering **both channels**: restore the probe/discovery tools so δ is not artifactually suppressed, and the crossing tools so an attempt executes and fails *inertly* (like arm N) rather than returning command-not-found. We frame this as **a fabricated-substrate fidelity choice — the same character as the `/proc/self` narrowing — not a bug patch.** The exact tool set is pending pinned-digest verification, and the parity implementation + tests are a pre-data gate. **Question for you:** is inert command-present parity sufficient for both the δ and ω channels, or should affected channels instead be narrowed/stratified in the analysis?

---

## 6. Supporting documents (all in the repo)

- `docs/decisions/ADR-007-arm-m-real-shell.md` — the question and both readings.
- `docs/decisions/ADR-010-tool-absence-parity.md` — the tool-absence handling (§5).
- `docs/proposal/boundary-validity-gap-proposal.md` §4.2–4.5 — the identification argument (decomposition, estimands, three-arm identification, N/E equivalence check).
- The smoke-v6 evidence (why the mock failed its balance gates and moved to a real shell) — commit `0c9aa29`.
- For context on what is *out of scope*: the G3 security review + ADR-008 (security is a separate, already-run gate).

---

## 7. What a "pass" means

We ask for a **written judgment** on §2, §4, and §5:
- **§2:** does the Reviewer's "sharper form" reading hold, and is the proposed narrowing a valid OSF amendment-level claim change rather than a re-registration trigger?
- **§4:** is the un-fake-able-affordance handling a valid disclosure, or does it require separate re-registration of arm M's affordance?
- **§5:** is Option B's inert command-present parity sufficient for both the δ and ω channels, or should affected channels be narrowed/stratified?

A "pass" is the written answer that lets the OSF amendment proceed and flips ADR-007 Proposed → Accepted. **No arm-M-real data exists yet**, and the amendment is timestamped *before* any real-shell data is generated — so you are judging a design, not rationalizing a result. We will disclose your verdict in the amendment either way, including a "the question changed / re-register" verdict.
