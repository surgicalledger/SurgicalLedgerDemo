from inventory.models import ImplantTrace, ScanEvent
from .scan_common import record_scan


def scan_out(raw_barcode: str, *, case_reference: str, clinician_reference: str = '', user=None):
    event = record_scan(raw_barcode, direction=ScanEvent.Direction.OUTBOUND, user=user)
    ImplantTrace.objects.create(
        item=event.item,
        scan_event=event,
        case_reference=case_reference,
        clinician_reference=clinician_reference,
    )
    return event
