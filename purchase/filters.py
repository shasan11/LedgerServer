import django_filters as filters
from .models import (
    PurchaseOrder,
    PurchaseOrderLine,
    PurchaseBill,
    PurchaseBillLine,
    Expense,
    ExpenseLine,
    SupplierPayment,
    SupplierPaymentLine,
    DebitNote,
    DebitNoteLine,
)


class PurchaseOrderFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    supplier = filters.UUIDFilter(field_name="supplier_id")
    po_no = filters.CharFilter(field_name="po_no", lookup_expr="icontains")
    po_date = filters.DateFromToRangeFilter(field_name="po_date")
    expected_date = filters.DateFromToRangeFilter(field_name="expected_date")
    status = filters.CharFilter(field_name="status")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = PurchaseOrder
        fields = ["branch", "supplier", "po_no", "po_date", "expected_date", "status", "active"]


class PurchaseOrderLineFilter(filters.FilterSet):
    purchase_order = filters.UUIDFilter(field_name="purchase_order_id")
    product = filters.UUIDFilter(field_name="product_id")
    tax_rate = filters.UUIDFilter(field_name="tax_rate_id")
    created = filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = PurchaseOrderLine
        fields = ["purchase_order", "product", "tax_rate", "created"]


class PurchaseBillFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    supplier = filters.UUIDFilter(field_name="supplier_id")
    bill_no = filters.CharFilter(field_name="bill_no", lookup_expr="icontains")
    bill_date = filters.DateFromToRangeFilter(field_name="bill_date")
    due_date = filters.DateFromToRangeFilter(field_name="due_date")
    status = filters.CharFilter(field_name="status")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = PurchaseBill
        fields = ["branch", "supplier", "bill_no", "bill_date", "due_date", "status", "active"]


class PurchaseBillLineFilter(filters.FilterSet):
    purchase_bill = filters.UUIDFilter(field_name="purchase_bill_id")
    product = filters.UUIDFilter(field_name="product_id")
    tax_rate = filters.UUIDFilter(field_name="tax_rate_id")
    created = filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = PurchaseBillLine
        fields = ["purchase_bill", "product", "tax_rate", "created"]


class ExpenseFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    supplier = filters.UUIDFilter(field_name="supplier_id")
    expense_no = filters.CharFilter(field_name="expense_no", lookup_expr="icontains")
    expense_date = filters.DateFromToRangeFilter(field_name="expense_date")
    status = filters.CharFilter(field_name="status")
    expense_account = filters.UUIDFilter(field_name="expense_account_id")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Expense
        fields = ["branch", "supplier", "expense_no", "expense_date", "status", "expense_account", "active"]


class ExpenseLineFilter(filters.FilterSet):
    expense = filters.UUIDFilter(field_name="expense_id")
    product = filters.UUIDFilter(field_name="product_id")
    tax_rate = filters.UUIDFilter(field_name="tax_rate_id")
    created = filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = ExpenseLine
        fields = ["expense", "product", "tax_rate", "created"]


class SupplierPaymentFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    supplier = filters.UUIDFilter(field_name="supplier_id")
    payment_no = filters.CharFilter(field_name="payment_no", lookup_expr="icontains")
    payment_date = filters.DateFromToRangeFilter(field_name="payment_date")
    method = filters.CharFilter(field_name="method")
    status = filters.CharFilter(field_name="status")
    bank_account = filters.UUIDFilter(field_name="bank_account_id")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = SupplierPayment
        fields = ["branch", "supplier", "payment_no", "payment_date", "method", "status", "bank_account", "active"]


class SupplierPaymentLineFilter(filters.FilterSet):
    supplier_payment = filters.UUIDFilter(field_name="supplier_payment_id")
    purchase_bill = filters.UUIDFilter(field_name="purchase_bill_id")
    created = filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = SupplierPaymentLine
        fields = ["supplier_payment", "purchase_bill", "created"]


class DebitNoteFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    supplier = filters.UUIDFilter(field_name="supplier_id")
    debit_note_no = filters.CharFilter(field_name="debit_note_no", lookup_expr="icontains")
    debit_note_date = filters.DateFromToRangeFilter(field_name="debit_note_date")
    purchase_bill = filters.UUIDFilter(field_name="purchase_bill_id")
    status = filters.CharFilter(field_name="status")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = DebitNote
        fields = ["branch", "supplier", "debit_note_no", "debit_note_date", "purchase_bill", "status", "active"]


class DebitNoteLineFilter(filters.FilterSet):
    debit_note = filters.UUIDFilter(field_name="debit_note_id")
    product = filters.UUIDFilter(field_name="product_id")
    tax_rate = filters.UUIDFilter(field_name="tax_rate_id")
    created = filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = DebitNoteLine
        fields = ["debit_note", "product", "tax_rate", "created"]
