from django.urls import path, include
from rest_framework_bulk.routes import BulkRouter
from .views import (
    QuotationViewSet,
    QuotationItemViewSet,
    SaleViewSet,
    SaleItemViewSet,
    InvoiceViewSet,
    InvoiceItemViewSet,
    CustomerPaymentViewSet,
    CustomerPaymentAllocationViewSet,
    CreditNoteViewSet,
    CreditNoteLineViewSet,
)

router = BulkRouter()
router.register(r"quotations", QuotationViewSet, basename="quotation")
router.register(r"quotation-items", QuotationItemViewSet, basename="quotation-item")
router.register(r"sales", SaleViewSet, basename="sale")
router.register(r"sale-items", SaleItemViewSet, basename="sale-item")
router.register(r"invoices", InvoiceViewSet, basename="invoice")
router.register(r"invoice-items", InvoiceItemViewSet, basename="invoice-item")
router.register(r"customer-payments", CustomerPaymentViewSet, basename="customer-payment")
router.register(r"customer-payment-allocations", CustomerPaymentAllocationViewSet, basename="customer-payment-allocation")
router.register(r"credit-notes", CreditNoteViewSet, basename="credit-note")
router.register(r"credit-note-lines", CreditNoteLineViewSet, basename="credit-note-line")

urlpatterns = [
    path("", include(router.urls)),
]
