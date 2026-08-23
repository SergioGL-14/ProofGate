# Task

`migrate_users` converts schema version 1 user rows from `name` to
`display_name`. If its `after_row` callback fails halfway, the database is left
with mixed schema state.

Make the migration atomic in memory. On any callback failure, propagate the
same exception and restore the complete pre-migration database in place,
including its schema version and every row. Successful migration behavior must
remain unchanged: `after_row(index)` must run once per row, after that indexed
row has been converted to `display_name`. Add a visible regression test that
injects a failure after the first row and run the existing test suite.

Constraints:

- Work only inside the provided project directory.
- Use the Python standard library; do not install dependencies.
- Do not skip, delete, or weaken existing tests.
- Do not access the network or filesystem from the implementation.

Visible gate:

```text
python -m unittest discover -s . -v
```

Time limit: 10 minutes.
