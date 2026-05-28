from django.contrib import admin
from .models import CatalogEntry, ImplantTrace, InventoryItem, ParLevel, PurchaseOrder, ScanEvent

admin.site.register([CatalogEntry, ImplantTrace, InventoryItem, ParLevel, PurchaseOrder, ScanEvent])
