from django.db import models
from core.utils.coreModels import StampedOwnedActive


class Currency(StampedOwnedActive):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    symbol = models.CharField(max_length=10, null=True, blank=True)
    decimal_places = models.IntegerField(default=2)
    is_base = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.name}"


class TaxClass(StampedOwnedActive):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class TaxRate(StampedOwnedActive):
    tax_class = models.ForeignKey(TaxClass, on_delete=models.PROTECT, related_name="rates")
    name = models.CharField(max_length=120)
    rate_percent = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    inclusive = models.BooleanField(default=False)
    active_from = models.DateField(null=True, blank=True)
    active_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.rate_percent}%)"


class MasterData(StampedOwnedActive):
    key = models.CharField(max_length=80, db_index=True)
    name = models.CharField(max_length=150)
    value = models.TextField(null=True, blank=True)
    is_boolean = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
    )

    def __str__(self):
        return self.key


class Branch(StampedOwnedActive):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=80, null=True, blank=True)
    city = models.CharField(max_length=80, null=True, blank=True)
    timezone = models.CharField(max_length=64, null=True, blank=True)
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="branches",
    )
    is_head_office = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.name}"
