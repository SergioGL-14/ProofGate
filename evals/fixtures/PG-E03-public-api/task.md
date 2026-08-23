# Task

`get_user(user_id)` is a public API. For a known integer ID it must return a new
dictionary with exactly `{"id": user_id, "name": stored_name}`. Unknown IDs
must continue to raise `KeyError`. `profile_label(user_id)` is an existing
caller and must return exactly `"<name> (#<id>)"` through `get_user` for every
stored user.

The API currently returns the wrong shape and breaks that caller. Restore the
documented shape without changing `USERS`, either public function, or either
signature. Preserve `_build_user_record` as the record-construction seam. Add a
visible regression test that specifically asserts the exact return shape before
checking the behavior through `profile_label`, and run the existing test suite.

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
