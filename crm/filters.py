import django_filters as filters
from .models import ContactGroup, Contact, Deal, DealItem, Activity


class ContactGroupFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    parent = filters.UUIDFilter(field_name="parent_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = ContactGroup
        fields = ["branch", "parent", "name", "active"]


class ContactFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    type = filters.CharFilter(field_name="type")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    group = filters.UUIDFilter(field_name="group_id")
    phone = filters.CharFilter(field_name="phone", lookup_expr="icontains")
    email = filters.CharFilter(field_name="email", lookup_expr="icontains")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Contact
        fields = ["branch", "type", "name", "code", "group", "phone", "email", "active"]


class DealFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    contact = filters.UUIDFilter(field_name="contact_id")
    stage = filters.CharFilter(field_name="stage")
    expected_close = filters.DateFromToRangeFilter(field_name="expected_close")
    owner = filters.UUIDFilter(field_name="owner_id")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Deal
        fields = ["branch", "code", "title", "contact", "stage", "expected_close", "owner", "active"]


class DealItemFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    deal = filters.UUIDFilter(field_name="deal_id")
    product = filters.UUIDFilter(field_name="product_id")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = DealItem
        fields = ["branch", "deal", "product", "active"]


class ActivityFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    type = filters.CharFilter(field_name="type")
    subject = filters.CharFilter(field_name="subject", lookup_expr="icontains")
    contact = filters.UUIDFilter(field_name="contact_id")
    deal = filters.UUIDFilter(field_name="deal_id")
    due_at = filters.DateFromToRangeFilter(field_name="due_at")
    status = filters.CharFilter(field_name="status")
    assigned_to = filters.UUIDFilter(field_name="assigned_to_id")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Activity
        fields = ["branch", "type", "subject", "contact", "deal", "due_at", "status", "assigned_to", "active"]
