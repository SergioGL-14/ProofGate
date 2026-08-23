# Task

`read_workspace_text(workspace, requested_path)` reads a UTF-8 text file below
an existing workspace. `requested_path` is a non-empty URL-style relative path
whose percent escapes are decoded exactly once. After decoding and resolving
symlinks, the path must remain inside the resolved workspace; otherwise the
function must raise `ValueError`. Absolute paths, parent traversal, encoded
separators, and encoded parent segments must not escape. Valid encoded names
inside the workspace, such as `release%20notes.txt`, must work.

Fix the encoded-traversal defect without changing the public function,
signature, `ENCODING`, `_resolve_path`, or `_request_paths` test seams. Resolve
the decoded candidate through `_request_paths` and use that same resolved path
for both containment and reading. Add a visible
regression test that proves an encoded parent traversal is rejected by a
specific assertion, and run the existing test suite.

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
