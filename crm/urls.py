from django.urls import path, include
from rest_framework_bulk.routes import BulkRouter
from .views import (
    ContactGroupViewSet,
    ContactViewSet,
    DealViewSet,
    DealItemViewSet,
    ActivityViewSet,
)

router = BulkRouter()
router.register(r"contact-groups", ContactGroupViewSet, basename="contact-group")
router.register(r"contacts", ContactViewSet, basename="contact")
router.register(r"deals", DealViewSet, basename="deal")
router.register(r"deal-items", DealItemViewSet, basename="deal-item")
router.register(r"activities", ActivityViewSet, basename="activity")

urlpatterns = [
    path("", include(router.urls)),
]
