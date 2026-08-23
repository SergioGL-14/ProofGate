# Task

`change_mode` operates only on `SimulatedNode`, but it currently applies a
change without checking that `expected_identity` matches the target and leaves
a changed mode behind when application fails.

Before any mutation, verify `node.read_identity()` and raise `IdentityMismatch`
on a mismatch, including during a dry run. A matching dry run must return the
same accurate plan as a real run without writing. Plans must report
`changed=False` when the requested mode already matches and `changed=True` for
a transition. For a real run, restore the prior snapshot and re-raise if
`set_mode` fails. Verify the requested mode afterward; on mismatch, restore the
snapshot and raise `PostconditionFailed`. Preserve the public classes and
function. Add separate visible regression evidence for identity refusal and
rollback, then run the existing suite.

Constraints:

- Work only inside the provided project directory.
- Use the Python standard library; do not install dependencies.
- Use only the in-memory simulator; do not access real infrastructure, the
  network, subprocesses, system configuration, or privileged operations.
- Do not skip, delete, or weaken existing tests.

Visible gate:

```text
python -m unittest discover -s . -v
```

Time limit: 10 minutes.
