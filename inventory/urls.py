from django.urls import path, include
from rest_framework_bulk.routes import BulkRouter
from .views import (
    ProductCategoryViewSet,
    UnitOfMeasurementViewSet,
    VariantAttributeViewSet,
    VariantAttributeOptionViewSet,
    ProductViewSet,
    ProductVariantViewSet,
    ProductVariantOptionViewSet,
    ProductPictureViewSet,
    WarehouseViewSet,
    WarehouseTransferViewSet,
    WarehouseTransferItemViewSet,
    InventoryAdjustmentViewSet,
    InventoryAdjustmentItemViewSet,
    ProductionOrderViewSet,
    ProductionInputViewSet,
    ProductionOutputViewSet,
)

router = BulkRouter()
router.register(r"product-categories", ProductCategoryViewSet, basename="product-category")
router.register(r"units", UnitOfMeasurementViewSet, basename="unit-of-measurement")
router.register(r"variant-attributes", VariantAttributeViewSet, basename="variant-attribute")
router.register(r"variant-attribute-options", VariantAttributeOptionViewSet, basename="variant-attribute-option")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"product-variants", ProductVariantViewSet, basename="product-variant")
router.register(r"product-variant-options", ProductVariantOptionViewSet, basename="product-variant-option")
router.register(r"product-pictures", ProductPictureViewSet, basename="product-picture")
router.register(r"warehouses", WarehouseViewSet, basename="warehouse")
router.register(r"warehouse-transfers", WarehouseTransferViewSet, basename="warehouse-transfer")
router.register(r"warehouse-transfer-items", WarehouseTransferItemViewSet, basename="warehouse-transfer-item")
router.register(r"inventory-adjustments", InventoryAdjustmentViewSet, basename="inventory-adjustment")
router.register(r"inventory-adjustment-items", InventoryAdjustmentItemViewSet, basename="inventory-adjustment-item")
router.register(r"production-orders", ProductionOrderViewSet, basename="production-order")
router.register(r"production-inputs", ProductionInputViewSet, basename="production-input")
router.register(r"production-outputs", ProductionOutputViewSet, basename="production-output")

urlpatterns = [
    path("", include(router.urls)),
]
