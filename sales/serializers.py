import uuid
from rest_framework import serializers
from core.utils.AdaptedBulkListSerializer import BulkModelSerializer
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


class QuotationItemSerializer(BulkModelSerializer):
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
        model = QuotationItem
        fields = (
            "id",
            "quotation",
            "product",
            "product_name",
            "qty",
            "rate",
            "discount_amount",
            "tax_rate",
            "line_total",
            "created",
            "updated",
        )
        read_only_fields = ("quotation", "created", "updated")


class QuotationSerializer(BulkModelSerializer):
    customer = ReadablePKField(queryset=None)
    currency = ReadablePKField(queryset=None, required=False, allow_null=True)
    items = QuotationItemSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact
        from master.models import Currency

        self.fields["customer"].queryset = Contact.objects.all()
        self.fields["currency"].queryset = Currency.objects.all()

    class Meta:
        model = Quotation
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_item_uuid(self, item):
        if not item.get("id"):
            item["id"] = uuid.uuid4()
        return item

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        obj = Quotation.objects.create(**validated_data)

        for item in items_data:
            item = self._ensure_item_uuid(item)
            QuotationItem.objects.create(quotation=obj, **item)

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
                QuotationItem.objects.create(quotation=instance, **item)

        return instance


class SaleItemSerializer(BulkModelSerializer):
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
        model = SaleItem
        fields = (
            "id",
            "sale",
            "product",
            "product_name",
            "qty",
            "rate",
            "discount_amount",
            "tax_rate",
            "line_total",
            "created",
            "updated",
        )
        read_only_fields = ("sale", "created", "updated")


class SaleSerializer(BulkModelSerializer):
    customer = ReadablePKField(queryset=None)
    currency = ReadablePKField(queryset=None, required=False, allow_null=True)
    items = SaleItemSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact
        from master.models import Currency

        self.fields["customer"].queryset = Contact.objects.all()
        self.fields["currency"].queryset = Currency.objects.all()

    class Meta:
        model = Sale
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_item_uuid(self, item):
        if not item.get("id"):
            item["id"] = uuid.uuid4()
        return item

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        obj = Sale.objects.create(**validated_data)

        for item in items_data:
            item = self._ensure_item_uuid(item)
            SaleItem.objects.create(sale=obj, **item)

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
                SaleItem.objects.create(sale=instance, **item)

        return instance


class InvoiceItemSerializer(BulkModelSerializer):
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
        model = InvoiceItem
        fields = (
            "id",
            "invoice",
            "product",
            "product_name",
            "qty",
            "rate",
            "discount_amount",
            "tax_rate",
            "line_total",
            "created",
            "updated",
        )
        read_only_fields = ("invoice", "created", "updated")


class InvoiceSerializer(BulkModelSerializer):
    customer = ReadablePKField(queryset=None)
    currency = ReadablePKField(queryset=None, required=False, allow_null=True)
    items = InvoiceItemSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact
        from master.models import Currency

        self.fields["customer"].queryset = Contact.objects.all()
        self.fields["currency"].queryset = Currency.objects.all()

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_item_uuid(self, item):
        if not item.get("id"):
            item["id"] = uuid.uuid4()
        return item

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        obj = Invoice.objects.create(**validated_data)

        for item in items_data:
            item = self._ensure_item_uuid(item)
            InvoiceItem.objects.create(invoice=obj, **item)

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
                InvoiceItem.objects.create(invoice=instance, **item)

        return instance


class CustomerPaymentAllocationSerializer(BulkModelSerializer):
    id = serializers.UUIDField(required=False)
    invoice = ReadablePKField(queryset=Invoice.objects.all())

    class Meta:
        model = CustomerPaymentAllocation
        fields = ("id", "customer_payment", "invoice", "allocated_amount", "note", "created", "updated")
        read_only_fields = ("customer_payment", "created", "updated")


class CustomerPaymentSerializer(BulkModelSerializer):
    customer = ReadablePKField(queryset=None)
    currency = ReadablePKField(queryset=None, required=False, allow_null=True)
    bank_account = ReadablePKField(queryset=None, required=False, allow_null=True)
    allocations = CustomerPaymentAllocationSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact
        from master.models import Currency
        from accounting.models import BankAccount

        self.fields["customer"].queryset = Contact.objects.all()
        self.fields["currency"].queryset = Currency.objects.all()
        self.fields["bank_account"].queryset = BankAccount.objects.all()

    class Meta:
        model = CustomerPayment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_allocation_uuid(self, allocation):
        if not allocation.get("id"):
            allocation["id"] = uuid.uuid4()
        return allocation

    def create(self, validated_data):
        allocations_data = validated_data.pop("allocations", [])
        obj = CustomerPayment.objects.create(**validated_data)

        for allocation in allocations_data:
            allocation = self._ensure_allocation_uuid(allocation)
            CustomerPaymentAllocation.objects.create(customer_payment=obj, **allocation)

        return obj

    def update(self, instance, validated_data):
        allocations_data = validated_data.pop("allocations", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        if allocations_data is not None:
            instance.allocations.all().delete()
            for allocation in allocations_data:
                allocation = self._ensure_allocation_uuid(allocation)
                CustomerPaymentAllocation.objects.create(customer_payment=instance, **allocation)

        return instance


class CreditNoteLineSerializer(BulkModelSerializer):
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
        model = CreditNoteLine
        fields = (
            "id",
            "credit_note",
            "product",
            "description",
            "qty",
            "rate",
            "tax_rate",
            "line_total",
            "created",
            "updated",
        )
        read_only_fields = ("credit_note", "created", "updated")


class CreditNoteSerializer(BulkModelSerializer):
    customer = ReadablePKField(queryset=None)
    invoice = ReadablePKField(queryset=Invoice.objects.all(), required=False, allow_null=True)
    currency = ReadablePKField(queryset=None, required=False, allow_null=True)
    lines = CreditNoteLineSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact
        from master.models import Currency

        self.fields["customer"].queryset = Contact.objects.all()
        self.fields["currency"].queryset = Currency.objects.all()

    class Meta:
        model = CreditNote
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_line_uuid(self, line):
        if not line.get("id"):
            line["id"] = uuid.uuid4()
        return line

    def create(self, validated_data):
        lines_data = validated_data.pop("lines", [])
        obj = CreditNote.objects.create(**validated_data)

        for line in lines_data:
            line = self._ensure_line_uuid(line)
            CreditNoteLine.objects.create(credit_note=obj, **line)

        return obj

    def update(self, instance, validated_data):
        lines_data = validated_data.pop("lines", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        if lines_data is not None:
            instance.lines.all().delete()
            for line in lines_data:
                line = self._ensure_line_uuid(line)
                CreditNoteLine.objects.create(credit_note=instance, **line)

        return instance
