from rest_framework import serializers
from .models import Company, Storage, Supplier, Product, Supply, SupplyProduct


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['id']


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'
        read_only_fields = ['id', 'company']


class StorageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'
        read_only_fields = ['id']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['id', 'company']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'quantity', 'storage']


class SupplyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyProduct
        fields = ['product', 'quantity']


class SupplySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Supply
        fields = ['id', 'supplier', 'delivery_date', 'products']
        read_only_fields = ['id']

    def get_products(self, obj):
        supply_products = obj.supplyproduct_set.all()

        serializer = SupplyProductSerializer(supply_products, many=True)
        return serializer.data
