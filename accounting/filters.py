import django_filters as filters
from .models import (
    AccountType,
    COA,
    AccountBalance,
    BankAccount,
    CashTransfer,
    ChequeRegister,
    JournalVoucher,
)


class AccountTypeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    category = filters.CharFilter(field_name="category")
    normal_balance = filters.CharFilter(field_name="normal_balance")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = AccountType
        fields = ["name", "category", "normal_balance", "active"]


class COAFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    parent = filters.UUIDFilter(field_name="parent_id")
    account_type = filters.UUIDFilter(field_name="account_type_id")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    is_group = filters.BooleanFilter(field_name="is_group")
    is_system = filters.BooleanFilter(field_name="is_system")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = COA
        fields = ["branch", "parent", "account_type", "code", "name", "is_group", "is_system", "active"]


class AccountBalanceFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    account = filters.UUIDFilter(field_name="account_id")
    as_of_date = filters.DateFromToRangeFilter(field_name="as_of_date")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = AccountBalance
        fields = ["branch", "account", "as_of_date", "active"]


class BankAccountFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    type = filters.CharFilter(field_name="type")
    currency = filters.UUIDFilter(field_name="currency_id")
    coa_account = filters.UUIDFilter(field_name="coa_account_id")
    display_name = filters.CharFilter(field_name="display_name", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = BankAccount
        fields = ["branch", "type", "currency", "coa_account", "display_name", "code", "active"]


class CashTransferFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    transfer_no = filters.CharFilter(field_name="transfer_no", lookup_expr="icontains")
    transfer_date = filters.DateFromToRangeFilter(field_name="transfer_date")
    from_account = filters.UUIDFilter(field_name="from_account_id")
    approved = filters.BooleanFilter(field_name="approved")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = CashTransfer
        fields = ["branch", "transfer_no", "transfer_date", "from_account", "approved", "active"]


class ChequeRegisterFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    cheque_no = filters.CharFilter(field_name="cheque_no", lookup_expr="icontains")
    status = filters.CharFilter(field_name="status")
    cheque_date = filters.DateFromToRangeFilter(field_name="cheque_date")
    received_date = filters.DateFromToRangeFilter(field_name="received_date")
    bank_account = filters.UUIDFilter(field_name="bank_account_id")
    contact = filters.UUIDFilter(field_name="contact_id")
    approved = filters.BooleanFilter(field_name="approved")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = ChequeRegister
        fields = ["branch", "cheque_no", "status", "cheque_date", "received_date", "bank_account", "contact", "approved", "active"]


class JournalVoucherFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    voucher_no = filters.CharFilter(field_name="voucher_no", lookup_expr="icontains")
    voucher_date = filters.DateFromToRangeFilter(field_name="voucher_date")
    approved = filters.BooleanFilter(field_name="approved")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = JournalVoucher
        fields = ["branch", "voucher_no", "voucher_date", "approved", "active"]
