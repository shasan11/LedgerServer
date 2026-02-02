from django.db import models
from django.conf import settings
from core.utils.coreModels import (
    UUIDPk,
    BranchScopedStampedOwnedActive,
    TransactionBasedBranchScopedStampedOwnedActive,
)


class POSRegister(BranchScopedStampedOwnedActive):
    code = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    name = models.CharField(max_length=150)

    warehouse = models.ForeignKey(
        "inventory.Warehouse",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pos_registers",
    )
    cash_account = models.ForeignKey(
        "accounting.BankAccount",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pos_registers",
    )

    def __str__(self):
        return self.name


class POSShift(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    register = models.ForeignKey(POSRegister, on_delete=models.PROTECT, related_name="shifts")

    opened_at = models.DateTimeField()
    opened_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="pos_shifts_opened",
    )

    closed_at = models.DateTimeField(null=True, blank=True)
    closed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pos_shifts_closed",
    )

    opening_cash = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    closing_cash = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN, db_index=True)

    # override base
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.register} - {self.opened_at}"


class POSSession(BranchScopedStampedOwnedActive):
    shift = models.ForeignKey(POSShift, on_delete=models.PROTECT, related_name="sessions")
    device_id = models.CharField(max_length=120, null=True, blank=True, db_index=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.shift} - {self.device_id or 'device'}"


class POSCashMovement(TransactionBasedBranchScopedStampedOwnedActive):
    class Type(models.TextChoices):
        IN_ = "in", "In"
        OUT = "out", "Out"

    shift = models.ForeignKey(POSShift, on_delete=models.PROTECT, related_name="cash_movements")
    type = models.CharField(max_length=5, choices=Type.choices, db_index=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    reason = models.CharField(max_length=255, null=True, blank=True)

    # override base
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.type} {self.amount}"


class POSPaymentMethod(BranchScopedStampedOwnedActive):
    class Type(models.TextChoices):
        CASH = "cash", "Cash"
        CARD = "card", "Card"
        BANK = "bank", "Bank"
        WALLET = "wallet", "Wallet"
        COD = "cod", "COD"

    name = models.CharField(max_length=120)
    type = models.CharField(max_length=20, choices=Type.choices, db_index=True)

    def __str__(self):
        return self.name


class POSOrder(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        POSTED = "posted", "Posted"
        VOID = "void", "Void"

    order_no = models.CharField(max_length=60, null=True, blank=True, db_index=True)
    order_date = models.DateTimeField(db_index=True)

    register = models.ForeignKey(POSRegister, on_delete=models.PROTECT, related_name="orders")
    shift = models.ForeignKey(POSShift, on_delete=models.PROTECT, related_name="orders")

    customer = models.ForeignKey(
        "crm.Contact",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pos_orders",
    )

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)

    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    # override base
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.order_no or str(self.id)


class POSOrderItem(UUIDPk):
    pos_order = models.ForeignKey(POSOrder, on_delete=models.CASCADE, related_name="items")

    product_variant = models.ForeignKey(
        "inventory.ProductVariant",
        on_delete=models.PROTECT,
        related_name="pos_order_items",
    )

    product_name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.DecimalField(max_digits=18, decimal_places=6, default=1)
    unit_price = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    discount_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    tax_rate = models.ForeignKey(
        "master.TaxRate",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pos_order_items",
    )
    line_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class POSPayment(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        POSTED = "posted", "Posted"
        VOID = "void", "Void"

    pos_order = models.ForeignKey(POSOrder, on_delete=models.PROTECT, related_name="payments")
    method = models.ForeignKey(POSPaymentMethod, on_delete=models.PROTECT, related_name="payments")

    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    reference = models.CharField(max_length=120, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.POSTED, db_index=True)

    # override base
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.method} {self.amount}"


class POSReceipt(BranchScopedStampedOwnedActive):
    pos_order = models.ForeignKey(POSOrder, on_delete=models.PROTECT, related_name="receipts")
    receipt_no = models.CharField(max_length=60, null=True, blank=True, db_index=True)
    printed_at = models.DateTimeField(null=True, blank=True)
    payload = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.receipt_no or str(self.id)


class POSReturn(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        POSTED = "posted", "Posted"
        VOID = "void", "Void"

    return_no = models.CharField(max_length=60, null=True, blank=True, db_index=True)
    return_date = models.DateTimeField(db_index=True)

    pos_order = models.ForeignKey(POSOrder, on_delete=models.PROTECT, null=True, blank=True, related_name="returns")
    customer = models.ForeignKey(
        "crm.Contact",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pos_returns",
    )

    reason = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)

    # override base
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.return_no or str(self.id)


class POSReturnItem(UUIDPk):
    pos_return = models.ForeignKey(POSReturn, on_delete=models.CASCADE, related_name="items")

    pos_order_item = models.ForeignKey(
        POSOrderItem,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="return_items",
    )

    product_variant = models.ForeignKey(
        "inventory.ProductVariant",
        on_delete=models.PROTECT,
        related_name="pos_return_items",
    )

    qty = models.DecimalField(max_digits=18, decimal_places=6, default=1)
    unit_price = models.DecimalField(max_digits=18, decimal_places=6, default=0)

    tax_rate = models.ForeignKey(
        "master.TaxRate",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="pos_return_items",
    )

    line_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class POSDiscountProfile(BranchScopedStampedOwnedActive):
    class DiscountType(models.TextChoices):
        PERCENT = "percent", "Percent"
        FIXED = "fixed", "Fixed"

    name = models.CharField(max_length=120)
    discount_type = models.CharField(max_length=10, choices=DiscountType.choices, default=DiscountType.PERCENT)
    value = models.DecimalField(max_digits=18, decimal_places=6, default=0)

    def __str__(self):
        return self.name


class POSTaxProfile(BranchScopedStampedOwnedActive):
    name = models.CharField(max_length=120)
    tax_rate = models.ForeignKey("master.TaxRate", on_delete=models.PROTECT, related_name="pos_tax_profiles")

    def __str__(self):
        return self.name
