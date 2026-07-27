# OSF Update History

Registration DOI: `10.17605/OSF.IO/2KH7B`

Chronological record of every schema response filed against the registration.
Newest first. All URLs point to the OSF API resource for the response.

## 2026-07-27T00:40:06 UTC — round-3 cleanup (approved)

Response id: `6a66a81d80d684c0cea5a6e3`
- https://api.osf.io/v2/schema_responses/6a66a81d80d684c0cea5a6e3/

Scope:
- Field `344-4` Foreknowledge: corrected certification back to "Authors
  have observed the data, but have not performed the proposed analyses"
  (round-2 had regressed to the opposite).
- Field `344-40` Study Design: removed leading `Replace the entire box
  with this:` drafting-instruction prefix.
- Field `344-86` Other / Context: added evidence artifact corrigendum
  block pinning commit `0c9aa294e7bd51ea07b74cb2adad1ceacf0fadbd`.
- Metadata Description: replaced with three-arm-identification-design /
  two-arm-study-for-this-paper / arm-E-deferred wording, no bare hash.

## 2026-07-27T00:33:40 UTC — round-2 evidence corrigendum (approved)

Response id: `6a669d880613c5ddcdc7baff`
- https://api.osf.io/v2/schema_responses/6a669d880613c5ddcdc7baff/

Scope:
- Reason / revision_justification: post-amendment evidence artifact
  corrigendum + clerical cleanup note.
- Field `344-55` Starting/Stopping: removed leading `One change needed:`
  drafting-instruction preamble; run order updated to two-arm execution
  with arm E deferred noted.
- Two other intended cleanups did not land in this submission and were
  fixed in the round-3 response above.

## 2026-07-26T02:35:30 UTC — arm-M substrate amendment (approved)

Response id: `6a656e84c0fbd82bf0f21c84`
- https://api.osf.io/v2/schema_responses/6a656e84c0fbd82bf0f21c84/

Scope:
- Arm-M substrate: changed from hand-coded MockShell to real bash in a
  per-episode Docker container pinned by content digest
  `debian@sha256:7b140f374b289a7c2befc338f42ebe6441b7ea838a042bbd5acbfca6ec875818`.
- Governed by ADR-007 (Proposed at time of filing; not Accepted).
- Pinned repository commit at time of filing:
  `d023f8f33744a831ed9dbe88e34c5bffaa67eacb`.
- Real-shell data collection gated on: amendment timestamp + external
  reviewer response + separate commit flipping ADR-007 to Accepted.

## 2026-07-25T17:47:47 UTC — original registration (approved)

Response id: `6a64f6c4ab00f189b7d1561c`
- https://api.osf.io/v2/schema_responses/6a64f6c4ab00f189b7d1561c/

Pinned repository commit at time of registration:
`b8a9f34abc45484819767e7c34c6dd8ddb080158`.

Three-arm identification design (M/N/E) per ADR-000 and ADR-001.
This paper executes the two-arm study (M, N); arm E deferred out of scope.

## Notes

- ADR-007 status is still Proposed as of 2026-07-27; not Accepted.
- No real-shell model data has been collected under `BV_ARM_M_SHELL=real`.
- No paid model API spend has occurred for arm-M-real or arm-N runs.
- The pilot evidence audit that motivated the round-2 corrigendum lives
  at `data/pilot/audit_20260726/`, pinned at commit `0c9aa294...`.
