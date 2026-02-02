from django.urls import path, include
from rest_framework_bulk.routes import BulkRouter
from .views import (
    CurrencyViewSet,
    TaxClassViewSet,
    TaxRateViewSet,
    MasterDataViewSet,
    BranchViewSet,
)

router = BulkRouter()
router.register(r"currencies", CurrencyViewSet, basename="currency")
router.register(r"tax-classes", TaxClassViewSet, basename="tax-class")
router.register(r"tax-rates", TaxRateViewSet, basename="tax-rate")
router.register(r"master-data", MasterDataViewSet, basename="master-data")
router.register(r"branches", BranchViewSet, basename="branch")

urlpatterns = [
    path("", include(router.urls)),
]
