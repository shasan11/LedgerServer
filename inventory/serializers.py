from rest_framework import serializers
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


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class UnitOfMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasurement
        fields = "__all__"


class VariantAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantAttribute
        fields = "__all__"


class VariantAttributeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantAttributeOption
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = "__all__"


class ProductVariantOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantOption
        fields = "__all__"


class ProductPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPicture
        fields = "__all__"


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = "__all__"


class WarehouseTransferItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseTransferItem
        fields = "__all__"


class WarehouseTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseTransfer
        fields = "__all__"


class InventoryAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryAdjustment
        fields = "__all__"


class InventoryAdjustmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryAdjustmentItem
        fields = "__all__"


class ProductionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrder
        fields = "__all__"


class ProductionInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionInput
        fields = "__all__"


class ProductionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOutput
        fields = "__all__"
