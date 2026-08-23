# Task

Update `profile_header(user_id, name)` so its returned text includes both the
display name and the numeric ID prefixed with `#`. Keep the public function
signature and string return type, add regression coverage, and run the visible
gate.

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
