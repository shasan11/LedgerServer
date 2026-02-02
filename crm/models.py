from django.db import models
from core.utils.coreModels import BranchScopedStampedOwnedActive


class ContactGroup(BranchScopedStampedOwnedActive):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Contact(BranchScopedStampedOwnedActive):
    class Type(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        SUPPLIER = "supplier", "Supplier"
        LEAD = "lead", "Lead"

    type = models.CharField(max_length=20, choices=Type.choices, db_index=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    pan = models.CharField(max_length=50, null=True, blank=True)

    phone = models.CharField(max_length=60, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    group = models.ForeignKey(
        ContactGroup,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="contacts",
    )

    accept_purchase = models.BooleanField(default=False)
    credit_terms_days = models.IntegerField(default=0)
    credit_limit = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    receivable_account = models.ForeignKey(
        "accounting.COA",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="receivable_contacts",
    )
    payable_account = models.ForeignKey(
        "accounting.COA",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="payable_contacts",
    )

    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Deal(BranchScopedStampedOwnedActive):
    class Stage(models.TextChoices):
        LEAD = "lead", "Lead"
        QUALIFIED = "qualified", "Qualified"
        PROPOSAL = "proposal", "Proposal"
        WON = "won", "Won"
        LOST = "lost", "Lost"

    code = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    title = models.CharField(max_length=200)

    contact = models.ForeignKey("crm.Contact", on_delete=models.PROTECT, related_name="deals")
    stage = models.CharField(max_length=20, choices=Stage.choices, default=Stage.LEAD, db_index=True)

    expected_close = models.DateField(null=True, blank=True)
    probability = models.IntegerField(default=0)

    currency = models.ForeignKey(
        "master.Currency",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="deals",
    )

    expected_value = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    source = models.CharField(max_length=80, null=True, blank=True)

    owner = models.ForeignKey(
        "auth.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="owned_deals",
    )

    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class DealItem(BranchScopedStampedOwnedActive):
    deal = models.ForeignKey("crm.Deal", on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(
        "inventory.Product",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="deal_items",
    )

    description = models.CharField(max_length=255, null=True, blank=True)
    qty = models.DecimalField(max_digits=18, decimal_places=6, default=1)
    rate = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    discount_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    tax_rate = models.ForeignKey(
        "master.TaxRate",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="deal_items",
    )

    line_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.deal} - {self.id}"


class Activity(BranchScopedStampedOwnedActive):
    class Type(models.TextChoices):
        CALL = "call", "Call"
        MEETING = "meeting", "Meeting"
        TASK = "task", "Task"
        EMAIL = "email", "Email"
        NOTE = "note", "Note"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        DONE = "done", "Done"
        CANCELLED = "cancelled", "Cancelled"

    type = models.CharField(max_length=20, choices=Type.choices, db_index=True)
    subject = models.CharField(max_length=200)

    contact = models.ForeignKey(
        "crm.Contact",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="activities",
    )
    deal = models.ForeignKey(
        "crm.Deal",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="activities",
    )

    due_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)

    assigned_to = models.ForeignKey(
        "auth.User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="assigned_activities",
    )

    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.subject
