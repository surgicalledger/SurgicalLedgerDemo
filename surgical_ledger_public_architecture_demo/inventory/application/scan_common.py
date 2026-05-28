from __future__ import annotations

from django.db import transaction

from inventory.models import InventoryItem, ScanEvent
from inventory.services import ParsedBarcode, parse_barcode


def get_or_create_item(parsed: ParsedBarcode) -> InventoryItem:
    item, _ = InventoryItem.objects.get_or_create(
        brand=parsed.brand,
        public_serial_hash=parsed.serial_fingerprint,
        defaults={
            'model_code': parsed.model_code,
            'normalized_power': parsed.normalized_power,
            'expiration_date': parsed.expiration_date,
            'status': 'on_hand',
        },
    )
    return item


@transaction.atomic
def record_scan(raw_barcode: str, *, direction: str, user=None, note: str = '') -> ScanEvent:
    """Shared scan workflow with public-safe parser and no raw barcode persistence."""
    parsed = parse_barcode(raw_barcode)
    item = get_or_create_item(parsed)
    qty_delta = 1 if direction == ScanEvent.Direction.INBOUND else -1
    if direction == ScanEvent.Direction.OUTBOUND:
        item.status = 'used'
        item.save(update_fields=['status', 'updated_at'])
    return ScanEvent.objects.create(
        item=item,
        direction=direction,
        qty_delta=qty_delta,
        scan_fingerprint=parsed.scan_fingerprint,
        scanned_by=user if getattr(user, 'is_authenticated', False) else None,
        note=note,
    )
