from core.utils.BaseModelViewSet import BaseModelViewSet
from .models import (
    POSRegister,
    POSShift,
    POSSession,
    POSCashMovement,
    POSPaymentMethod,
    POSOrder,
    POSOrderItem,
    POSPayment,
    POSReceipt,
    POSReturn,
    POSReturnItem,
    POSDiscountProfile,
    POSTaxProfile,
)
from .serializers import (
    POSRegisterSerializer,
    POSShiftSerializer,
    POSSessionSerializer,
    POSCashMovementSerializer,
    POSPaymentMethodSerializer,
    POSOrderSerializer,
    POSOrderItemSerializer,
    POSPaymentSerializer,
    POSReceiptSerializer,
    POSReturnSerializer,
    POSReturnItemSerializer,
    POSDiscountProfileSerializer,
    POSTaxProfileSerializer,
)
from .filters import (
    POSRegisterFilter,
    POSShiftFilter,
    POSSessionFilter,
    POSCashMovementFilter,
    POSPaymentMethodFilter,
    POSOrderFilter,
    POSOrderItemFilter,
    POSPaymentFilter,
    POSReceiptFilter,
    POSReturnFilter,
    POSReturnItemFilter,
    POSDiscountProfileFilter,
    POSTaxProfileFilter,
)


class POSRegisterViewSet(BaseModelViewSet):
    queryset = POSRegister.objects.select_related("warehouse", "cash_account", "branch").all()
    serializer_class = POSRegisterSerializer
    filterset_class = POSRegisterFilter
    search_fields = ["name", "code"]


class POSShiftViewSet(BaseModelViewSet):
    queryset = POSShift.objects.select_related("register", "opened_by", "closed_by", "branch").all()
    serializer_class = POSShiftSerializer
    filterset_class = POSShiftFilter
    search_fields = ["note"]


class POSSessionViewSet(BaseModelViewSet):
    queryset = POSSession.objects.select_related("shift", "branch").all()
    serializer_class = POSSessionSerializer
    filterset_class = POSSessionFilter
    search_fields = ["device_id"]


class POSCashMovementViewSet(BaseModelViewSet):
    queryset = POSCashMovement.objects.select_related("shift", "branch").all()
    serializer_class = POSCashMovementSerializer
    filterset_class = POSCashMovementFilter
    search_fields = ["reason", "note"]


class POSPaymentMethodViewSet(BaseModelViewSet):
    queryset = POSPaymentMethod.objects.select_related("branch").all()
    serializer_class = POSPaymentMethodSerializer
    filterset_class = POSPaymentMethodFilter
    search_fields = ["name"]


class POSOrderViewSet(BaseModelViewSet):
    queryset = POSOrder.objects.select_related("register", "shift", "customer", "branch").prefetch_related("items").all()
    serializer_class = POSOrderSerializer
    filterset_class = POSOrderFilter
    search_fields = ["order_no", "note"]


class POSOrderItemViewSet(BaseModelViewSet):
    queryset = POSOrderItem.objects.select_related("pos_order", "product_variant", "tax_rate").all()
    serializer_class = POSOrderItemSerializer
    filterset_class = POSOrderItemFilter
    search_fields = ["product_name"]


class POSPaymentViewSet(BaseModelViewSet):
    queryset = POSPayment.objects.select_related("pos_order", "method", "branch").all()
    serializer_class = POSPaymentSerializer
    filterset_class = POSPaymentFilter
    search_fields = ["reference", "note"]


class POSReceiptViewSet(BaseModelViewSet):
    queryset = POSReceipt.objects.select_related("pos_order", "branch").all()
    serializer_class = POSReceiptSerializer
    filterset_class = POSReceiptFilter
    search_fields = ["receipt_no"]


class POSReturnViewSet(BaseModelViewSet):
    queryset = POSReturn.objects.select_related("pos_order", "customer", "branch").prefetch_related("items").all()
    serializer_class = POSReturnSerializer
    filterset_class = POSReturnFilter
    search_fields = ["return_no", "reason", "note"]


class POSReturnItemViewSet(BaseModelViewSet):
    queryset = POSReturnItem.objects.select_related("pos_return", "pos_order_item", "product_variant", "tax_rate").all()
    serializer_class = POSReturnItemSerializer
    filterset_class = POSReturnItemFilter
    search_fields = []


class POSDiscountProfileViewSet(BaseModelViewSet):
    queryset = POSDiscountProfile.objects.select_related("branch").all()
    serializer_class = POSDiscountProfileSerializer
    filterset_class = POSDiscountProfileFilter
    search_fields = ["name"]


class POSTaxProfileViewSet(BaseModelViewSet):
    queryset = POSTaxProfile.objects.select_related("tax_rate", "branch").all()
    serializer_class = POSTaxProfileSerializer
    filterset_class = POSTaxProfileFilter
    search_fields = ["name"]
