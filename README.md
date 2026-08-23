# ProofGate

**Code is not approved. It is proven.**

ProofGate is a portable skill that turns software work into an evidence-based
engineering cycle. It studies the affected system, defines observable
acceptance conditions, selects proportional tests, implements the smallest
responsible change, tries to invalidate it, and reports `PASS`, `FAIL`,
`BLOCKED`, or `EXCEPTION`.

## Status

Phase 1 completed on 2026-08-23 after three real-repository trials. Phase 2 also
completed on 2026-08-23: ten reproducible fixtures compared the base agent with
ProofGate. Final results were 9/10 for base and 10/10 for ProofGate, with zero
critical false `PASS` verdicts from ProofGate. See
[`evals/phase-2-report.md`](evals/phase-2-report.md). Phase 3 applied the full
cycle to an unseen real repository: it found and fixed a latent defect in
`scrapy/queuelib` with red-first regression tests across six backends
([PG-R04](evals/runs/PG-R04-queuelib-report.md)). ProofGate is not installed
globally.

## Engineering Doctrine

ProofGate combines these rules under one evidence contract:

- Understand the real flow before editing.
- Fix root causes at the narrowest responsible layer.
- Apply YAGNI before writing code.
- Reuse project code, then standard library, platform features, and installed
  dependencies before adding anything.
- Prefer deletion, boring code, and the smallest correct diff.
- Use clean code and explicit contracts.
- Keep domain rules independent from frameworks and I/O when the domain is
  complex enough to justify that separation.
- Apply SOLID and DRY only when they remove demonstrated pain.
- Validate untrusted input at trust boundaries.
- Never trade away security, accessibility, data safety, or required behavior
  for fewer lines.
- Never claim success without relevant executed evidence.
- Report briefly without hiding uncertainty or residual risk.

Ponytail and Caveman are design references, not runtime dependencies and not
sources copied into this project.

## Modes

| Mode | Use |
|---|---|
| `lite` | Documentation and trivial mechanical changes |
| `full` | Normal application work; default |
| `ultra` | Security, persistence, concurrency, migrations, and public contracts |
| `infra` | Operational profile for services, permissions, networks, backups, and operating systems; combines with `full` or `ultra` |
| `off` | Disable ProofGate for the current session |

Operations are independent from intensity: `plan`, `build`, `verify`, and
`audit`. Examples: `ProofGate full build`, `ProofGate ultra audit`, or
`verify this with ProofGate infra ultra`. When no intensity accompanies
`infra`, it uses `full`.

## Lifecycle

```text
SCAN -> CONTRACT -> THREAT -> TEST DESIGN -> BUILD -> GAUNTLET
     -> ADVERSARY -> VERDICT
```

`PASS` requires executed evidence for every required acceptance condition,
invariant, non-functional condition, and forbidden condition. An unavailable
or unexecuted required gate cannot be reported as passed.

## Layout

```text
skills/proofgate/SKILL.md  Portable agent contract
templates/                 Contract and report skeletons
evals/                     Evaluation protocol, fixtures, and run evidence
tests/                     Repository contract tests
```

## Use

### OpenCode

Point `skills.paths` at this repository or copy `skills/proofgate/` into a
project or global OpenCode skill directory. No OpenCode configuration is
changed by this repository.

### Codex and Other Agents

Make `skills/proofgate/SKILL.md` available through the host's supported skill
or instruction mechanism. If the host has no skill loader, provide the file as
session instructions.

## Verify

The repository uses only the Python standard library for its contract tests:

```bash
python -m unittest discover -s tests -v
```

These tests verify the portable package, fixture baselines, and mandatory
policy vocabulary. Real-repository trials and the Phase 2 behavioral benchmark
are recorded under `evals/`; future external validation remains separate.

## License

MIT. See [LICENSE](LICENSE).
