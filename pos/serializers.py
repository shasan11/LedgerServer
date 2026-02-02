# pos/serializers.py

import uuid
from django.apps import apps
from django.contrib.auth import get_user_model
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
from inventory.models import Warehouse


# -----------------------------
# Safe model lookups (no direct imports -> fewer circular import issues)
# -----------------------------
User = get_user_model()
BankAccount = apps.get_model("accounting", "BankAccount")
Contact = apps.get_model("crm", "Contact")
ProductVariant = apps.get_model("inventory", "ProductVariant")
TaxRate = apps.get_model("master", "TaxRate")


class ReadablePKField(serializers.PrimaryKeyRelatedField):
    """Shows readable string in response while still being PK-based."""

    def to_representation(self, value):
        if value is None:
            return None
        return {"id": str(value.pk), "label": str(value)}


# =========================================================
# REGISTER
# =========================================================
class POSRegisterSerializer(BulkModelSerializer):
    # ✅ NEVER queryset=None on relational fields (this was your crash)
    warehouse = ReadablePKField(
        queryset=Warehouse.objects.all(), required=False, allow_null=True
    )
    cash_account = ReadablePKField(
        queryset=BankAccount.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = POSRegister
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


# =========================================================
# SHIFT
# =========================================================
class POSShiftSerializer(BulkModelSerializer):
    register = ReadablePKField(queryset=POSRegister.objects.all())
    opened_by = ReadablePKField(queryset=User.objects.all())
    closed_by = ReadablePKField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = POSShift
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


# =========================================================
# SESSION
# =========================================================
class POSSessionSerializer(BulkModelSerializer):
    shift = ReadablePKField(queryset=POSShift.objects.all())

    class Meta:
        model = POSSession
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


# =========================================================
# CASH MOVEMENT
# =========================================================
class POSCashMovementSerializer(BulkModelSerializer):
    shift = ReadablePKField(queryset=POSShift.objects.all())

    class Meta:
        model = POSCashMovement
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


# =========================================================
# PAYMENT METHOD
# =========================================================
class POSPaymentMethodSerializer(BulkModelSerializer):
    class Meta:
        model = POSPaymentMethod
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


# =========================================================
# ORDER ITEM
# =========================================================
class POSOrderItemSerializer(BulkModelSerializer):
    id = serializers.UUIDField(required=False)

    product_variant = ReadablePKField(queryset=ProductVariant.objects.all())
    tax_rate = ReadablePKField(queryset=TaxRate.objects.all(), required=False, allow_null=True)

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


# =========================================================
# ORDER
# =========================================================
class POSOrderSerializer(BulkModelSerializer):
    register = ReadablePKField(queryset=POSRegister.objects.all())
    shift = ReadablePKField(queryset=POSShift.objects.all())
    customer = ReadablePKField(queryset=Contact.objects.all(), required=False, allow_null=True)

    items = POSOrderItemSerializer(many=True, required=False)

    class Meta:
        model = POSOrder
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_item_uuid(self, item: dict) -> dict:
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


# =========================================================
# PAYMENT
# =========================================================
class POSPaymentSerializer(BulkModelSerializer):
    pos_order = ReadablePKField(queryset=POSOrder.objects.all())
    method = ReadablePKField(queryset=POSPaymentMethod.objects.all())

    class Meta:
        model = POSPayment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


# =========================================================
# RECEIPT
# =========================================================
class POSReceiptSerializer(BulkModelSerializer):
    pos_order = ReadablePKField(queryset=POSOrder.objects.all())

    class Meta:
        model = POSReceipt
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


# =========================================================
# RETURN ITEM
# =========================================================
class POSReturnItemSerializer(BulkModelSerializer):
    id = serializers.UUIDField(required=False)

    pos_order_item = ReadablePKField(
        queryset=POSOrderItem.objects.all(), required=False, allow_null=True
    )
    product_variant = ReadablePKField(queryset=ProductVariant.objects.all())
    tax_rate = ReadablePKField(queryset=TaxRate.objects.all(), required=False, allow_null=True)

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


# =========================================================
# RETURN
# =========================================================
class POSReturnSerializer(BulkModelSerializer):
    pos_order = ReadablePKField(queryset=POSOrder.objects.all(), required=False, allow_null=True)
    customer = ReadablePKField(queryset=Contact.objects.all(), required=False, allow_null=True)

    items = POSReturnItemSerializer(many=True, required=False)

    class Meta:
        model = POSReturn
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_item_uuid(self, item: dict) -> dict:
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


# =========================================================
# DISCOUNT PROFILE
# =========================================================
class POSDiscountProfileSerializer(BulkModelSerializer):
    class Meta:
        model = POSDiscountProfile
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


# =========================================================
# TAX PROFILE
# =========================================================
class POSTaxProfileSerializer(BulkModelSerializer):
    tax_rate = ReadablePKField(queryset=TaxRate.objects.all())

    class Meta:
        model = POSTaxProfile
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")
