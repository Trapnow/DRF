from rest_framework import serializers
from .models import Company, Storage, Supplier


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['id']


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['address']
        read_only_fields = ['id']


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
