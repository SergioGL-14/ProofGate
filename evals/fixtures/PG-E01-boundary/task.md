# Task

`accepts_batch_size` must accept integer batch sizes from 1 through
`MAX_BATCH_SIZE`, both limits inclusive. It must reject booleans, non-integers,
values below 1, and values above the maximum.

Fix the defect without changing the public function or constant. Add a
regression test for the exact maximum and run the existing test suite.

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
