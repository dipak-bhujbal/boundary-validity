# AUP Pre-Registration

Both AWS and Google Cloud acceptable-use policies prohibit deliberately eliciting unauthorized system access, even self-contained. The `boundary-validity` study is not adversarial against provider infrastructure — but the surface of the study *is* eliciting containment-boundary crossing under measurement. That is close enough to the AUP-prohibited pattern that pre-registration to each provider's abuse or trust-and-safety team is the correct move.

## Purpose

- Establish written non-objection before any arm N execution.
- Give abuse teams a documented threat model so an alert during the study (which the study's own egress-alerting layer is designed to generate) is contextualized, not surprising.
- Protect the account from mid-study termination that would destroy data and delay publication.

## When to send

**Before** any arm N execution. Response turnaround is typically 5–10 business days, so send by end of week 2 to keep arm N start on the PLAN.md schedule.

## Drafts

- [aws.md](aws.md) — for AWS Trust & Safety (target instance family: `c8i` in `us-west-2` with `CpuOptions` nested-virt enabled)
- [gcp.md](gcp.md) — for Google Cloud Trust & Safety (target: Compute Engine with nested-virt-licensed image)

## Reviewer checklist before sending

- [ ] Confirm the target email addresses against the current AWS and GCP trust & safety contact pages — do not send to the addresses drafted here without verification
- [ ] Add Dipak's phone number and mailing address to the signature
- [ ] Add the OSF pre-registration DOI once the pre-registration is timestamped (week 2 gate)
- [ ] Add the GitHub repo URL (already public: https://github.com/dipak-bhujbal/boundary-validity)
- [ ] Do not attach the full 38K proposal PDF; link to the GitHub `docs/proposal/` path instead
- [ ] Send from `dipak.bhujbal23@gmail.com`, expect an initial auto-response and a human follow-up within 5–10 business days
- [ ] If no substantive reply after 10 business days, follow up once; if no reply after 15, escalate via account support ticket
