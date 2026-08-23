# Task

`export_report` raises `TypeError: write() argument must be str, not bytes` when
used with a real output path, although the current tests pass. Fix the real
integration path without changing the public function signatures. Add a
regression test that writes and reads a real temporary file, then run the suite.

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
