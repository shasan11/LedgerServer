from core.utils.BaseModelViewSet import BaseModelViewSet
from .models import Currency, TaxClass, TaxRate, MasterData, Branch
from .serializers import (
    CurrencySerializer,
    TaxClassSerializer,
    TaxRateSerializer,
    MasterDataSerializer,
    BranchSerializer,
)
from .filters import (
    CurrencyFilter,
    TaxClassFilter,
    TaxRateFilter,
    MasterDataFilter,
    BranchFilter,
)


class CurrencyViewSet(BaseModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    filterset_class = CurrencyFilter
    search_fields = ["name", "code", "symbol"]


class TaxClassViewSet(BaseModelViewSet):
    queryset = TaxClass.objects.all()
    serializer_class = TaxClassSerializer
    filterset_class = TaxClassFilter
    search_fields = ["name", "code", "description"]


class TaxRateViewSet(BaseModelViewSet):
    queryset = TaxRate.objects.select_related("tax_class").all()
    serializer_class = TaxRateSerializer
    filterset_class = TaxRateFilter
    search_fields = ["name", "tax_class__name"]


class MasterDataViewSet(BaseModelViewSet):
    queryset = MasterData.objects.select_related("parent").all()
    serializer_class = MasterDataSerializer
    filterset_class = MasterDataFilter
    search_fields = ["key", "name", "value"]


class BranchViewSet(BaseModelViewSet):
    queryset = Branch.objects.select_related("currency").all()
    serializer_class = BranchSerializer
    filterset_class = BranchFilter
    search_fields = ["code", "name", "email", "phone", "address", "country", "city"]
