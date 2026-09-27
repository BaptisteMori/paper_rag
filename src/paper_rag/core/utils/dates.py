from datetime import date


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    parts = [int(p) for p in value.split("-")] + [1, 1]
    try:
        return date(parts[0], parts[1], parts[2])
    except ValueError:
        return None
