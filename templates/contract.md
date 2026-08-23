# ProofGate Contract

Intensity: `<lite|full|ultra>`
Profile: `<standard|infra>`
Operation: `<plan|build|verify|audit>`

## Scan

```yaml
project:
  language: <value>
  framework: <value or none>
  test_runner: <value or unavailable>
  gates:
    - <existing command>
affected:
  modules:
    - <path>
  callers:
    - <path>
risk:
  intensity: <lite|full|ultra>
  profile: <standard|infra>
  reasons:
    - <reason>
```

## Objective

<Observable outcome requested by the user.>

Use one independently verifiable condition per ID. State the measurement point
when timing can change the result, such as before BUILD or at verdict.

## Acceptance

| ID | Observable condition | Measurement point | Required |
|---|---|---|---|
| PG-A1 | <behavior> | <before BUILD, after gate, or at verdict> | Yes |

## Invariants

| ID | Preserved condition | Measurement point | Required |
|---|---|---|---|
| PG-I1 | <existing behavior or contract> | <before BUILD, after gate, or at verdict> | Yes |

## Non-Functional Conditions

| ID | Condition | Measurement point | Required |
|---|---|---|---|
| PG-N1 | <security, compatibility, performance, or operation> | <before BUILD, after gate, or at verdict> | Yes |

## Forbidden

| ID | Action or regression | Measurement point | Required |
|---|---|---|---|
| PG-F1 | <forbidden condition> | <before BUILD, after gate, or at verdict> | Yes |

## Risks And Evidence

| Contract ID | Required | Risk or attack | Evidence | Required gate |
|---|---|---|---|---|
| PG-A1 | Yes | <plausible failure> | <test or check> | <command or unavailable> |
| PG-I1 | Yes | <regression> | <test or check> | <command or unavailable> |
| PG-N1 | Yes | <non-functional failure> | <test or check> | <command or unavailable> |
| PG-F1 | Yes | <forbidden outcome> | <negative check> | <command or unavailable> |

## Ambiguities

- <Question requiring user input, or declared safe reversible interpretation.>

## Rollback

- <Required for infra and stateful changes; otherwise not applicable.>

Every condition defaults to required. Optional conditions must be justified
before BUILD. Contract changes after BUILD starts require explicit user
authorization and must identify affected IDs and reason; missing authorization
forces `BLOCKED`.
