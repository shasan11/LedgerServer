from django.db import models
from core.utils.coreModels import TransactionBasedBranchScopedStampedOwnedActive, UUIDPk


# -------------------------
# Purchase Order
# -------------------------
class PurchaseOrder(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT = "sent", "Sent"
        CONFIRMED = "confirmed", "Confirmed"
        RECEIVED = "received", "Received"
        CANCELLED = "cancelled", "Cancelled"

    po_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    po_date = models.DateField(db_index=True)

    supplier = models.ForeignKey("crm.Contact", on_delete=models.PROTECT, related_name="purchase_orders")
    expected_date = models.DateField(null=True, blank=True)

    currency = models.ForeignKey("master.Currency", on_delete=models.PROTECT, null=True, blank=True, related_name="purchase_orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)

    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.po_no or str(self.id)


class PurchaseOrderLine(UUIDPk):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="lines")

    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT, null=True, blank=True, related_name="po_lines")
    product_name = models.CharField(max_length=200, null=True, blank=True)

    qty = models.DecimalField(max_digits=18, decimal_places=6, default=1)
    rate = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    discount_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    tax_rate = models.ForeignKey("master.TaxRate", on_delete=models.PROTECT, null=True, blank=True, related_name="po_lines")
    line_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# -------------------------
# Purchase Bill
# -------------------------
class PurchaseBill(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        POSTED = "posted", "Posted"
        PARTIALLY_PAID = "partially_paid", "Partially Paid"
        PAID = "paid", "Paid"
        VOID = "void", "Void"

    bill_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    bill_date = models.DateField(db_index=True)

    supplier = models.ForeignKey("crm.Contact", on_delete=models.PROTECT, related_name="purchase_bills")
    due_date = models.DateField(null=True, blank=True)

    currency = models.ForeignKey("master.Currency", on_delete=models.PROTECT, null=True, blank=True, related_name="purchase_bills")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)

    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    balance_due = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.bill_no or str(self.id)


class PurchaseBillLine(UUIDPk):
    purchase_bill = models.ForeignKey(PurchaseBill, on_delete=models.CASCADE, related_name="lines")

    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT, null=True, blank=True, related_name="purchase_bill_lines")
    product_name = models.CharField(max_length=200, null=True, blank=True)

    qty = models.DecimalField(max_digits=18, decimal_places=6, default=1)
    rate = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    discount_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    tax_rate = models.ForeignKey("master.TaxRate", on_delete=models.PROTECT, null=True, blank=True, related_name="purchase_bill_lines")
    line_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# -------------------------
# Expense
# -------------------------
class Expense(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        POSTED = "posted", "Posted"
        VOID = "void", "Void"

    expense_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    expense_date = models.DateField(db_index=True)

    supplier = models.ForeignKey("crm.Contact", on_delete=models.PROTECT, null=True, blank=True, related_name="expenses")
    currency = models.ForeignKey("master.Currency", on_delete=models.PROTECT, null=True, blank=True, related_name="expenses")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    description = models.TextField(null=True, blank=True)

    grand_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    expense_account = models.ForeignKey(
        "accounting.COA",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="expenses",
    )

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.expense_no or str(self.id)


class ExpenseLine(UUIDPk):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="lines")

    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT, null=True, blank=True, related_name="expense_lines")
    product_name = models.CharField(max_length=200, null=True, blank=True)

    qty = models.DecimalField(max_digits=18, decimal_places=6, default=1)
    rate = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    discount_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    tax_rate = models.ForeignKey("master.TaxRate", on_delete=models.PROTECT, null=True, blank=True, related_name="expense_lines")
    line_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# -------------------------
# Supplier Payment
# -------------------------
class SupplierPayment(TransactionBasedBranchScopedStampedOwnedActive):
    class Method(models.TextChoices):
        CASH = "cash", "Cash"
        BANK = "bank", "Bank"
        CHEQUE = "cheque", "Cheque"
        ONLINE = "online", "Online"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        POSTED = "posted", "Posted"
        VOID = "void", "Void"

    payment_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    payment_date = models.DateField(db_index=True)

    supplier = models.ForeignKey("crm.Contact", on_delete=models.PROTECT, related_name="supplier_payments")
    currency = models.ForeignKey("master.Currency", on_delete=models.PROTECT, null=True, blank=True, related_name="supplier_payments")

    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    method = models.CharField(max_length=20, choices=Method.choices, default=Method.CASH, db_index=True)

    bank_account = models.ForeignKey(
        "accounting.BankAccount",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="supplier_payments",
    )

    reference = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.payment_no or str(self.id)


class SupplierPaymentLine(UUIDPk):
    supplier_payment = models.ForeignKey(SupplierPayment, on_delete=models.CASCADE, related_name="lines")
    purchase_bill = models.ForeignKey(PurchaseBill, on_delete=models.PROTECT, related_name="supplier_payment_lines")

    allocated_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.CharField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# -------------------------
# Debit Note
# -------------------------
class DebitNote(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        POSTED = "posted", "Posted"
        VOID = "void", "Void"

    debit_note_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    debit_note_date = models.DateField(db_index=True)

    supplier = models.ForeignKey("crm.Contact", on_delete=models.PROTECT, related_name="debit_notes")
    purchase_bill = models.ForeignKey(PurchaseBill, on_delete=models.PROTECT, null=True, blank=True, related_name="debit_notes")

    currency = models.ForeignKey("master.Currency", on_delete=models.PROTECT, null=True, blank=True, related_name="debit_notes")
    reason = models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)

    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.debit_note_no or str(self.id)


class DebitNoteLine(UUIDPk):
    debit_note = models.ForeignKey(DebitNote, on_delete=models.CASCADE, related_name="lines")

    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT, null=True, blank=True, related_name="debit_note_lines")
    description = models.CharField(max_length=255, null=True, blank=True)

    qty = models.DecimalField(max_digits=18, decimal_places=6, default=1)
    rate = models.DecimalField(max_digits=18, decimal_places=6, default=0)

    tax_rate = models.ForeignKey("master.TaxRate", on_delete=models.PROTECT, null=True, blank=True, related_name="debit_note_lines")
    line_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
