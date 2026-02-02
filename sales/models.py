from django.db import models
from core.utils.coreModels import TransactionBasedBranchScopedStampedOwnedActive, UUIDPk


# -------------------------
# Quotation
# -------------------------
class Quotation(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT = "sent", "Sent"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        EXPIRED = "expired", "Expired"

    quotation_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    quotation_date = models.DateField(db_index=True)

    customer = models.ForeignKey("crm.Contact", on_delete=models.PROTECT, related_name="quotations")
    valid_until = models.DateField(null=True, blank=True)

    currency = models.ForeignKey("master.Currency", on_delete=models.PROTECT, null=True, blank=True, related_name="quotations")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)

    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    # override base
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.quotation_no or str(self.id)


class QuotationItem(UUIDPk):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT, null=True, blank=True, related_name="quotation_items")
    product_name = models.CharField(max_length=200, null=True, blank=True)

    qty = models.DecimalField(max_digits=18, decimal_places=6, default=1)
    rate = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    discount_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    tax_rate = models.ForeignKey("master.TaxRate", on_delete=models.PROTECT, null=True, blank=True, related_name="quotation_items")
    line_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# -------------------------
# Sale
# -------------------------
class Sale(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        CONFIRMED = "confirmed", "Confirmed"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    sale_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    sale_date = models.DateField(db_index=True)

    customer = models.ForeignKey("crm.Contact", on_delete=models.PROTECT, related_name="sales")
    currency = models.ForeignKey("master.Currency", on_delete=models.PROTECT, null=True, blank=True, related_name="sales")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)

    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.sale_no or str(self.id)


class SaleItem(UUIDPk):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT, null=True, blank=True, related_name="sale_items")
    product_name = models.CharField(max_length=200, null=True, blank=True)

    qty = models.DecimalField(max_digits=18, decimal_places=6, default=1)
    rate = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    discount_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    tax_rate = models.ForeignKey("master.TaxRate", on_delete=models.PROTECT, null=True, blank=True, related_name="sale_items")
    line_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# -------------------------
# Invoice
# -------------------------
class Invoice(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        POSTED = "posted", "Posted"
        PARTIALLY_PAID = "partially_paid", "Partially Paid"
        PAID = "paid", "Paid"
        VOID = "void", "Void"

    invoice_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    invoice_date = models.DateField(db_index=True)

    customer = models.ForeignKey("crm.Contact", on_delete=models.PROTECT, related_name="invoices")
    due_date = models.DateField(null=True, blank=True)

    currency = models.ForeignKey("master.Currency", on_delete=models.PROTECT, null=True, blank=True, related_name="invoices")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)

    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    balance_due = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.invoice_no or str(self.id)


class InvoiceItem(UUIDPk):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT, null=True, blank=True, related_name="invoice_items")
    product_name = models.CharField(max_length=200, null=True, blank=True)

    qty = models.DecimalField(max_digits=18, decimal_places=6, default=1)
    rate = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    discount_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    tax_rate = models.ForeignKey("master.TaxRate", on_delete=models.PROTECT, null=True, blank=True, related_name="invoice_items")
    line_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# -------------------------
# Customer Payment
# -------------------------
class CustomerPayment(TransactionBasedBranchScopedStampedOwnedActive):
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

    customer = models.ForeignKey("crm.Contact", on_delete=models.PROTECT, related_name="customer_payments")
    currency = models.ForeignKey("master.Currency", on_delete=models.PROTECT, null=True, blank=True, related_name="customer_payments")

    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    method = models.CharField(max_length=20, choices=Method.choices, default=Method.CASH, db_index=True)

    bank_account = models.ForeignKey(
        "accounting.BankAccount",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="customer_payments",
    )

    reference = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.payment_no or str(self.id)


class CustomerPaymentAllocation(UUIDPk):
    customer_payment = models.ForeignKey(CustomerPayment, on_delete=models.CASCADE, related_name="allocations")
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name="payment_allocations")
    allocated_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.CharField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# -------------------------
# Credit Note
# -------------------------
class CreditNote(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        POSTED = "posted", "Posted"
        VOID = "void", "Void"

    credit_note_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    credit_note_date = models.DateField(db_index=True)

    customer = models.ForeignKey("crm.Contact", on_delete=models.PROTECT, related_name="credit_notes")
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, null=True, blank=True, related_name="credit_notes")

    currency = models.ForeignKey("master.Currency", on_delete=models.PROTECT, null=True, blank=True, related_name="credit_notes")
    reason = models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)

    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.credit_note_no or str(self.id)


class CreditNoteLine(UUIDPk):
    credit_note = models.ForeignKey(CreditNote, on_delete=models.CASCADE, related_name="lines")

    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT, null=True, blank=True, related_name="credit_note_lines")
    description = models.CharField(max_length=255, null=True, blank=True)

    qty = models.DecimalField(max_digits=18, decimal_places=6, default=1)
    rate = models.DecimalField(max_digits=18, decimal_places=6, default=0)

    tax_rate = models.ForeignKey("master.TaxRate", on_delete=models.PROTECT, null=True, blank=True, related_name="credit_note_lines")
    line_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
