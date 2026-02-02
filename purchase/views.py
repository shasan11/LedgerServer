from core.utils.BaseModelViewSet import BaseModelViewSet
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
from .serializers import (
    PurchaseOrderSerializer,
    PurchaseOrderLineSerializer,
    PurchaseBillSerializer,
    PurchaseBillLineSerializer,
    ExpenseSerializer,
    ExpenseLineSerializer,
    SupplierPaymentSerializer,
    SupplierPaymentLineSerializer,
    DebitNoteSerializer,
    DebitNoteLineSerializer,
)
from .filters import (
    PurchaseOrderFilter,
    PurchaseOrderLineFilter,
    PurchaseBillFilter,
    PurchaseBillLineFilter,
    ExpenseFilter,
    ExpenseLineFilter,
    SupplierPaymentFilter,
    SupplierPaymentLineFilter,
    DebitNoteFilter,
    DebitNoteLineFilter,
)


class PurchaseOrderViewSet(BaseModelViewSet):
    queryset = PurchaseOrder.objects.select_related("supplier", "currency", "branch").prefetch_related("lines").all()
    serializer_class = PurchaseOrderSerializer
    filterset_class = PurchaseOrderFilter
    search_fields = ["po_no", "note"]


class PurchaseOrderLineViewSet(BaseModelViewSet):
    queryset = PurchaseOrderLine.objects.select_related("purchase_order", "product", "tax_rate").all()
    serializer_class = PurchaseOrderLineSerializer
    filterset_class = PurchaseOrderLineFilter
    search_fields = ["product_name"]


class PurchaseBillViewSet(BaseModelViewSet):
    queryset = PurchaseBill.objects.select_related("supplier", "currency", "branch").prefetch_related("lines").all()
    serializer_class = PurchaseBillSerializer
    filterset_class = PurchaseBillFilter
    search_fields = ["bill_no", "note"]


class PurchaseBillLineViewSet(BaseModelViewSet):
    queryset = PurchaseBillLine.objects.select_related("purchase_bill", "product", "tax_rate").all()
    serializer_class = PurchaseBillLineSerializer
    filterset_class = PurchaseBillLineFilter
    search_fields = ["product_name"]


class ExpenseViewSet(BaseModelViewSet):
    queryset = Expense.objects.select_related("supplier", "currency", "expense_account", "branch").prefetch_related("lines").all()
    serializer_class = ExpenseSerializer
    filterset_class = ExpenseFilter
    search_fields = ["expense_no", "description", "note"]


class ExpenseLineViewSet(BaseModelViewSet):
    queryset = ExpenseLine.objects.select_related("expense", "product", "tax_rate").all()
    serializer_class = ExpenseLineSerializer
    filterset_class = ExpenseLineFilter
    search_fields = ["product_name"]


class SupplierPaymentViewSet(BaseModelViewSet):
    queryset = SupplierPayment.objects.select_related("supplier", "currency", "bank_account", "branch").prefetch_related("lines").all()
    serializer_class = SupplierPaymentSerializer
    filterset_class = SupplierPaymentFilter
    search_fields = ["payment_no", "reference", "note"]


class SupplierPaymentLineViewSet(BaseModelViewSet):
    queryset = SupplierPaymentLine.objects.select_related("supplier_payment", "purchase_bill").all()
    serializer_class = SupplierPaymentLineSerializer
    filterset_class = SupplierPaymentLineFilter
    search_fields = ["note"]


class DebitNoteViewSet(BaseModelViewSet):
    queryset = DebitNote.objects.select_related("supplier", "purchase_bill", "currency", "branch").prefetch_related("lines").all()
    serializer_class = DebitNoteSerializer
    filterset_class = DebitNoteFilter
    search_fields = ["debit_note_no", "reason", "note"]


class DebitNoteLineViewSet(BaseModelViewSet):
    queryset = DebitNoteLine.objects.select_related("debit_note", "product", "tax_rate").all()
    serializer_class = DebitNoteLineSerializer
    filterset_class = DebitNoteLineFilter
    search_fields = ["description"]
