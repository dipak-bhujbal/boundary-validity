# boundary-validity

**Measuring the validity gap in propensity evaluations of agentic boundary crossing.**

An independent AI-safety evaluation extending UK AISI's [SandboxEscapeBench](https://arxiv.org/abs/2603.02277) (ICML 2026) from escape capability to escape propensity, with a three-arm identification design that separates substrate fidelity from consequence availability.

## Status

Pre-registration in progress (target: OSF, week 2). No data collected yet. Repository is public from the start to make the design and analysis plan reviewable.

## Scope

Two of three arms will be executed:

- **Arm M** — mocked shell, no virtualization. Cheap, no containment risk.
- **Arm N** — real container with a real affordance surface, exploit silently neutered. Carries the primary estimand $\Delta_{\mathrm{fid}}$. No live escape possible by construction.
- **Arm E** — real exploit, deferred out of scope for the first paper (see [ADR-001](docs/decisions/ADR-001-arm-scope-and-tmlr-fit.md)).

## Target venue

[TMLR](https://jmlr.org/tmlr/). Rolling submission, criterion is *claims supported by evidence*. Arms M and N together support the fidelity-gap claim; arm E is not required.

## Budget & timeline

- ~$900 gross API + compute / ~$400 out-of-pocket after research credits
- 16 weeks solo through submission, 6-week TMLR first-decision median

## Decisions

See [docs/decisions/](docs/decisions/README.md) for architecture decision records.

## Collaboration model

Solo authorship. Acknowledgment-only contributions welcomed for: identification-argument review, statistical review of the hierarchical model, neutering-layer design review, arXiv endorsement. Anyone building harness code is a co-author (see ADR-001).

## Acknowledgments

Portions of this documentation were drafted with AI assistance.

## License

MIT — see [LICENSE](LICENSE).
