import hashlib


def hash_strings(strings: list[str]) -> str:
    hasher = hashlib.sha256()
    for string in strings:
        hasher.update(string.encode("utf-8"))
        hasher.update(b"\x00")  # separator
    return hasher.hexdigest()
