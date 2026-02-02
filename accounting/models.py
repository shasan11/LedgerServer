from django.db import models
from core.utils.coreModels import (
    StampedOwnedActive,
    BranchScopedStampedOwnedActive,
    TransactionBasedBranchScopedStampedOwnedActive,
)
from master.models import Currency, TaxRate
from master.models import Branch  # optional, only if you need typing/IDE help


class AccountType(StampedOwnedActive):
    class Category(models.TextChoices):
        ASSET = "asset", "Asset"
        LIABILITY = "liability", "Liability"
        EQUITY = "equity", "Equity"
        INCOME = "income", "Income"
        EXPENSE = "expense", "Expense"

    class NormalBalance(models.TextChoices):
        DR = "dr", "Dr"
        CR = "cr", "Cr"

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=Category.choices, db_index=True)
    normal_balance = models.CharField(max_length=2, choices=NormalBalance.choices, db_index=True)

    def __str__(self):
        return self.name


class COA(BranchScopedStampedOwnedActive):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=60, db_index=True)
    description = models.TextField(null=True, blank=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
    )
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT, related_name="accounts")
    is_group = models.BooleanField(default=False)
    is_system = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.name}"


class AccountBalance(BranchScopedStampedOwnedActive):
    account = models.ForeignKey(COA, on_delete=models.PROTECT, related_name="balances")
    as_of_date = models.DateField(db_index=True)
    debit_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    credit_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.account} @ {self.as_of_date}"


class BankAccount(BranchScopedStampedOwnedActive):
    class Type(models.TextChoices):
        BANK = "bank", "Bank"
        CASH = "cash", "Cash"

    class BankAccountType(models.TextChoices):
        SAVING = "saving", "Saving"
        CURRENT = "current", "Current"

    type = models.CharField(max_length=10, choices=Type.choices, db_index=True)
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    display_name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, null=True, blank=True, db_index=True)

    account_name = models.CharField(max_length=150, null=True, blank=True)
    account_number = models.CharField(max_length=80, null=True, blank=True)
    account_type = models.CharField(max_length=10, choices=BankAccountType.choices, null=True, blank=True)

    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True, blank=True, related_name="bank_accounts")
    coa_account = models.ForeignKey(COA, on_delete=models.PROTECT, null=True, blank=True, related_name="linked_bank_accounts")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.display_name


class CashTransfer(TransactionBasedBranchScopedStampedOwnedActive):
    transfer_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    transfer_date = models.DateField(db_index=True)
    from_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, related_name="cash_transfers_out")
    reference_no = models.CharField(max_length=80, null=True, blank=True)

    # override base total to match your blueprint (18,2)
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.transfer_no or str(self.id)


class CashTransferItem(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    cash_transfer = models.ForeignKey(CashTransfer, on_delete=models.CASCADE, related_name="items")
    to_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, related_name="cash_transfers_in")
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ChequeRegister(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        ISSUED = "issued", "Issued"
        RECEIVED = "received", "Received"
        CLEARED = "cleared", "Cleared"
        BOUNCED = "bounced", "Bounced"
        CANCELLED = "cancelled", "Cancelled"

    cheque_no = models.CharField(max_length=80, null=True, blank=True, db_index=True)
    coa_account = models.ForeignKey(COA, on_delete=models.PROTECT, null=True, blank=True, related_name="cheques")
    bank_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, null=True, blank=True, related_name="cheques")

    # Contact is CRM; keep FK as string so accounting app doesn't hard-depend on crm app
    contact = models.ForeignKey("crm.Contact", on_delete=models.PROTECT, null=True, blank=True, related_name="cheques")

    cheque_date = models.DateField(null=True, blank=True)
    received_date = models.DateField(null=True, blank=True)

    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.RECEIVED, db_index=True)
    memo = models.CharField(max_length=255, null=True, blank=True)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.cheque_no or str(self.id)


class JournalVoucher(TransactionBasedBranchScopedStampedOwnedActive):
    voucher_no = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    voucher_date = models.DateField(db_index=True)
    narration = models.TextField(null=True, blank=True)

    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.voucher_no or str(self.id)


class JournalVoucherItem(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    journal_voucher = models.ForeignKey(JournalVoucher, on_delete=models.CASCADE, related_name="items")
    account = models.ForeignKey(COA, on_delete=models.PROTECT, related_name="journal_lines")
    dr_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    cr_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    line_note = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
