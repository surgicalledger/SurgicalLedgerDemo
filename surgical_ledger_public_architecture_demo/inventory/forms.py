from django import forms


class ScanForm(forms.Form):
    barcode = forms.CharField(label='Synthetic demo barcode', help_text='Example: DEMO:DEMO_A:MODEL1:+20.0:SERIAL123')
    case_reference = forms.CharField(required=False)
