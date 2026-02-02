from core.utils.BaseModelViewSet import BaseModelViewSet
from .models import ContactGroup, Contact, Deal, DealItem, Activity
from .serializers import (
    ContactGroupSerializer,
    ContactSerializer,
    DealSerializer,
    DealItemSerializer,
    ActivitySerializer,
)
from .filters import (
    ContactGroupFilter,
    ContactFilter,
    DealFilter,
    DealItemFilter,
    ActivityFilter,
)


class ContactGroupViewSet(BaseModelViewSet):
    queryset = ContactGroup.objects.select_related("parent", "branch").all()
    serializer_class = ContactGroupSerializer
    filterset_class = ContactGroupFilter
    search_fields = ["name", "description"]


class ContactViewSet(BaseModelViewSet):
    queryset = Contact.objects.select_related("group", "receivable_account", "payable_account", "branch").all()
    serializer_class = ContactSerializer
    filterset_class = ContactFilter
    search_fields = ["name", "code", "phone", "email"]


class DealViewSet(BaseModelViewSet):
    queryset = Deal.objects.select_related("contact", "currency", "owner", "branch").prefetch_related("items").all()
    serializer_class = DealSerializer
    filterset_class = DealFilter
    search_fields = ["title", "code", "description", "source"]


class DealItemViewSet(BaseModelViewSet):
    queryset = DealItem.objects.select_related("deal", "product", "tax_rate", "branch").all()
    serializer_class = DealItemSerializer
    filterset_class = DealItemFilter
    search_fields = ["description"]


class ActivityViewSet(BaseModelViewSet):
    queryset = Activity.objects.select_related("contact", "deal", "assigned_to", "branch").all()
    serializer_class = ActivitySerializer
    filterset_class = ActivityFilter
    search_fields = ["subject", "description"]
