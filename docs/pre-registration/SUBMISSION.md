# OSF Pre-registration Submission SOP

**Target:** `https://osf.io/prereg/`, format "Registered Report — Preregistration"
**Timing:** end of week 2 (per PLAN.md gate G1)
**Precondition:** all `[VERIFY]` fields resolved elsewhere in the repo; AUP emails already sent OR clearly staged for immediate follow-up post-timestamp
**Postcondition:** OSF DOI issued and committed back into `docs/pre-registration/osf-doi.md`

## Step-by-step

### 0. Working tree check (do first, before anything else)

```bash
git status                         # must show clean working tree
git log --oneline -5               # sanity-check what will be pinned
.venv/bin/pytest -q                # must show 52/52 pass
.venv/bin/boundary-validity validate data/scenarios/   # must show 7/7 ok
```

If any of these fail, resolve before proceeding. Do NOT submit on a dirty tree.

### 1. Freeze commit hash

```bash
git rev-parse HEAD > /tmp/prereg-commit-hash
cat /tmp/prereg-commit-hash
```

This is the value you enter on the OSF form as the pre-registered commit. It is NOT edited into the .md draft — the .md's `<REPO_COMMIT_HASH>` placeholder cannot self-reference (that would change its own hash). Enter the hash directly on the OSF form.

### 2. Convert draft to PDF

Two paths — the fast one is fine for OSF submission; the proper one is worth doing before the eventual arXiv/TMLR submission but not required now.

**Fast path (no install, ~30 seconds).** Pandoc → HTML → print-to-PDF from browser. OSF accepts this without complaint.

```bash
pandoc docs/pre-registration/osf-preregistration-draft.md \
    --from markdown --to html5 --standalone --mathjax \
    --toc --toc-depth=2 --number-sections \
    --metadata title="Boundary-Validity Pre-Registration (v0.1)" \
    --metadata author="Dipak Bhujbal" \
    --output /tmp/osf-preregistration-preview.html
open /tmp/osf-preregistration-preview.html      # Chrome or Safari
# In browser: File → Print → Destination: Save as PDF
# Save to: docs/pre-registration/osf-preregistration.pdf
```

**Proper path (LaTeX rendering; one-time ~5 minute install).** Do this before the arXiv/TMLR manuscript conversion.

```bash
brew install --cask basictex        # ~90 MB; adds xelatex to /Library/TeX
                                    # NOTE: requires admin password
sudo tlmgr update --self && sudo tlmgr install collection-latexrecommended
# Restart terminal or: eval "$(/usr/libexec/path_helper)"
```

Then convert:

```bash
# From the repo root:
pandoc docs/pre-registration/osf-preregistration-draft.md \
    --from markdown --to pdf \
    --pdf-engine=xelatex \
    --output docs/pre-registration/osf-preregistration.pdf \
    --metadata title="Boundary-Validity Pre-Registration (v0.1)" \
    --metadata author="Dipak Bhujbal" \
    --toc --toc-depth=2 --number-sections
```

Sanity-check the PDF opens and the manifest tables render cleanly.

### 3. Submit on OSF

1. Log in at `osf.io` (create account if needed; use `dipak.bhujbal23@gmail.com`).
2. Create a new project titled "Boundary-Validity: Measuring the Validity Gap in Propensity Evaluations of Agentic Boundary Crossing".
3. Under the project, click **Registrations → Add a New Registration**.
4. Choose form: **Registered Report — Preregistration**.
5. Upload `docs/pre-registration/osf-preregistration.pdf` as the primary attachment.
6. In the form's freeform fields, paste the corresponding sections from the markdown draft (OSF's forms mirror the same structure).
7. Enter the commit hash from Step 1 in every field that asks for "version" or "URL" — combine with the GitHub URL as `https://github.com/dipak-bhujbal/boundary-validity/tree/<hash>`.
8. Under "Associated resources", link:
    - GitHub repo (main branch AND the pinned commit URL)
    - The AUP pre-registration email threads once responses arrive (see `docs/communications/aup-pre-registration/`)
9. Submit for registration. OSF issues a DOI within ~24 hours.

### 4. Post-timestamp actions

Once the DOI is issued:

1. Create `docs/pre-registration/osf-doi.md` with the DOI, submission date, and pinned commit hash.
2. Commit and push — this commit is the FIRST post-registration commit. Its git message must say "Post-registration: OSF DOI issued as `<doi>` for commit `<hash>`".
3. Send the DOI as an addendum to the AWS and GCP AUP threads.
4. Reference the DOI in the abstract and footer of every subsequent artifact (README, applications, future preprint drafts).

### 5. Amendment procedure (post-timestamp)

Per ADR-004 §6, any change to a pre-registered artifact requires:

1. A new ADR in `docs/decisions/` explaining the change and its motivation.
2. A revised commit hash pinned in the amendment.
3. The amendment filed BEFORE the affected data is collected.
4. Update to the OSF record via the "Add an addendum" flow — do NOT edit the original registration.

Silent changes are the failure mode ADR-004 exists to prevent.

## Reviewer's pre-flight checklist

Before Step 3 (actual submission), confirm:

- [ ] All `[VERIFY]` flags in the OSF draft resolved (ICML claim, program URLs, addresses, phone)
- [ ] `docs/proposal/boundary-validity-gap-proposal.md` post-drafting-scope-changes preamble reflects current state
- [ ] AUP emails at `docs/communications/aup-pre-registration/` have their `[VERIFY]` addresses resolved
- [ ] Sample-size policy in ADR-002 matches OSF draft §3.5
- [ ] All 8 hypotheses (H1–H8) appear identically in ADR-004, OSF draft, and proposal §5.1
- [ ] Panel table matches across ADR-002, OSF draft §3.5, and proposal §5.5
- [ ] `boundary-validity validate data/scenarios/` shows all 7 scenarios ok
- [ ] `pytest -q` shows all tests passing
- [ ] No new commits between the freeze (Step 1) and the OSF upload (Step 3) — if there are, redo Step 1
- [ ] Cost: OSF preregistration is free. There is no bill.

## If the submission is rejected or requires revision

OSF's Registered Report review is light-touch (they check the format, not the science). If OSF asks for a change:
- Small edits (typos, missing field): resubmit within the same OSF project, do NOT change the pinned commit unless the science changed
- Substantive changes: file as a new pre-registration and mark the first as withdrawn; a new commit hash pin is required
