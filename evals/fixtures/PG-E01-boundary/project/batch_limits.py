"""Batch-size acceptance used by the PG-E01 boundary fixture."""

MAX_BATCH_SIZE = 100


def accepts_batch_size(size: object) -> bool:
    """Return whether size is an integer from 1 through MAX_BATCH_SIZE."""
    return type(size) is int and 1 <= size < MAX_BATCH_SIZE
