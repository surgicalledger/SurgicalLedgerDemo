def normalize_reference(value: str) -> str:
    return ''.join(ch for ch in (value or '').strip().upper() if ch.isalnum() or ch in {'-', '_'})
