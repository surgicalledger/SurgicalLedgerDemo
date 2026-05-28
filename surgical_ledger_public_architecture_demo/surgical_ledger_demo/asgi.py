import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'surgical_ledger_demo.settings')
application = get_asgi_application()
