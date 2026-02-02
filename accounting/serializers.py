import uuid
from rest_framework import serializers
from .models import (
    AccountType,
    COA,
    AccountBalance,
    BankAccount,
    CashTransfer,
    CashTransferItem,
    ChequeRegister,
    JournalVoucher,
    JournalVoucherItem,
)


from core.utils.AdaptedBulkListSerializer import BulkModelSerializer


class ReadablePKField(serializers.PrimaryKeyRelatedField):
    """
    Shows readable string in response while still being PK-based.
    """

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


# -------------------------
# Masters
# -------------------------
class AccountTypeSerializer(BulkModelSerializer):
    class Meta:
        model = AccountType
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class COASerializer(BulkModelSerializer):
    parent = ReadablePKField(queryset=COA.objects.all(), required=False, allow_null=True)
    account_type = ReadablePKField(queryset=AccountType.objects.all())

    class Meta:
        model = COA
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class AccountBalanceSerializer(BulkModelSerializer):
    account = ReadablePKField(queryset=COA.objects.all())

    class Meta:
        model = AccountBalance
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class BankAccountSerializer(BulkModelSerializer):
    currency = ReadablePKField(queryset=None, required=False, allow_null=True)  # set in __init__
    coa_account = ReadablePKField(queryset=COA.objects.all(), required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # avoid circular imports; Currency is in master app
        from master.models import Currency
        self.fields["currency"].queryset = Currency.objects.all()

    class Meta:
        model = BankAccount
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


# -------------------------
# Transactions - Cash Transfer
# -------------------------
class CashTransferItemSerializer(BulkModelSerializer):
    id = serializers.UUIDField(required=False)

    to_account = ReadablePKField(queryset=BankAccount.objects.all())

    class Meta:
        model = CashTransferItem
        fields = ("id", "cash_transfer", "to_account", "amount", "note", "created", "updated")
        read_only_fields = ("cash_transfer", "created", "updated")

    def validate(self, attrs):
        # basic sanity
        amount = attrs.get("amount")
        if amount is not None and amount < 0:
            raise serializers.ValidationError({"amount": "Amount cannot be negative."})
        return attrs


class CashTransferSerializer(BulkModelSerializer):
    from_account = ReadablePKField(queryset=BankAccount.objects.all())
    items = CashTransferItemSerializer(many=True, required=False)

    class Meta:
        model = CashTransfer
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_item_uuid(self, item):
        # Your model has id UUIDField(primary_key=True, editable=False) with no default.
        # So we generate here if missing.
        if not item.get("id"):
            item["id"] = uuid.uuid4()
        return item

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        obj = CashTransfer.objects.create(**validated_data)

        total = 0
        for item in items_data:
            item = self._ensure_item_uuid(item)
            CashTransferItem.objects.create(cash_transfer=obj, **item)
            total += item.get("amount") or 0

        # set total (optional but useful)
        obj.total = total
        obj.save(update_fields=["total"])
        return obj

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        if items_data is not None:
            # Replace strategy (simple & reliable):
            instance.items.all().delete()

            total = 0
            for item in items_data:
                item = self._ensure_item_uuid(item)
                CashTransferItem.objects.create(cash_transfer=instance, **item)
                total += item.get("amount") or 0

            instance.total = total
            instance.save(update_fields=["total"])

        return instance


# -------------------------
# Transactions - Cheque Register
# -------------------------
class ChequeRegisterSerializer(BulkModelSerializer):
    coa_account = ReadablePKField(queryset=COA.objects.all(), required=False, allow_null=True)
    bank_account = ReadablePKField(queryset=BankAccount.objects.all(), required=False, allow_null=True)

    contact = ReadablePKField(queryset=None, required=False, allow_null=True)  # crm.Contact

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from crm.models import Contact
        self.fields["contact"].queryset = Contact.objects.all()

    class Meta:
        model = ChequeRegister
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


# -------------------------
# Transactions - Journal Voucher
# -------------------------
class JournalVoucherItemSerializer(BulkModelSerializer):
    id = serializers.UUIDField(required=False)
    account = ReadablePKField(queryset=COA.objects.all())

    class Meta:
        model = JournalVoucherItem
        fields = ("id", "journal_voucher", "account", "dr_amount", "cr_amount", "line_note", "created", "updated")
        read_only_fields = ("journal_voucher", "created", "updated")

    def validate(self, attrs):
        dr = attrs.get("dr_amount") or 0
        cr = attrs.get("cr_amount") or 0
        if dr < 0 or cr < 0:
            raise serializers.ValidationError("Amounts cannot be negative.")
        if dr > 0 and cr > 0:
            raise serializers.ValidationError("A line cannot have both DR and CR amounts.")
        if dr == 0 and cr == 0:
            raise serializers.ValidationError("A line must have either DR or CR amount.")
        return attrs


class JournalVoucherSerializer(BulkModelSerializer):
    items = JournalVoucherItemSerializer(many=True, required=False)

    class Meta:
        model = JournalVoucher
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_item_uuid(self, item):
        if not item.get("id"):
            item["id"] = uuid.uuid4()
        return item

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        obj = JournalVoucher.objects.create(**validated_data)

        total = 0
        for item in items_data:
            item = self._ensure_item_uuid(item)
            JournalVoucherItem.objects.create(journal_voucher=obj, **item)
            total += (item.get("dr_amount") or 0) + (item.get("cr_amount") or 0)

        obj.total = total
        obj.save(update_fields=["total"])
        return obj

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()

            total = 0
            for item in items_data:
                item = self._ensure_item_uuid(item)
                JournalVoucherItem.objects.create(journal_voucher=instance, **item)
                total += (item.get("dr_amount") or 0) + (item.get("cr_amount") or 0)

            instance.total = total
            instance.save(update_fields=["total"])

        return instance
