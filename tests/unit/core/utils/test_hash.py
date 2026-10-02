
from paper_rag.core.utils.hash import hash_strings


def test_hash_separator_avoids_collisions():
    assert hash_strings(["ab", "c"]) != hash_strings(["a", "bc"])
