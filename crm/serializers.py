import uuid
from rest_framework import serializers
from core.utils.AdaptedBulkListSerializer import BulkModelSerializer
from .models import ContactGroup, Contact, Deal, DealItem, Activity


class ReadablePKField(serializers.PrimaryKeyRelatedField):
    """Shows readable string in response while still being PK-based."""

    def to_representation(self, value):
        return {"id": str(value.pk), "label": str(value)}


class ContactGroupSerializer(BulkModelSerializer):
    parent = ReadablePKField(queryset=ContactGroup.objects.all(), required=False, allow_null=True)

    class Meta:
        model = ContactGroup
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class ContactSerializer(BulkModelSerializer):
    group = ReadablePKField(queryset=ContactGroup.objects.all(), required=False, allow_null=True)
    receivable_account = ReadablePKField(queryset=None, required=False, allow_null=True)
    payable_account = ReadablePKField(queryset=None, required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounting.models import COA

        self.fields["receivable_account"].queryset = COA.objects.all()
        self.fields["payable_account"].queryset = COA.objects.all()

    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class DealItemSerializer(BulkModelSerializer):
    id = serializers.UUIDField(required=False)
    product = ReadablePKField(queryset=None, required=False, allow_null=True)
    tax_rate = ReadablePKField(queryset=None, required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from inventory.models import Product
        from master.models import TaxRate

        self.fields["product"].queryset = Product.objects.all()
        self.fields["tax_rate"].queryset = TaxRate.objects.all()

    class Meta:
        model = DealItem
        fields = (
            "id",
            "deal",
            "product",
            "description",
            "qty",
            "rate",
            "discount_amount",
            "tax_rate",
            "line_total",
            "created",
            "updated",
        )
        read_only_fields = ("deal", "created", "updated")

    def validate(self, attrs):
        qty = attrs.get("qty")
        if qty is not None and qty < 0:
            raise serializers.ValidationError({"qty": "Quantity cannot be negative."})
        return attrs


class DealSerializer(BulkModelSerializer):
    contact = ReadablePKField(queryset=Contact.objects.all())
    currency = ReadablePKField(queryset=None, required=False, allow_null=True)
    owner = ReadablePKField(queryset=None, required=False, allow_null=True)
    items = DealItemSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from master.models import Currency
        from django.contrib.auth import get_user_model

        self.fields["currency"].queryset = Currency.objects.all()
        self.fields["owner"].queryset = get_user_model().objects.all()

    class Meta:
        model = Deal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_item_uuid(self, item):
        if not item.get("id"):
            item["id"] = uuid.uuid4()
        return item

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        obj = Deal.objects.create(**validated_data)

        for item in items_data:
            item = self._ensure_item_uuid(item)
            item.setdefault("branch", obj.branch)
            DealItem.objects.create(deal=obj, **item)

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
                item.setdefault("branch", instance.branch)
                DealItem.objects.create(deal=instance, **item)

        return instance


class ActivitySerializer(BulkModelSerializer):
    contact = ReadablePKField(queryset=Contact.objects.all(), required=False, allow_null=True)
    deal = ReadablePKField(queryset=Deal.objects.all(), required=False, allow_null=True)
    assigned_to = ReadablePKField(queryset=None, required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth import get_user_model

        self.fields["assigned_to"].queryset = get_user_model().objects.all()

    class Meta:
        model = Activity
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")
