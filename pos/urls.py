from django.urls import path, include
from rest_framework_bulk.routes import BulkRouter
from .views import (
    POSRegisterViewSet,
    POSShiftViewSet,
    POSSessionViewSet,
    POSCashMovementViewSet,
    POSPaymentMethodViewSet,
    POSOrderViewSet,
    POSOrderItemViewSet,
    POSPaymentViewSet,
    POSReceiptViewSet,
    POSReturnViewSet,
    POSReturnItemViewSet,
    POSDiscountProfileViewSet,
    POSTaxProfileViewSet,
)

router = BulkRouter()
router.register(r"registers", POSRegisterViewSet, basename="pos-register")
router.register(r"shifts", POSShiftViewSet, basename="pos-shift")
router.register(r"sessions", POSSessionViewSet, basename="pos-session")
router.register(r"cash-movements", POSCashMovementViewSet, basename="pos-cash-movement")
router.register(r"payment-methods", POSPaymentMethodViewSet, basename="pos-payment-method")
router.register(r"orders", POSOrderViewSet, basename="pos-order")
router.register(r"order-items", POSOrderItemViewSet, basename="pos-order-item")
router.register(r"payments", POSPaymentViewSet, basename="pos-payment")
router.register(r"receipts", POSReceiptViewSet, basename="pos-receipt")
router.register(r"returns", POSReturnViewSet, basename="pos-return")
router.register(r"return-items", POSReturnItemViewSet, basename="pos-return-item")
router.register(r"discount-profiles", POSDiscountProfileViewSet, basename="pos-discount-profile")
router.register(r"tax-profiles", POSTaxProfileViewSet, basename="pos-tax-profile")

urlpatterns = [
    path("", include(router.urls)),
]
