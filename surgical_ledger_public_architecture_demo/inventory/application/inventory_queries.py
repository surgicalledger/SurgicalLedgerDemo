from inventory.models import InventoryItem


def on_hand_items():
    return InventoryItem.objects.filter(status='on_hand').order_by('brand', 'model_code')
