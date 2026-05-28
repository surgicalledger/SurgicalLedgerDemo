from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from .constants import BrandChoices


class InventoryItem(models.Model):
    """Public-safe data model showing item identity without proprietary barcode fields."""

    brand = models.CharField(max_length=32, choices=BrandChoices.choices, db_index=True)
    model_code = models.CharField(max_length=64, db_index=True)
    normalized_power = models.CharField(max_length=32, blank=True)
    public_serial_hash = models.CharField(max_length=96, db_index=True)
    expiration_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=24, default='on_hand', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['brand', 'model_code', 'normalized_power']
        constraints = [models.UniqueConstraint(fields=['brand', 'public_serial_hash'], name='demo_unique_item_identity')]

    def __str__(self) -> str:
        return f'{self.brand} / {self.model_code}'


class ScanEvent(models.Model):
    """Immutable scan ledger entry. Raw barcode content is intentionally not stored."""

    class Direction(models.TextChoices):
        INBOUND = 'IN', 'Inbound'
        OUTBOUND = 'OUT', 'Outbound'
        ADJUSTMENT = 'ADJ', 'Adjustment'

    item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT, related_name='scan_events')
    direction = models.CharField(max_length=4, choices=Direction.choices)
    qty_delta = models.IntegerField(default=0)
    scan_fingerprint = models.CharField(max_length=96, db_index=True)
    scanned_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    scanned_at = models.DateTimeField(default=timezone.now, db_index=True)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-scanned_at']
        indexes = [models.Index(fields=['direction', 'scanned_at'])]


class ImplantTrace(models.Model):
    """Traceability link using demo-safe references, not real patient identifiers."""

    item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT, related_name='implant_traces')
    scan_event = models.OneToOneField(ScanEvent, on_delete=models.PROTECT, related_name='implant_trace')
    case_reference = models.CharField(max_length=96, db_index=True)
    clinician_reference = models.CharField(max_length=96, blank=True)
    procedure_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CatalogEntry(models.Model):
    """Demo catalog row used to show relationships without disclosing vendor catalog data."""

    brand = models.CharField(max_length=32, choices=BrandChoices.choices)
    model_code = models.CharField(max_length=64)
    display_name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = [('brand', 'model_code')]
        ordering = ['brand', 'model_code']


class ParLevel(models.Model):
    catalog_entry = models.OneToOneField(CatalogEntry, on_delete=models.CASCADE, related_name='par_level')
    minimum_quantity = models.PositiveIntegerField(default=0)
    target_quantity = models.PositiveIntegerField(default=0)


class PurchaseOrder(models.Model):
    reference = models.CharField(max_length=64, unique=True)
    vendor_label = models.CharField(max_length=128, blank=True)
    status = models.CharField(max_length=24, default='open', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
