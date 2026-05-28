class InventoryError(Exception):
    """Base domain error for the demo architecture."""


class DuplicateItemError(InventoryError):
    pass


class ItemNotAvailableError(InventoryError):
    pass


class TraceabilityValidationError(InventoryError):
    pass
