import django_filters as filters
from .models import Currency, TaxClass, TaxRate, MasterData, Branch


class CurrencyFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    is_base = filters.BooleanFilter(field_name="is_base")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Currency
        fields = ["name", "code", "is_base", "active"]


class TaxClassFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = TaxClass
        fields = ["name", "code", "active"]


class TaxRateFilter(filters.FilterSet):
    tax_class = filters.UUIDFilter(field_name="tax_class_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    inclusive = filters.BooleanFilter(field_name="inclusive")
    active_from = filters.DateFromToRangeFilter(field_name="active_from")
    active_to = filters.DateFromToRangeFilter(field_name="active_to")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = TaxRate
        fields = ["tax_class", "name", "inclusive", "active_from", "active_to", "active"]


class MasterDataFilter(filters.FilterSet):
    key = filters.CharFilter(field_name="key", lookup_expr="icontains")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    is_boolean = filters.BooleanFilter(field_name="is_boolean")
    parent = filters.UUIDFilter(field_name="parent_id")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = MasterData
        fields = ["key", "name", "is_boolean", "parent", "active"]


class BranchFilter(filters.FilterSet):
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    email = filters.CharFilter(field_name="email", lookup_expr="icontains")
    phone = filters.CharFilter(field_name="phone", lookup_expr="icontains")
    country = filters.CharFilter(field_name="country", lookup_expr="icontains")
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")
    timezone = filters.CharFilter(field_name="timezone", lookup_expr="icontains")
    currency = filters.UUIDFilter(field_name="currency_id")
    is_head_office = filters.BooleanFilter(field_name="is_head_office")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Branch
        fields = [
            "code",
            "name",
            "email",
            "phone",
            "country",
            "city",
            "timezone",
            "currency",
            "is_head_office",
            "active",
        ]
