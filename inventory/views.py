from core.utils.BaseModelViewSet import BaseModelViewSet
from .models import (
    ProductCategory,
    UnitOfMeasurement,
    VariantAttribute,
    VariantAttributeOption,
    Product,
    ProductVariant,
    ProductVariantOption,
    ProductPicture,
    Warehouse,
    WarehouseTransfer,
    WarehouseTransferItem,
    InventoryAdjustment,
    InventoryAdjustmentItem,
    ProductionOrder,
    ProductionInput,
    ProductionOutput,
)
from .serializers import (
    ProductCategorySerializer,
    UnitOfMeasurementSerializer,
    VariantAttributeSerializer,
    VariantAttributeOptionSerializer,
    ProductSerializer,
    ProductVariantSerializer,
    ProductVariantOptionSerializer,
    ProductPictureSerializer,
    WarehouseSerializer,
    WarehouseTransferSerializer,
    WarehouseTransferItemSerializer,
    InventoryAdjustmentSerializer,
    InventoryAdjustmentItemSerializer,
    ProductionOrderSerializer,
    ProductionInputSerializer,
    ProductionOutputSerializer,
)
from .filters import (
    ProductCategoryFilter,
    UnitOfMeasurementFilter,
    VariantAttributeFilter,
    VariantAttributeOptionFilter,
    ProductFilter,
    ProductVariantFilter,
    ProductVariantOptionFilter,
    ProductPictureFilter,
    WarehouseFilter,
    WarehouseTransferFilter,
    WarehouseTransferItemFilter,
    InventoryAdjustmentFilter,
    InventoryAdjustmentItemFilter,
    ProductionOrderFilter,
    ProductionInputFilter,
    ProductionOutputFilter,
)


class ProductCategoryViewSet(BaseModelViewSet):
    queryset = ProductCategory.objects.select_related("parent", "branch").all()
    serializer_class = ProductCategorySerializer
    filterset_class = ProductCategoryFilter
    search_fields = ["name", "description"]


class UnitOfMeasurementViewSet(BaseModelViewSet):
    queryset = UnitOfMeasurement.objects.select_related("branch").all()
    serializer_class = UnitOfMeasurementSerializer
    filterset_class = UnitOfMeasurementFilter
    search_fields = ["name", "short_name", "description"]


class VariantAttributeViewSet(BaseModelViewSet):
    queryset = VariantAttribute.objects.select_related("branch").all()
    serializer_class = VariantAttributeSerializer
    filterset_class = VariantAttributeFilter
    search_fields = ["name", "key", "description"]


class VariantAttributeOptionViewSet(BaseModelViewSet):
    queryset = VariantAttributeOption.objects.select_related("attribute", "branch").all()
    serializer_class = VariantAttributeOptionSerializer
    filterset_class = VariantAttributeOptionFilter
    search_fields = ["name", "key", "description", "attribute__name"]


class ProductViewSet(BaseModelViewSet):
    queryset = Product.objects.select_related(
        "category",
        "tax_class",
        "primary_unit",
        "sales_account",
        "purchase_account",
        "purchase_return_account",
        "branch",
    ).all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ["name", "code", "description", "hs_code"]


class ProductVariantViewSet(BaseModelViewSet):
    queryset = ProductVariant.objects.select_related("product", "branch").all()
    serializer_class = ProductVariantSerializer
    filterset_class = ProductVariantFilter
    search_fields = ["sku", "name", "option_summary", "product__name"]


class ProductVariantOptionViewSet(BaseModelViewSet):
    queryset = ProductVariantOption.objects.select_related("product_variant", "attribute", "option").all()
    serializer_class = ProductVariantOptionSerializer
    filterset_class = ProductVariantOptionFilter
    search_fields = [
        "product_variant__sku",
        "product_variant__name",
        "attribute__name",
        "option__name",
    ]


class ProductPictureViewSet(BaseModelViewSet):
    queryset = ProductPicture.objects.select_related("product", "branch").all()
    serializer_class = ProductPictureSerializer
    filterset_class = ProductPictureFilter
    search_fields = ["description", "image", "product__name"]


class WarehouseViewSet(BaseModelViewSet):
    queryset = Warehouse.objects.select_related("branch").all()
    serializer_class = WarehouseSerializer
    filterset_class = WarehouseFilter
    search_fields = ["name", "code", "address", "contact_phone"]


class WarehouseTransferViewSet(BaseModelViewSet):
    queryset = WarehouseTransfer.objects.select_related(
        "from_warehouse",
        "to_warehouse",
        "branch",
    ).prefetch_related("items").all()
    serializer_class = WarehouseTransferSerializer
    filterset_class = WarehouseTransferFilter
    search_fields = ["transfer_no", "note"]


class WarehouseTransferItemViewSet(BaseModelViewSet):
    queryset = WarehouseTransferItem.objects.select_related("warehouse_transfer", "product_variant").all()
    serializer_class = WarehouseTransferItemSerializer
    filterset_class = WarehouseTransferItemFilter
    search_fields = ["note", "product_variant__sku", "product_variant__name"]


class InventoryAdjustmentViewSet(BaseModelViewSet):
    queryset = InventoryAdjustment.objects.select_related("warehouse", "branch").prefetch_related("items").all()
    serializer_class = InventoryAdjustmentSerializer
    filterset_class = InventoryAdjustmentFilter
    search_fields = ["adjustment_no", "reason", "note"]


class InventoryAdjustmentItemViewSet(BaseModelViewSet):
    queryset = InventoryAdjustmentItem.objects.select_related("inventory_adjustment", "product_variant").all()
    serializer_class = InventoryAdjustmentItemSerializer
    filterset_class = InventoryAdjustmentItemFilter
    search_fields = ["note", "product_variant__sku", "product_variant__name"]


class ProductionOrderViewSet(BaseModelViewSet):
    queryset = ProductionOrder.objects.select_related(
        "warehouse",
        "finished_good_variant",
        "branch",
    ).prefetch_related("inputs", "outputs").all()
    serializer_class = ProductionOrderSerializer
    filterset_class = ProductionOrderFilter
    search_fields = ["production_no", "note", "finished_good_variant__sku", "finished_good_variant__name"]


class ProductionInputViewSet(BaseModelViewSet):
    queryset = ProductionInput.objects.select_related("production_order", "raw_material_variant").all()
    serializer_class = ProductionInputSerializer
    filterset_class = ProductionInputFilter
    search_fields = ["raw_material_variant__sku", "raw_material_variant__name"]


class ProductionOutputViewSet(BaseModelViewSet):
    queryset = ProductionOutput.objects.select_related("production_order", "finished_good_variant").all()
    serializer_class = ProductionOutputSerializer
    filterset_class = ProductionOutputFilter
    search_fields = ["finished_good_variant__sku", "finished_good_variant__name"]
