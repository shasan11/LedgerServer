import django_filters as filters
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


class ProductCategoryFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    parent = filters.UUIDFilter(field_name="parent_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = ProductCategory
        fields = ["branch", "parent", "name", "active"]


class UnitOfMeasurementFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    short_name = filters.CharFilter(field_name="short_name", lookup_expr="icontains")
    accept_fraction = filters.BooleanFilter(field_name="accept_fraction")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = UnitOfMeasurement
        fields = ["branch", "name", "short_name", "accept_fraction", "active"]


class VariantAttributeFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    key = filters.CharFilter(field_name="key", lookup_expr="icontains")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = VariantAttribute
        fields = ["branch", "name", "key", "active"]


class VariantAttributeOptionFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    attribute = filters.UUIDFilter(field_name="attribute_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    key = filters.CharFilter(field_name="key", lookup_expr="icontains")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = VariantAttributeOption
        fields = ["branch", "attribute", "name", "key", "active"]


class ProductFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    type = filters.CharFilter(field_name="type")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    category = filters.UUIDFilter(field_name="category_id")
    tax_class = filters.UUIDFilter(field_name="tax_class_id")
    primary_unit = filters.UUIDFilter(field_name="primary_unit_id")
    hs_code = filters.CharFilter(field_name="hs_code", lookup_expr="icontains")
    ecommerce_enabled = filters.BooleanFilter(field_name="ecommerce_enabled")
    pos_enabled = filters.BooleanFilter(field_name="pos_enabled")
    valuation_method = filters.CharFilter(field_name="valuation_method")
    track_inventory = filters.BooleanFilter(field_name="track_inventory")
    sales_account = filters.UUIDFilter(field_name="sales_account_id")
    purchase_account = filters.UUIDFilter(field_name="purchase_account_id")
    purchase_return_account = filters.UUIDFilter(field_name="purchase_return_account_id")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Product
        fields = [
            "branch",
            "type",
            "name",
            "code",
            "category",
            "tax_class",
            "primary_unit",
            "hs_code",
            "ecommerce_enabled",
            "pos_enabled",
            "valuation_method",
            "track_inventory",
            "sales_account",
            "purchase_account",
            "purchase_return_account",
            "active",
        ]


class ProductVariantFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    product = filters.UUIDFilter(field_name="product_id")
    sku = filters.CharFilter(field_name="sku", lookup_expr="icontains")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = ProductVariant
        fields = ["branch", "product", "sku", "name", "active"]


class ProductVariantOptionFilter(filters.FilterSet):
    product_variant = filters.UUIDFilter(field_name="product_variant_id")
    attribute = filters.UUIDFilter(field_name="attribute_id")
    option = filters.UUIDFilter(field_name="option_id")

    class Meta:
        model = ProductVariantOption
        fields = ["product_variant", "attribute", "option"]


class ProductPictureFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    product = filters.UUIDFilter(field_name="product_id")
    is_main = filters.BooleanFilter(field_name="is_main")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = ProductPicture
        fields = ["branch", "product", "is_main", "active"]


class WarehouseFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    is_default = filters.BooleanFilter(field_name="is_default")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Warehouse
        fields = ["branch", "code", "name", "is_default", "active"]


class WarehouseTransferFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    transfer_no = filters.CharFilter(field_name="transfer_no", lookup_expr="icontains")
    transfer_date = filters.DateFromToRangeFilter(field_name="transfer_date")
    from_warehouse = filters.UUIDFilter(field_name="from_warehouse_id")
    to_warehouse = filters.UUIDFilter(field_name="to_warehouse_id")
    status = filters.CharFilter(field_name="status")
    approved = filters.BooleanFilter(field_name="approved")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = WarehouseTransfer
        fields = [
            "branch",
            "transfer_no",
            "transfer_date",
            "from_warehouse",
            "to_warehouse",
            "status",
            "approved",
            "active",
        ]


class WarehouseTransferItemFilter(filters.FilterSet):
    warehouse_transfer = filters.UUIDFilter(field_name="warehouse_transfer_id")
    product_variant = filters.UUIDFilter(field_name="product_variant_id")

    class Meta:
        model = WarehouseTransferItem
        fields = ["warehouse_transfer", "product_variant"]


class InventoryAdjustmentFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    adjustment_no = filters.CharFilter(field_name="adjustment_no", lookup_expr="icontains")
    adjustment_date = filters.DateFromToRangeFilter(field_name="adjustment_date")
    warehouse = filters.UUIDFilter(field_name="warehouse_id")
    status = filters.CharFilter(field_name="status")
    approved = filters.BooleanFilter(field_name="approved")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = InventoryAdjustment
        fields = [
            "branch",
            "adjustment_no",
            "adjustment_date",
            "warehouse",
            "status",
            "approved",
            "active",
        ]


class InventoryAdjustmentItemFilter(filters.FilterSet):
    inventory_adjustment = filters.UUIDFilter(field_name="inventory_adjustment_id")
    product_variant = filters.UUIDFilter(field_name="product_variant_id")

    class Meta:
        model = InventoryAdjustmentItem
        fields = ["inventory_adjustment", "product_variant"]


class ProductionOrderFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    production_no = filters.CharFilter(field_name="production_no", lookup_expr="icontains")
    production_date = filters.DateFromToRangeFilter(field_name="production_date")
    warehouse = filters.UUIDFilter(field_name="warehouse_id")
    status = filters.CharFilter(field_name="status")
    finished_good_variant = filters.UUIDFilter(field_name="finished_good_variant_id")
    approved = filters.BooleanFilter(field_name="approved")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = ProductionOrder
        fields = [
            "branch",
            "production_no",
            "production_date",
            "warehouse",
            "status",
            "finished_good_variant",
            "approved",
            "active",
        ]


class ProductionInputFilter(filters.FilterSet):
    production_order = filters.UUIDFilter(field_name="production_order_id")
    raw_material_variant = filters.UUIDFilter(field_name="raw_material_variant_id")

    class Meta:
        model = ProductionInput
        fields = ["production_order", "raw_material_variant"]


class ProductionOutputFilter(filters.FilterSet):
    production_order = filters.UUIDFilter(field_name="production_order_id")
    finished_good_variant = filters.UUIDFilter(field_name="finished_good_variant_id")

    class Meta:
        model = ProductionOutput
        fields = ["production_order", "finished_good_variant"]
