from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .application.compliance import traceability_summary
from .application.inventory_queries import on_hand_items
from .application.scan_in import scan_in
from .application.scan_out import scan_out
from .forms import ScanForm
from .models import ScanEvent
from .services import BarcodeParseError


def dashboard(request):
    return render(request, 'inventory/dashboard.html', {
        'items': on_hand_items()[:25],
        'summary': traceability_summary(),
    })


@require_http_methods(['GET', 'POST'])
def scan(request):
    form = ScanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            direction = request.POST.get('direction', 'IN')
            if direction == 'OUT':
                scan_out(form.cleaned_data['barcode'], case_reference=form.cleaned_data.get('case_reference') or 'DEMO-CASE', user=request.user)
            else:
                scan_in(form.cleaned_data['barcode'], user=request.user)
            messages.success(request, 'Demo scan recorded.')
            return redirect('inventory:dashboard')
        except BarcodeParseError as exc:
            messages.error(request, str(exc))
    return render(request, 'inventory/scan.html', {'form': form})


def scan_log(request):
    return render(request, 'inventory/scan_log.html', {'events': ScanEvent.objects.select_related('item')[:100]})
