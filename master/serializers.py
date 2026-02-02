from rest_framework import serializers
from .models import Currency, TaxClass, TaxRate, MasterData, Branch


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class TaxClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxClass
        fields = "__all__"


class TaxRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxRate
        fields = "__all__"


class MasterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterData
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
