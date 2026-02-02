from core.utils.BaseModelViewSet import BaseModelViewSet
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
from .serializers import (
    QuotationSerializer,
    QuotationItemSerializer,
    SaleSerializer,
    SaleItemSerializer,
    InvoiceSerializer,
    InvoiceItemSerializer,
    CustomerPaymentSerializer,
    CustomerPaymentAllocationSerializer,
    CreditNoteSerializer,
    CreditNoteLineSerializer,
)
from .filters import (
    QuotationFilter,
    QuotationItemFilter,
    SaleFilter,
    SaleItemFilter,
    InvoiceFilter,
    InvoiceItemFilter,
    CustomerPaymentFilter,
    CustomerPaymentAllocationFilter,
    CreditNoteFilter,
    CreditNoteLineFilter,
)


class QuotationViewSet(BaseModelViewSet):
    queryset = Quotation.objects.select_related("customer", "currency", "branch").prefetch_related("items").all()
    serializer_class = QuotationSerializer
    filterset_class = QuotationFilter
    search_fields = ["quotation_no", "note"]


class QuotationItemViewSet(BaseModelViewSet):
    queryset = QuotationItem.objects.select_related("quotation", "product", "tax_rate").all()
    serializer_class = QuotationItemSerializer
    filterset_class = QuotationItemFilter
    search_fields = ["product_name"]


class SaleViewSet(BaseModelViewSet):
    queryset = Sale.objects.select_related("customer", "currency", "branch").prefetch_related("items").all()
    serializer_class = SaleSerializer
    filterset_class = SaleFilter
    search_fields = ["sale_no", "note"]


class SaleItemViewSet(BaseModelViewSet):
    queryset = SaleItem.objects.select_related("sale", "product", "tax_rate").all()
    serializer_class = SaleItemSerializer
    filterset_class = SaleItemFilter
    search_fields = ["product_name"]


class InvoiceViewSet(BaseModelViewSet):
    queryset = Invoice.objects.select_related("customer", "currency", "branch").prefetch_related("items").all()
    serializer_class = InvoiceSerializer
    filterset_class = InvoiceFilter
    search_fields = ["invoice_no", "note"]


class InvoiceItemViewSet(BaseModelViewSet):
    queryset = InvoiceItem.objects.select_related("invoice", "product", "tax_rate").all()
    serializer_class = InvoiceItemSerializer
    filterset_class = InvoiceItemFilter
    search_fields = ["product_name"]


class CustomerPaymentViewSet(BaseModelViewSet):
    queryset = CustomerPayment.objects.select_related("customer", "currency", "bank_account", "branch").prefetch_related(
        "allocations"
    ).all()
    serializer_class = CustomerPaymentSerializer
    filterset_class = CustomerPaymentFilter
    search_fields = ["payment_no", "reference", "note"]


class CustomerPaymentAllocationViewSet(BaseModelViewSet):
    queryset = CustomerPaymentAllocation.objects.select_related("customer_payment", "invoice").all()
    serializer_class = CustomerPaymentAllocationSerializer
    filterset_class = CustomerPaymentAllocationFilter
    search_fields = ["note"]


class CreditNoteViewSet(BaseModelViewSet):
    queryset = CreditNote.objects.select_related("customer", "invoice", "currency", "branch").prefetch_related("lines").all()
    serializer_class = CreditNoteSerializer
    filterset_class = CreditNoteFilter
    search_fields = ["credit_note_no", "reason", "note"]


class CreditNoteLineViewSet(BaseModelViewSet):
    queryset = CreditNoteLine.objects.select_related("credit_note", "product", "tax_rate").all()
    serializer_class = CreditNoteLineSerializer
    filterset_class = CreditNoteLineFilter
    search_fields = ["description"]
