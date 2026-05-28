from django.db import models


class BrandChoices(models.TextChoices):
    DEMO_A = 'DEMO_A', 'Demo Vendor A'
    DEMO_B = 'DEMO_B', 'Demo Vendor B'
    DEMO_C = 'DEMO_C', 'Demo Vendor C'
