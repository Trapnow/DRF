from rest_framework import serializers
from .models import Company, Storage, Supplier, Product, Supply, SupplyProduct, Sale, ProductSale


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


class ProductSaleSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = ProductSale
        fields = ['product_id', 'quantity']


class SaleSerializer(serializers.ModelSerializer):
    product_sales = ProductSaleSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'buyer_name', 'sale_date', 'product_sales']
        read_only_fields = ['id']

    def create(self, validated_data):
        product_sales_data = validated_data.pop('product_sales')
        sale = Sale.objects.create(
            buyer_name=validated_data['buyer_name'],
            company=self.context['request'].user.company,
            sale_date=validated_data['sale_date']
        )

        for product_sale_data in product_sales_data:
            try:
                product_id = product_sale_data['product_id']
                quantity = product_sale_data['quantity']

                product = Product.objects.get(id=product_id)

                if product.quantity < quantity:
                    raise serializers.ValidationError({
                        'detail': f"Недостаточно товара {product.name}. "
                                  f"Доступно: {product.quantity}, "
                                  f"Запрошено: {quantity}"
                    })

                ProductSale.objects.create(
                    sale=sale,
                    product_id=product_id,
                    quantity=quantity
                )

                product.quantity -= quantity
                product.save()

            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Товар с ID {product_id} не найден"
                )

        return sale

class SaleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['buyer_name', 'sale_date']
        read_only_fields = ['id']