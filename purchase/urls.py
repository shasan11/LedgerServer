from django.urls import path, include
from rest_framework_bulk.routes import BulkRouter
from .views import (
    PurchaseOrderViewSet,
    PurchaseOrderLineViewSet,
    PurchaseBillViewSet,
    PurchaseBillLineViewSet,
    ExpenseViewSet,
    ExpenseLineViewSet,
    SupplierPaymentViewSet,
    SupplierPaymentLineViewSet,
    DebitNoteViewSet,
    DebitNoteLineViewSet,
)

router = BulkRouter()
router.register(r"purchase-orders", PurchaseOrderViewSet, basename="purchase-order")
router.register(r"purchase-order-lines", PurchaseOrderLineViewSet, basename="purchase-order-line")
router.register(r"purchase-bills", PurchaseBillViewSet, basename="purchase-bill")
router.register(r"purchase-bill-lines", PurchaseBillLineViewSet, basename="purchase-bill-line")
router.register(r"expenses", ExpenseViewSet, basename="expense")
router.register(r"expense-lines", ExpenseLineViewSet, basename="expense-line")
router.register(r"supplier-payments", SupplierPaymentViewSet, basename="supplier-payment")
router.register(r"supplier-payment-lines", SupplierPaymentLineViewSet, basename="supplier-payment-line")
router.register(r"debit-notes", DebitNoteViewSet, basename="debit-note")
router.register(r"debit-note-lines", DebitNoteLineViewSet, basename="debit-note-line")

urlpatterns = [
    path("", include(router.urls)),
]
