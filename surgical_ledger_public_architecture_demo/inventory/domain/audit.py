def audit_message(action: str, *, actor: str | None = None, target: str | None = None) -> str:
    """Small public-safe audit helper used by application services."""
    bits = [action]
    if actor:
        bits.append(f'actor={actor}')
    if target:
        bits.append(f'target={target}')
    return ' | '.join(bits)
