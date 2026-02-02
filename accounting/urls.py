from django.urls import path, include
from rest_framework_bulk.routes import BulkRouter
from .views import (
    AccountTypeViewSet,
    COAViewSet,
    AccountBalanceViewSet,
    BankAccountViewSet,
    CashTransferViewSet,
    ChequeRegisterViewSet,
    JournalVoucherViewSet,
)

router = BulkRouter()
router.register(r"account-types", AccountTypeViewSet, basename="account-type")
router.register(r"coa", COAViewSet, basename="coa")
router.register(r"account-balances", AccountBalanceViewSet, basename="account-balance")
router.register(r"bank-accounts", BankAccountViewSet, basename="bank-account")
router.register(r"cash-transfers", CashTransferViewSet, basename="cash-transfer")
router.register(r"cheque-registers", ChequeRegisterViewSet, basename="cheque-register")
router.register(r"journal-vouchers", JournalVoucherViewSet, basename="journal-voucher")

urlpatterns = [
    path("", include(router.urls)),
]
