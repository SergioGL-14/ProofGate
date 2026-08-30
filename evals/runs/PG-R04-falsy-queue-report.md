# PG-R04 - Falsy Queue Item Regression

`PROOFGATE: PASS`

Intensity: `full`
Profile: `standard`
Operation: `build`

## Finding

A round-robin queue used a truthiness check to distinguish an item from an
empty result. Empty byte strings were therefore discarded.

## Change

The check now distinguishes `None` from a valid falsy item. Regression tests
cover the shared queue mixin across the supported memory and disk backends.

## Evidence

- The regression failed before the change.
- The focused and full test suites passed after the change.
- Reverting the production line made the regression fail again.
- No existing test or public signature was changed.

## Limits

The run covered the queue implementation and its test suite only. It does not
claim that unrelated defects were resolved.
