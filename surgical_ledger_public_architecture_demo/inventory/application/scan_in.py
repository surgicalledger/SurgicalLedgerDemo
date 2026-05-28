from inventory.models import ScanEvent
from .scan_common import record_scan


def scan_in(raw_barcode: str, *, user=None):
    return record_scan(raw_barcode, direction=ScanEvent.Direction.INBOUND, user=user)
