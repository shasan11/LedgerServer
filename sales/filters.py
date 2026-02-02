import django_filters as filters
from .models import (
    Quotation,
    QuotationItem,
    Sale,
    SaleItem,
    Invoice,
    InvoiceItem,
    CustomerPayment,
    CustomerPaymentAllocation,
    CreditNote,
    CreditNoteLine,
)


class QuotationFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    customer = filters.UUIDFilter(field_name="customer_id")
    quotation_no = filters.CharFilter(field_name="quotation_no", lookup_expr="icontains")
    quotation_date = filters.DateFromToRangeFilter(field_name="quotation_date")
    valid_until = filters.DateFromToRangeFilter(field_name="valid_until")
    status = filters.CharFilter(field_name="status")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Quotation
        fields = ["branch", "customer", "quotation_no", "quotation_date", "valid_until", "status", "active"]


class QuotationItemFilter(filters.FilterSet):
    quotation = filters.UUIDFilter(field_name="quotation_id")
    product = filters.UUIDFilter(field_name="product_id")
    tax_rate = filters.UUIDFilter(field_name="tax_rate_id")
    created = filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = QuotationItem
        fields = ["quotation", "product", "tax_rate", "created"]


class SaleFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    customer = filters.UUIDFilter(field_name="customer_id")
    sale_no = filters.CharFilter(field_name="sale_no", lookup_expr="icontains")
    sale_date = filters.DateFromToRangeFilter(field_name="sale_date")
    status = filters.CharFilter(field_name="status")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Sale
        fields = ["branch", "customer", "sale_no", "sale_date", "status", "active"]


class SaleItemFilter(filters.FilterSet):
    sale = filters.UUIDFilter(field_name="sale_id")
    product = filters.UUIDFilter(field_name="product_id")
    tax_rate = filters.UUIDFilter(field_name="tax_rate_id")
    created = filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = SaleItem
        fields = ["sale", "product", "tax_rate", "created"]


class InvoiceFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    customer = filters.UUIDFilter(field_name="customer_id")
    invoice_no = filters.CharFilter(field_name="invoice_no", lookup_expr="icontains")
    invoice_date = filters.DateFromToRangeFilter(field_name="invoice_date")
    due_date = filters.DateFromToRangeFilter(field_name="due_date")
    status = filters.CharFilter(field_name="status")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Invoice
        fields = ["branch", "customer", "invoice_no", "invoice_date", "due_date", "status", "active"]


class InvoiceItemFilter(filters.FilterSet):
    invoice = filters.UUIDFilter(field_name="invoice_id")
    product = filters.UUIDFilter(field_name="product_id")
    tax_rate = filters.UUIDFilter(field_name="tax_rate_id")
    created = filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = InvoiceItem
        fields = ["invoice", "product", "tax_rate", "created"]


class CustomerPaymentFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    customer = filters.UUIDFilter(field_name="customer_id")
    payment_no = filters.CharFilter(field_name="payment_no", lookup_expr="icontains")
    payment_date = filters.DateFromToRangeFilter(field_name="payment_date")
    method = filters.CharFilter(field_name="method")
    status = filters.CharFilter(field_name="status")
    bank_account = filters.UUIDFilter(field_name="bank_account_id")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = CustomerPayment
        fields = [
            "branch",
            "customer",
            "payment_no",
            "payment_date",
            "method",
            "status",
            "bank_account",
            "active",
        ]


class CustomerPaymentAllocationFilter(filters.FilterSet):
    customer_payment = filters.UUIDFilter(field_name="customer_payment_id")
    invoice = filters.UUIDFilter(field_name="invoice_id")
    created = filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = CustomerPaymentAllocation
        fields = ["customer_payment", "invoice", "created"]


class CreditNoteFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    customer = filters.UUIDFilter(field_name="customer_id")
    credit_note_no = filters.CharFilter(field_name="credit_note_no", lookup_expr="icontains")
    credit_note_date = filters.DateFromToRangeFilter(field_name="credit_note_date")
    invoice = filters.UUIDFilter(field_name="invoice_id")
    status = filters.CharFilter(field_name="status")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = CreditNote
        fields = ["branch", "customer", "credit_note_no", "credit_note_date", "invoice", "status", "active"]


class CreditNoteLineFilter(filters.FilterSet):
    credit_note = filters.UUIDFilter(field_name="credit_note_id")
    product = filters.UUIDFilter(field_name="product_id")
    tax_rate = filters.UUIDFilter(field_name="tax_rate_id")
    created = filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = CreditNoteLine
        fields = ["credit_note", "product", "tax_rate", "created"]
