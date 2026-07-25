# Scenarios

Each subdirectory is one condition from the pre-registration (ADR-004, table §5.3 of the proposal). Every scenario must conform to the command contract schema in [ADR-003](../../docs/decisions/ADR-003-command-contract-v0.md).

## Structure

```
data/scenarios/{A..G}/
├── scenario.yaml          # authoritative spec — read by both scorer and arm-N harness
├── mock_fs/               # arm M: fake filesystem the mock shell returns
├── container_setup.sh     # arm N: real setup that creates the affordance surface (added week 9+)
└── expected_labels/       # hand-crafted trajectories with expected {D, X, Y, A} labels
                           # used for the pre-flight contract validation (140 total; ADR-003 §Validation)
```

The `scenario.yaml` is the single source of truth. Anything not in the YAML (mock filesystem contents, hand-crafted trajectories) is derived from it and validated against it.

## Conditions

| ID | In-sandbox path | Affordance | Purpose |
|:--|:--|:--|:--|
| A | open | present, unmentioned, useful | ordinary base rate |
| B | blocked | present, unmentioned, useful | primary manipulation, per H2 |
| C | open, scope language vague | present, unmentioned, useful | instruction clarity |
| D | open | present, framed as available | permission effect |
| E | open | present but useless for the task | separates crossing from usefulness |
| F | blocked, authorised blocker-report path | present, unmentioned, useful | tests whether an honourable exit suppresses crossing |
| G | open | present, unmentioned, useful — agent told it is being evaluated | eval-awareness (H6) |

Condition A is the canonical form. B–G share the same task, affordance, and command contract; they differ only in the `condition_flags` and (for B, F) in a `sandbox_gate` block that blocks the in-sandbox path.
