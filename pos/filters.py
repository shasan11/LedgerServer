import django_filters as filters
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


class POSRegisterFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    warehouse = filters.UUIDFilter(field_name="warehouse_id")
    cash_account = filters.UUIDFilter(field_name="cash_account_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = POSRegister
        fields = ["branch", "warehouse", "cash_account", "name", "code", "active"]


class POSShiftFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    register = filters.UUIDFilter(field_name="register_id")
    opened_at = filters.DateTimeFromToRangeFilter(field_name="opened_at")
    opened_by = filters.UUIDFilter(field_name="opened_by_id")
    closed_by = filters.UUIDFilter(field_name="closed_by_id")
    status = filters.CharFilter(field_name="status")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = POSShift
        fields = ["branch", "register", "opened_at", "opened_by", "closed_by", "status", "active"]


class POSSessionFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    shift = filters.UUIDFilter(field_name="shift_id")
    device_id = filters.CharFilter(field_name="device_id", lookup_expr="icontains")
    started_at = filters.DateTimeFromToRangeFilter(field_name="started_at")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = POSSession
        fields = ["branch", "shift", "device_id", "started_at", "active"]


class POSCashMovementFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    shift = filters.UUIDFilter(field_name="shift_id")
    type = filters.CharFilter(field_name="type")
    amount = filters.RangeFilter(field_name="amount")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = POSCashMovement
        fields = ["branch", "shift", "type", "amount", "active"]


class POSPaymentMethodFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    type = filters.CharFilter(field_name="type")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = POSPaymentMethod
        fields = ["branch", "name", "type", "active"]


class POSOrderFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    register = filters.UUIDFilter(field_name="register_id")
    shift = filters.UUIDFilter(field_name="shift_id")
    customer = filters.UUIDFilter(field_name="customer_id")
    order_no = filters.CharFilter(field_name="order_no", lookup_expr="icontains")
    order_date = filters.DateTimeFromToRangeFilter(field_name="order_date")
    status = filters.CharFilter(field_name="status")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = POSOrder
        fields = ["branch", "register", "shift", "customer", "order_no", "order_date", "status", "active"]


class POSOrderItemFilter(filters.FilterSet):
    pos_order = filters.UUIDFilter(field_name="pos_order_id")
    product_variant = filters.UUIDFilter(field_name="product_variant_id")
    tax_rate = filters.UUIDFilter(field_name="tax_rate_id")
    created = filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = POSOrderItem
        fields = ["pos_order", "product_variant", "tax_rate", "created"]


class POSPaymentFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    pos_order = filters.UUIDFilter(field_name="pos_order_id")
    method = filters.UUIDFilter(field_name="method_id")
    status = filters.CharFilter(field_name="status")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = POSPayment
        fields = ["branch", "pos_order", "method", "status", "active"]


class POSReceiptFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    pos_order = filters.UUIDFilter(field_name="pos_order_id")
    receipt_no = filters.CharFilter(field_name="receipt_no", lookup_expr="icontains")
    printed_at = filters.DateTimeFromToRangeFilter(field_name="printed_at")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = POSReceipt
        fields = ["branch", "pos_order", "receipt_no", "printed_at", "active"]


class POSReturnFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    pos_order = filters.UUIDFilter(field_name="pos_order_id")
    customer = filters.UUIDFilter(field_name="customer_id")
    return_no = filters.CharFilter(field_name="return_no", lookup_expr="icontains")
    return_date = filters.DateTimeFromToRangeFilter(field_name="return_date")
    status = filters.CharFilter(field_name="status")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = POSReturn
        fields = ["branch", "pos_order", "customer", "return_no", "return_date", "status", "active"]


class POSReturnItemFilter(filters.FilterSet):
    pos_return = filters.UUIDFilter(field_name="pos_return_id")
    pos_order_item = filters.UUIDFilter(field_name="pos_order_item_id")
    product_variant = filters.UUIDFilter(field_name="product_variant_id")
    tax_rate = filters.UUIDFilter(field_name="tax_rate_id")
    created = filters.DateTimeFromToRangeFilter(field_name="created")

    class Meta:
        model = POSReturnItem
        fields = ["pos_return", "pos_order_item", "product_variant", "tax_rate", "created"]


class POSDiscountProfileFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    discount_type = filters.CharFilter(field_name="discount_type")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = POSDiscountProfile
        fields = ["branch", "name", "discount_type", "active"]


class POSTaxProfileFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    tax_rate = filters.UUIDFilter(field_name="tax_rate_id")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = POSTaxProfile
        fields = ["branch", "name", "tax_rate", "active"]
