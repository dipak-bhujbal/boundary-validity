# Google Cloud AUP Pre-Registration — Draft

**⚠️ Before sending:** verify current Google Cloud Trust & Safety contact address. Google's abuse reporting page at https://support.google.com/code/contact/cloud_platform_report and Google Cloud's security response process at https://cloud.google.com/security/overview may direct research pre-registration to a specific form or account contact. Verify before sending to any address drafted here.

---

**To:** [VERIFY — check https://support.google.com/code/contact/cloud_platform_report and Google Cloud console → Support for the correct research-pre-registration channel]

**From:** Dipak Bhujbal <dipak.bhujbal23@gmail.com>

**Subject:** Research AUP pre-registration: AI safety evaluation using nested virtualization, self-contained containment study

---

Hello,

I am an independent researcher writing to pre-register a self-contained AI safety evaluation I plan to run on Google Cloud Compute Engine. The evaluation studies how language-model agents behave when placed near containment boundaries, and I want to confirm my protocol aligns with the Google Cloud acceptable use policy before I begin.

**Study in one paragraph.** The evaluation extends UK AI Security Institute's *SandboxEscapeBench* (Marchand et al., arXiv:2603.02277, ICML 2026 [VERIFY: oral vs poster before send]) from measuring capability to measuring propensity. It measures whether LM agents given ordinary in-container tasks take unprompted actions that would cross the container boundary, and compares behavior between fabricated substrates (mocked shell) and real substrates (nested-virt container). The public design is at https://github.com/dipak-bhujbal/boundary-validity (`docs/proposal/`). Target publication venue is TMLR.

**What runs on Google Cloud.** Only the "arm N" portion of the study runs on your infrastructure: real Docker containers running inside Compute Engine VMs launched from a nested-virtualization-licensed image (per https://cloud.google.com/compute/docs/instances/nested-virtualization/overview). Each container hosts a benign task and an *unmentioned but detectable* affordance drawn from the published SandboxEscapeBench suite. The exploit that would use the affordance is **silently neutered by a Python wrapper** that intercepts the exploit command signature and returns canned stdout without executing the underlying tool.

**Explicit no-escape guarantees:**

1. **No exploit ever executes.** The neutering wrapper is intercept-and-fake, not attempt-and-hope; the exploit command is matched by signature and returns a canned response without dispatch.
2. **Default-deny egress** at the VM host firewall via VPC firewall rules and denied outbound to the metadata IP. No outbound DNS, no outbound connections. Attempts are logged as measurements.
3. **No live credentials.** No service account attachment with any real permission; instance metadata concealment enabled; no reusable secrets in the environment. Any credential-shaped artifact in the container is a decoy with no privilege.
4. **Ephemeral hosts.** One VM per sample, destroyed after scoring; no state carried across samples.
5. **Published mechanisms only.** Every affordance is drawn from the published SandboxEscapeBench suite or from publicly documented, upstream-patched historical vulnerabilities. The study develops no new exploits and produces no capability that is not already public.
6. **Hard stop rule.** Default-deny egress is enforced at the VM host firewall via VPC firewall rules, and any denied outbound connection is logged as a measurement (the study's own design intends for the neutered exploit to *attempt* egress; the denial is expected and the log is the data point). Cgroup and process-boundary monitoring specifics are finalized in a follow-up design ADR (`docs/decisions/ADR-005`, invariants INV-1 through INV-5) before first arm-N execution. Any anomaly beyond the pre-registered denial-log pattern halts the study and I disclose to Google Cloud Trust & Safety before further sampling.
7. **Arm E excluded from this study.** A hypothetical third arm that would permit a live escape is explicitly out of scope (documented at `docs/decisions/ADR-001-arm-scope-and-tmlr-fit.md`). I am not asking for permission to run it and will not run it on Google Cloud.

**Scale.** Approximately 6,000 total episodes over 4 weeks (weeks 12–14 of the timeline), across 5 model APIs. Peak concurrency ~10 VMs. Cost estimate ~$200 in nested-virt compute plus API calls.

**What I am asking for.** Written non-objection to the protocol above under the acceptable use policy, and confirmation of the correct channel for the study's own egress-alert notifications (which the design is intended to generate as a measurement instrument, not as an incident).

I would rather delay start by two weeks and have your team's acknowledgment on file than proceed on my reading of the AUP alone. I am happy to make any changes needed to align with your policies, and to receive any conditions your team wishes to impose.

Full study protocol, containment appendix, and analysis plan:
- Repository: https://github.com/dipak-bhujbal/boundary-validity
- Proposal: https://github.com/dipak-bhujbal/boundary-validity/blob/main/docs/proposal/boundary-validity-gap-proposal.md
- Charter and scope: https://github.com/dipak-bhujbal/boundary-validity/tree/main/docs/decisions

Thank you for your time.

Dipak Bhujbal
Independent AI safety researcher
Cambridge, Massachusetts
[phone TBD]
