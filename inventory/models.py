from django.db import models
from core.utils.coreModels import (
    BranchScopedStampedOwnedActive,
    TransactionBasedBranchScopedStampedOwnedActive,
)
from master.models import TaxClass, TaxRate
from accounting.models import COA


class ProductCategory(BranchScopedStampedOwnedActive):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="children")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class UnitOfMeasurement(BranchScopedStampedOwnedActive):
    name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    accept_fraction = models.BooleanField(default=False)

    def __str__(self):
        return self.short_name


class VariantAttribute(BranchScopedStampedOwnedActive):
    name = models.CharField(max_length=120)
    key = models.CharField(max_length=60, db_index=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class VariantAttributeOption(BranchScopedStampedOwnedActive):
    attribute = models.ForeignKey(VariantAttribute, on_delete=models.PROTECT, related_name="options")
    name = models.CharField(max_length=120)
    key = models.CharField(max_length=60, db_index=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.attribute.name}: {self.name}"


class Product(BranchScopedStampedOwnedActive):
    class Type(models.TextChoices):
        GOODS = "goods", "Goods"
        SERVICE = "service", "Service"

    class ValuationMethod(models.TextChoices):
        FIFO = "fifo", "FIFO"
        WEIGHTED_AVERAGE = "weighted_average", "Weighted Average"

    type = models.CharField(max_length=10, choices=Type.choices, db_index=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=80, null=True, blank=True, db_index=True)

    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, null=True, blank=True, related_name="products")
    tax_class = models.ForeignKey(TaxClass, on_delete=models.PROTECT, null=True, blank=True, related_name="products")
    primary_unit = models.ForeignKey(UnitOfMeasurement, on_delete=models.PROTECT, null=True, blank=True, related_name="products")

    hs_code = models.CharField(max_length=40, null=True, blank=True)

    ecommerce_enabled = models.BooleanField(default=False)
    pos_enabled = models.BooleanField(default=False)

    description = models.TextField(null=True, blank=True)
    selling_price = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    purchase_price = models.DecimalField(max_digits=18, decimal_places=6, default=0)

    sales_account = models.ForeignKey(COA, on_delete=models.PROTECT, null=True, blank=True, related_name="sales_products")
    purchase_account = models.ForeignKey(COA, on_delete=models.PROTECT, null=True, blank=True, related_name="purchase_products")
    purchase_return_account = models.ForeignKey(COA, on_delete=models.PROTECT, null=True, blank=True, related_name="purchase_return_products")

    valuation_method = models.CharField(max_length=20, choices=ValuationMethod.choices, default=ValuationMethod.FIFO)
    track_inventory = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductVariant(BranchScopedStampedOwnedActive):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=120, null=True, blank=True, db_index=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    option_summary = models.CharField(max_length=255, null=True, blank=True)

    selling_price = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    purchase_price = models.DecimalField(max_digits=18, decimal_places=6, default=0)

    def __str__(self):
        return self.sku or self.name or str(self.id)


class ProductVariantOption(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="variant_options")
    attribute = models.ForeignKey(VariantAttribute, on_delete=models.PROTECT, related_name="variant_links")
    option = models.ForeignKey(VariantAttributeOption, on_delete=models.PROTECT, related_name="variant_links")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ProductPicture(BranchScopedStampedOwnedActive):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="pictures")
    image = models.CharField(max_length=255)
    is_main = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)


class Warehouse(BranchScopedStampedOwnedActive):
    code = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    name = models.CharField(max_length=150)
    address = models.TextField(null=True, blank=True)
    contact_phone = models.CharField(max_length=60, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class WarehouseTransfer(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        POSTED = "posted", "Posted"
        VOID = "void", "Void"

    transfer_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    transfer_date = models.DateField(db_index=True)
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="transfers_out")
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="transfers_in")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)


class WarehouseTransferItem(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    warehouse_transfer = models.ForeignKey(WarehouseTransfer, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name="warehouse_transfer_lines")
    qty = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    note = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class InventoryAdjustment(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        POSTED = "posted", "Posted"
        VOID = "void", "Void"

    adjustment_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    adjustment_date = models.DateField(db_index=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="adjustments")
    reason = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)


class InventoryAdjustmentItem(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    inventory_adjustment = models.ForeignKey(InventoryAdjustment, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name="adjustment_lines")
    qty_change = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    unit_cost = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    note = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ProductionOrder(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        VOID = "void", "Void"

    production_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    production_date = models.DateField(db_index=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="production_orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)

    finished_good_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name="finished_in_productions")
    planned_qty = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    produced_qty = models.DecimalField(max_digits=18, decimal_places=6, default=0)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)


class ProductionInput(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE, related_name="inputs")
    raw_material_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name="raw_in_productions")
    qty_required = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    qty_consumed = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ProductionOutput(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE, related_name="outputs")
    finished_good_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name="output_productions")
    qty_produced = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
