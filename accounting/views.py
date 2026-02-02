from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.utils.BaseModelViewSet import BaseModelViewSet
from .models import (
    AccountType,
    COA,
    AccountBalance,
    BankAccount,
    CashTransfer,
    ChequeRegister,
    JournalVoucher,
)
from .serializers import (
    AccountTypeSerializer,
    COASerializer,
    AccountBalanceSerializer,
    BankAccountSerializer,
    CashTransferSerializer,
    ChequeRegisterSerializer,
    JournalVoucherSerializer,
)
from .filters import (
    AccountTypeFilter,
    COAFilter,
    AccountBalanceFilter,
    BankAccountFilter,
    CashTransferFilter,
    ChequeRegisterFilter,
    JournalVoucherFilter,
)


class AccountTypeViewSet(BaseModelViewSet):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    filterset_class = AccountTypeFilter
    search_fields = ["name", "category", "normal_balance"]


class COAViewSet(BaseModelViewSet):
    queryset = COA.objects.select_related("parent", "account_type", "branch").all()
    serializer_class = COASerializer
    filterset_class = COAFilter
    search_fields = ["name", "code", "description"]


class AccountBalanceViewSet(BaseModelViewSet):
    queryset = AccountBalance.objects.select_related("account", "branch").all()
    serializer_class = AccountBalanceSerializer
    filterset_class = AccountBalanceFilter
    search_fields = ["account__name", "account__code"]


class BankAccountViewSet(BaseModelViewSet):
    queryset = BankAccount.objects.select_related("currency", "coa_account", "branch").all()
    serializer_class = BankAccountSerializer
    filterset_class = BankAccountFilter
    search_fields = ["display_name", "code", "bank_name", "account_number"]


class CashTransferViewSet(BaseModelViewSet):
    queryset = CashTransfer.objects.select_related("from_account", "branch").prefetch_related("items").all()
    serializer_class = CashTransferSerializer
    filterset_class = CashTransferFilter
    search_fields = ["transfer_no", "reference_no", "note"]


class ChequeRegisterViewSet(BaseModelViewSet):
    queryset = ChequeRegister.objects.select_related("coa_account", "bank_account", "branch", "contact").all()
    serializer_class = ChequeRegisterSerializer
    filterset_class = ChequeRegisterFilter
    search_fields = ["cheque_no", "memo", "note"]


class JournalVoucherViewSet(BaseModelViewSet):
    queryset = JournalVoucher.objects.select_related("branch").prefetch_related("items").all()
    serializer_class = JournalVoucherSerializer
    filterset_class = JournalVoucherFilter
    search_fields = ["voucher_no", "narration", "note"]
