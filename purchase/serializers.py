import uuid
from rest_framework import serializers
from core.utils.AdaptedBulkListSerializer import BulkModelSerializer
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


class ReadablePKField(serializers.PrimaryKeyRelatedField):
    """Shows readable string in response while still being PK-based."""

    def to_representation(self, value):
        return {"id": str(value.pk), "label": str(value)}


class PurchaseOrderLineSerializer(BulkModelSerializer):
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
        model = PurchaseOrderLine
        fields = (
            "id",
            "purchase_order",
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
        read_only_fields = ("purchase_order", "created", "updated")


class PurchaseOrderSerializer(BulkModelSerializer):
    supplier = ReadablePKField(queryset=None)
    currency = ReadablePKField(queryset=None, required=False, allow_null=True)
    lines = PurchaseOrderLineSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact
        from master.models import Currency

        self.fields["supplier"].queryset = Contact.objects.all()
        self.fields["currency"].queryset = Currency.objects.all()

    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_line_uuid(self, line):
        if not line.get("id"):
            line["id"] = uuid.uuid4()
        return line

    def create(self, validated_data):
        lines_data = validated_data.pop("lines", [])
        obj = PurchaseOrder.objects.create(**validated_data)

        for line in lines_data:
            line = self._ensure_line_uuid(line)
            PurchaseOrderLine.objects.create(purchase_order=obj, **line)

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
                PurchaseOrderLine.objects.create(purchase_order=instance, **line)

        return instance


class PurchaseBillLineSerializer(BulkModelSerializer):
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
        model = PurchaseBillLine
        fields = (
            "id",
            "purchase_bill",
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
        read_only_fields = ("purchase_bill", "created", "updated")


class PurchaseBillSerializer(BulkModelSerializer):
    supplier = ReadablePKField(queryset=None)
    currency = ReadablePKField(queryset=None, required=False, allow_null=True)
    lines = PurchaseBillLineSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact
        from master.models import Currency

        self.fields["supplier"].queryset = Contact.objects.all()
        self.fields["currency"].queryset = Currency.objects.all()

    class Meta:
        model = PurchaseBill
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_line_uuid(self, line):
        if not line.get("id"):
            line["id"] = uuid.uuid4()
        return line

    def create(self, validated_data):
        lines_data = validated_data.pop("lines", [])
        obj = PurchaseBill.objects.create(**validated_data)

        for line in lines_data:
            line = self._ensure_line_uuid(line)
            PurchaseBillLine.objects.create(purchase_bill=obj, **line)

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
                PurchaseBillLine.objects.create(purchase_bill=instance, **line)

        return instance


class ExpenseLineSerializer(BulkModelSerializer):
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
        model = ExpenseLine
        fields = (
            "id",
            "expense",
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
        read_only_fields = ("expense", "created", "updated")


class ExpenseSerializer(BulkModelSerializer):
    supplier = ReadablePKField(queryset=None, required=False, allow_null=True)
    currency = ReadablePKField(queryset=None, required=False, allow_null=True)
    expense_account = ReadablePKField(queryset=None, required=False, allow_null=True)
    lines = ExpenseLineSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact
        from master.models import Currency
        from accounting.models import COA

        self.fields["supplier"].queryset = Contact.objects.all()
        self.fields["currency"].queryset = Currency.objects.all()
        self.fields["expense_account"].queryset = COA.objects.all()

    class Meta:
        model = Expense
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_line_uuid(self, line):
        if not line.get("id"):
            line["id"] = uuid.uuid4()
        return line

    def create(self, validated_data):
        lines_data = validated_data.pop("lines", [])
        obj = Expense.objects.create(**validated_data)

        for line in lines_data:
            line = self._ensure_line_uuid(line)
            ExpenseLine.objects.create(expense=obj, **line)

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
                ExpenseLine.objects.create(expense=instance, **line)

        return instance


class SupplierPaymentLineSerializer(BulkModelSerializer):
    id = serializers.UUIDField(required=False)
    purchase_bill = ReadablePKField(queryset=PurchaseBill.objects.all())

    class Meta:
        model = SupplierPaymentLine
        fields = ("id", "supplier_payment", "purchase_bill", "allocated_amount", "note", "created", "updated")
        read_only_fields = ("supplier_payment", "created", "updated")


class SupplierPaymentSerializer(BulkModelSerializer):
    supplier = ReadablePKField(queryset=None)
    currency = ReadablePKField(queryset=None, required=False, allow_null=True)
    bank_account = ReadablePKField(queryset=None, required=False, allow_null=True)
    lines = SupplierPaymentLineSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact
        from master.models import Currency
        from accounting.models import BankAccount

        self.fields["supplier"].queryset = Contact.objects.all()
        self.fields["currency"].queryset = Currency.objects.all()
        self.fields["bank_account"].queryset = BankAccount.objects.all()

    class Meta:
        model = SupplierPayment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_line_uuid(self, line):
        if not line.get("id"):
            line["id"] = uuid.uuid4()
        return line

    def create(self, validated_data):
        lines_data = validated_data.pop("lines", [])
        obj = SupplierPayment.objects.create(**validated_data)

        for line in lines_data:
            line = self._ensure_line_uuid(line)
            SupplierPaymentLine.objects.create(supplier_payment=obj, **line)

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
                SupplierPaymentLine.objects.create(supplier_payment=instance, **line)

        return instance


class DebitNoteLineSerializer(BulkModelSerializer):
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
        model = DebitNoteLine
        fields = (
            "id",
            "debit_note",
            "product",
            "description",
            "qty",
            "rate",
            "tax_rate",
            "line_total",
            "created",
            "updated",
        )
        read_only_fields = ("debit_note", "created", "updated")


class DebitNoteSerializer(BulkModelSerializer):
    supplier = ReadablePKField(queryset=None)
    purchase_bill = ReadablePKField(queryset=PurchaseBill.objects.all(), required=False, allow_null=True)
    currency = ReadablePKField(queryset=None, required=False, allow_null=True)
    lines = DebitNoteLineSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact
        from master.models import Currency

        self.fields["supplier"].queryset = Contact.objects.all()
        self.fields["currency"].queryset = Currency.objects.all()

    class Meta:
        model = DebitNote
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_line_uuid(self, line):
        if not line.get("id"):
            line["id"] = uuid.uuid4()
        return line

    def create(self, validated_data):
        lines_data = validated_data.pop("lines", [])
        obj = DebitNote.objects.create(**validated_data)

        for line in lines_data:
            line = self._ensure_line_uuid(line)
            DebitNoteLine.objects.create(debit_note=obj, **line)

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
                DebitNoteLine.objects.create(debit_note=instance, **line)

        return instance
