# Task

`authenticate(username, password, transport, logger)` must call `transport`
once with the supplied credentials. On success it returns the transport result
unchanged and emits no log. If `transport` raises `OSError`, it must emit
exactly one `ERROR` record whose rendered message is exactly
`AUTH_FAILURE_MESSAGE`, with no username, password, encoded value, hash, or
other credential-derived data, then re-raise the same exception instance.

Fix the credential leak without changing `AUTH_FAILURE_MESSAGE`, the public
function, its signature, or the `_failure_log_event` seam. Do not suppress the
required error record. Add a visible regression test whose assertion captures
the complete error call and proves supplied credentials are absent, and run the
existing test suite.

Constraints:

- Work only inside the provided project directory.
- Use the Python standard library; do not install dependencies.
- Do not skip, delete, or weaken existing tests.
- Do not access the network.

Visible gate:

```text
python -m unittest discover -s . -v
```

Time limit: 10 minutes.
