from inventory.models import ImplantTrace, ScanEvent


def traceability_summary():
    return {
        'scan_events': ScanEvent.objects.count(),
        'implant_traces': ImplantTrace.objects.count(),
    }
