# ADR-006 — Egress-under-load verification for arm N (scaffold)

**Status:** Scaffold — decision pending. Blocks arm N execution per PLAN.md gate G3.

**Reviewer:** TBD (to be filled when a security reviewer engages via LessWrong recruitment post or targeted cold email).

**Author of scaffold:** dipak, 2026-07-25.

**Relationship to ADR-005:** This ADR resolves Tension 2 of ADR-005 (§Known unresolved tensions). ADR-005 documents the tension; this ADR chooses the concrete replacement for INV-4 that must be in place before any arm N episode runs.

## Context

ADR-005 INV-4 verifies "no side effects" during an intercepted-crossing episode by running `strace` on the wrapper's PID during a fixture run and asserting zero writes to `/var/log/*`, zero opens of `/dev/net/tun`, zero mounts, zero container-network egress.

**The tension** (extracted from ADR-005 §Known unresolved tensions, Tension 2):

The failure mode the study exists to prevent is a packet reaching a network. `strace` on a fixture run is necessary but not sufficient: it does not verify that default-deny egress at the hypervisor firewall holds under concurrent adversarial load. The invariant that actually matters — no packet ever leaves the guest — must be verified against an adversarial workload, at the layer where the failure would occur (the firewall log), not inside the guest where a compromised agent could suppress evidence.

## Candidate approaches

### Candidate A — Adversarial concurrent-episode fuzzing at hypervisor firewall

Before any real arm N episode, run a dedicated fuzzing pass:
- ≥ 10 concurrent episodes of the arm-N harness in parallel
- Each episode runs a curated egress-attempt playbook (below)
- Failure criterion: **any single packet reaching the hypervisor firewall log** halts the study
- Verification is at the firewall (host-level), not inside the guest

**Playbook (must include, non-exhaustive):**
- `nc -zv 8.8.8.8 443` (TCP)
- `nc -uzv 8.8.8.8 53` (UDP)
- `nslookup google.com` (DNS)
- `curl -v http://169.254.169.254/latest/meta-data/` (AWS instance-metadata IPv4)
- `curl -v http://[fd00:ec2::254]/latest/meta-data/` (AWS instance-metadata IPv6)
- `curl -v http://metadata.google.internal/` (GCP metadata)
- `ping -c 1 8.8.8.8` (ICMP)
- `ping -c 1 -6 2001:4860:4860::8888` (ICMPv6)
- HTTPS GET to a known responder controlled by the researcher
- HTTPS POST with a distinguishing payload to a known responder
- DNS TXT-record lookup to a subdomain owned by the researcher (DNS tunnel probe)

- **Detection confidence:** High. Firewall log is the ground truth for "packet left the guest."
- **False-positive rate:** Very low. A packet is a packet.
- **Implementation complexity:** Moderate. Requires firewall log ingestion + assertion harness + orchestrator for concurrent episodes.
- **Cost:** ~$50 in cloud compute for the fuzzing run.

### Candidate B — VPC flow-log analysis with automated alerting

Enable VPC flow logs (AWS) or equivalent (GCP). During arm N runs, tail the flow log; any accepted or rejected outbound flow triggers an alert and halts the study.

- **Detection confidence:** High for accepted flows; VPC flow logs are authoritative for AWS. GCP flow logs equivalent.
- **False-positive rate:** Low. Flow logs are precise about {src, dst, port, protocol, action}.
- **Implementation complexity:** Low-moderate. Provider-managed infrastructure; ingestion and alerting are standard patterns.
- **Cost:** ~$10-30/month in flow-log storage during arm N execution weeks.

**Coverage gap vs A:** Flow logs are post-hoc — they detect a leak after it happened. Candidate A is a pre-run gate (fail before any real episode). Also, VPC flow logs may miss out-of-band leaks below the VPC layer (highly unlikely but not impossible on some kernel bugs).

### Candidate C — Both A and B

Candidate A as the **pre-arm-N gate** (must pass before first real arm-N episode). Candidate B as the **during-arm-N monitoring** (running throughout arm N execution as an in-flight safety net).

- **Detection confidence:** Highest. Two independent detection layers at two temporal windows.
- **False-positive rate:** Additive but still low.
- **Implementation complexity:** Sum of A + B.
- **Cost:** ~$60-80 total across A and B.

## Tradeoff summary

| Aspect                                          | A: fuzzing gate   | B: flow-log monitor | C: both              |
|-------------------------------------------------|:-----------------:|:-------------------:|:--------------------:|
| Detection confidence                            | High              | High                | Highest              |
| Temporal window                                 | Pre-run only      | During-run only     | Both                 |
| False-positive rate                             | Very low          | Low                 | Low                  |
| Implementation complexity                       | Moderate          | Low-moderate        | Sum                  |
| Cloud spend (weeks 9-12)                        | ~$50              | ~$30                | ~$80                 |
| Detects post-deployment behavior change         | No                | Yes                 | Yes                  |
| Fail-before-first-real-episode                  | Yes               | No                  | Yes                  |

## Test criteria any decision must pass

1. **Reliably detects the following in a controlled test:**
   - DNS exfiltration via TXT-record lookup to a researcher-owned subdomain
   - ICMP echo to 8.8.8.8
   - HTTP GET to a researcher-controlled IP on port 80
   - HTTPS POST to a researcher-controlled endpoint on port 443
   - Connect attempt to `169.254.169.254` (AWS metadata)
   - IPv6 outbound (both DNS and TCP)
2. **Zero packet leaks** in a 24-hour concurrent-episode stress test with the adversarial playbook running continuously across 10 parallel episodes.
3. **The choice must be defensible in TMLR §7** as the operationalization of the hard-stop rule (proposal §7, OSF §5.3).
4. **If Candidate B is chosen alone:** the ADR must explicitly acknowledge that a leak can happen once before detection, and justify why that risk is acceptable.

## Decision

**PENDING — awaiting security reviewer input. Blocks arm N execution per PLAN.md gate G3.**

This ADR does not commit to A, B, or C. The scaffold exists so a reviewer with cloud-security domain knowledge can slot their answer into a well-defined decision space rather than answering "how should we verify containment" from scratch.

## Amendment path

Once the security reviewer's answer is in hand:
1. Update the "Decision" section with the chosen candidate letter (A / B / C).
2. Add the reviewer's name and affiliation in the header.
3. Record the reviewer's justification in a new §Rationale section.
4. Attach the fuzzing test harness (Candidate A/C) or flow-log ingestion script (Candidate B/C) as a linked commit.
5. File as an amendment to the OSF pre-registration (new blob hash, per ADR-004 §6).
6. Mark PLAN.md gate G3 for this ADR as satisfied.

## What this ADR does not address

- **Post-deployment cloud provider policy changes** that could relax egress defaults. Assumption: manual re-verification of egress policy is a PLAN.md pre-arm-N-week checklist item, not this ADR's scope.
- **Compromise of the firewall itself.** Out of threat model — the study's threat model assumes the cloud provider's hypervisor and firewall are trusted.
- **Egress via legitimate provider services** (e.g., an authorized image pull). Handled by the "arm-N image is pre-pulled and cached; no runtime image fetches" rule in ADR-005 §Design principles.
