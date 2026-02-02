import uuid
from rest_framework import serializers
from core.utils.AdaptedBulkListSerializer import BulkModelSerializer
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


class ReadablePKField(serializers.PrimaryKeyRelatedField):
    """Shows readable string in response while still being PK-based."""

    def __init__(self, *args, **kwargs):
        self._placeholder_queryset = object()
        if kwargs.get("queryset") is None and not kwargs.get("read_only", False):
            kwargs["queryset"] = self._placeholder_queryset
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if queryset is self._placeholder_queryset:
            return None
        if hasattr(queryset, "all"):
            return queryset.all()
        return queryset

    def to_representation(self, value):
        return {"id": str(value.pk), "label": str(value)}


class POSRegisterSerializer(BulkModelSerializer):
    warehouse = ReadablePKField(queryset=None, required=False, allow_null=True)
    cash_account = ReadablePKField(queryset=None, required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from inventory.models import Warehouse
        from accounting.models import BankAccount

        self.fields["warehouse"].queryset = Warehouse.objects.all()
        self.fields["cash_account"].queryset = BankAccount.objects.all()

    class Meta:
        model = POSRegister
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class POSShiftSerializer(BulkModelSerializer):
    register = ReadablePKField(queryset=POSRegister.objects.all())
    opened_by = ReadablePKField(queryset=None)
    closed_by = ReadablePKField(queryset=None, required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth import get_user_model

        self.fields["opened_by"].queryset = get_user_model().objects.all()
        self.fields["closed_by"].queryset = get_user_model().objects.all()

    class Meta:
        model = POSShift
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class POSSessionSerializer(BulkModelSerializer):
    shift = ReadablePKField(queryset=POSShift.objects.all())

    class Meta:
        model = POSSession
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class POSCashMovementSerializer(BulkModelSerializer):
    shift = ReadablePKField(queryset=POSShift.objects.all())

    class Meta:
        model = POSCashMovement
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class POSPaymentMethodSerializer(BulkModelSerializer):
    class Meta:
        model = POSPaymentMethod
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class POSOrderItemSerializer(BulkModelSerializer):
    id = serializers.UUIDField(required=False)
    product_variant = ReadablePKField(queryset=None)
    tax_rate = ReadablePKField(queryset=None, required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from inventory.models import ProductVariant
        from master.models import TaxRate

        self.fields["product_variant"].queryset = ProductVariant.objects.all()
        self.fields["tax_rate"].queryset = TaxRate.objects.all()

    class Meta:
        model = POSOrderItem
        fields = (
            "id",
            "pos_order",
            "product_variant",
            "product_name",
            "qty",
            "unit_price",
            "discount_amount",
            "tax_rate",
            "line_total",
            "created",
            "updated",
        )
        read_only_fields = ("pos_order", "created", "updated")


class POSOrderSerializer(BulkModelSerializer):
    register = ReadablePKField(queryset=POSRegister.objects.all())
    shift = ReadablePKField(queryset=POSShift.objects.all())
    customer = ReadablePKField(queryset=None, required=False, allow_null=True)
    items = POSOrderItemSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact

        self.fields["customer"].queryset = Contact.objects.all()

    class Meta:
        model = POSOrder
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_item_uuid(self, item):
        if not item.get("id"):
            item["id"] = uuid.uuid4()
        return item

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        obj = POSOrder.objects.create(**validated_data)

        for item in items_data:
            item = self._ensure_item_uuid(item)
            POSOrderItem.objects.create(pos_order=obj, **item)

        return obj

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                item = self._ensure_item_uuid(item)
                POSOrderItem.objects.create(pos_order=instance, **item)

        return instance


class POSPaymentSerializer(BulkModelSerializer):
    pos_order = ReadablePKField(queryset=POSOrder.objects.all())
    method = ReadablePKField(queryset=POSPaymentMethod.objects.all())

    class Meta:
        model = POSPayment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class POSReceiptSerializer(BulkModelSerializer):
    pos_order = ReadablePKField(queryset=POSOrder.objects.all())

    class Meta:
        model = POSReceipt
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class POSReturnItemSerializer(BulkModelSerializer):
    id = serializers.UUIDField(required=False)
    pos_order_item = ReadablePKField(queryset=POSOrderItem.objects.all(), required=False, allow_null=True)
    product_variant = ReadablePKField(queryset=None)
    tax_rate = ReadablePKField(queryset=None, required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from inventory.models import ProductVariant
        from master.models import TaxRate

        self.fields["product_variant"].queryset = ProductVariant.objects.all()
        self.fields["tax_rate"].queryset = TaxRate.objects.all()

    class Meta:
        model = POSReturnItem
        fields = (
            "id",
            "pos_return",
            "pos_order_item",
            "product_variant",
            "qty",
            "unit_price",
            "tax_rate",
            "line_total",
            "created",
            "updated",
        )
        read_only_fields = ("pos_return", "created", "updated")


class POSReturnSerializer(BulkModelSerializer):
    pos_order = ReadablePKField(queryset=POSOrder.objects.all(), required=False, allow_null=True)
    customer = ReadablePKField(queryset=None, required=False, allow_null=True)
    items = POSReturnItemSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact

        self.fields["customer"].queryset = Contact.objects.all()

    class Meta:
        model = POSReturn
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_item_uuid(self, item):
        if not item.get("id"):
            item["id"] = uuid.uuid4()
        return item

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        obj = POSReturn.objects.create(**validated_data)

        for item in items_data:
            item = self._ensure_item_uuid(item)
            POSReturnItem.objects.create(pos_return=obj, **item)

        return obj

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                item = self._ensure_item_uuid(item)
                POSReturnItem.objects.create(pos_return=instance, **item)

        return instance


class POSDiscountProfileSerializer(BulkModelSerializer):
    class Meta:
        model = POSDiscountProfile
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class POSTaxProfileSerializer(BulkModelSerializer):
    tax_rate = ReadablePKField(queryset=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from master.models import TaxRate

        self.fields["tax_rate"].queryset = TaxRate.objects.all()

    class Meta:
        model = POSTaxProfile
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")
