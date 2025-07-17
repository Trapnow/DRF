from itertools import product

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company, Storage, Supplier, Product, Supply, SupplyProduct, Sale, ProductSale
from .serializer import CompanySerializer, StorageSerializer, StorageDetailSerializer, SupplierSerializer, \
    ProductSerializer, SupplySerializer, SaleSerializer, SaleUpdateSerializer
from .permissions import IsCompanyOwnerOrReadOnly, IsRelatedToCompany


class CompanyRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['company'],
        description="Получение компании по ID. Доступно всем авторизованным пользователям.",
        request=CompanySerializer
    )
    def get(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        except Company.DoesNotExist:
            return Response({"detail": "Компания не найдена"}, status=status.HTTP_404_NOT_FOUND)


class CompanyCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrReadOnly]

    @extend_schema(
        tags=['company'],
        description="Создание компании. Доступно только авторизированным пользователям.",
        request=CompanySerializer
    )
    def post(self, request):
        if request.user.company is not None:
            return Response({"detail": "У Вас уже есть компания"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            company = serializer.save()

            request.user.is_company_owner = True
            request.user.company = company
            request.user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrReadOnly]

    @extend_schema(
        tags=['company'],
        description="Удаление компании. Доступно только владельцу компании.",
        request=CompanySerializer
    )
    def delete(self, request):
        company = request.user.company

        if not request.user.is_company_owner:
            return Response({
                "detail": "Вы не являетесь владельцем этой компании"
            }, status=status.HTTP_403_FORBIDDEN)

        company.delete()

        request.user.is_company_owner = False
        request.user.company = None
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrReadOnly]

    @extend_schema(
        tags=['company'],
        description="Редактирование компании. Доступно только владельцу компании.",
        request=CompanySerializer
    )
    def put(self, request):
        company = request.user.company

        if not request.user.is_company_owner:
            return Response({
                "detail": "У вас нет прав на изменение компании"
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = CompanySerializer(
            company,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


########################STORAGE########################################


class StorageRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['storage'],
        description="Получение склада по ID. Доступно пользователям, связанным с компанией склада.",
        request=StorageDetailSerializer
    )
    def get(self, request, pk):
        try:
            storage = Storage.objects.get(pk=pk)

            if not (request.user.company == storage.company):
                return Response({
                    "detail": "У вас нет доступа к этому складу"
                }, status=status.HTTP_403_FORBIDDEN)

            serializer = StorageDetailSerializer(storage)
            return Response(serializer.data)
        except Storage.DoesNotExist:
            return Response({"detail": "Склад не найден"}, status=status.HTTP_404_NOT_FOUND)


class StorageCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrReadOnly]

    @extend_schema(
        tags=['storage'],
        description="Создание склада. Доступно только владельцу компании.",
        request=StorageSerializer
    )
    def post(self, request):
        if not request.user.is_company_owner:
            return Response({
                "detail": "Только владелец компании может создавать склады"
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = StorageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StorageUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrReadOnly]

    @extend_schema(
        tags=['storage'],
        description="Обновление склада. Доступно только владельцу компании.",
        request=StorageSerializer
    )
    def put(self, request, pk):
        try:
            storage = Storage.objects.get(pk=pk)

            if not (request.user.is_company_owner and request.user.company == storage.company):
                return Response({
                    "detail": "Только владелец компании может изменять склад"
                }, status=status.HTTP_403_FORBIDDEN)

            serializer = StorageSerializer(
                storage,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Storage.DoesNotExist:
            return Response({"detail": "Склад не найден"}, status=status.HTTP_404_NOT_FOUND)


class StorageDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrReadOnly]

    @extend_schema(
        tags=['storage'],
        description="Удаление склада. Доступно только владельцу компании.",
        request=StorageSerializer
    )
    def delete(self, request, pk):
        try:
            storage = Storage.objects.get(pk=pk)

            if not (request.user.is_company_owner and request.user.company == storage.company):
                return Response({
                    "detail": "Только владелец компании может удалять склад"
                }, status=status.HTTP_403_FORBIDDEN)

            storage.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Storage.DoesNotExist:
            return Response({"detail": "Склад не найден"}, status=status.HTTP_404_NOT_FOUND)


########################SUPPLIER########################################


class SupplierListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['supplier'],
        description="Получение списка поставщиков компании"
    )
    def get(self, request):
        suppliers = Supplier.objects.filter(company=request.user.company)
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)


class SupplierCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['supplier'],
        description="Создание нового поставщика",
        request=SupplierSerializer
    )
    def post(self, request):
        request_data = request.data.copy()
        request_data['company'] = request.user.company.id

        serializer = SupplierSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save(company=request.user.company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['supplier'],
        description="Обновление информации о поставщике",
        request=SupplierSerializer
    )
    def put(self, request, pk):
        try:
            supplier = Supplier.objects.get(pk=pk, company=request.user.company)

            serializer = SupplierSerializer(
                supplier,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Supplier.DoesNotExist:
            return Response({"detail": "Поставщик не найден"}, status=status.HTTP_404_NOT_FOUND)


class SupplierDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['supplier'],
        description="Удаление поставщика",
        request=SupplierSerializer
    )
    def delete(self, request, pk):
        try:
            supplier = Supplier.objects.get(pk=pk)
            supplier.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Supplier.DoesNotExist:
            return Response(
                {"detail": "Поставщик с указанным ID не найден"},
                status=status.HTTP_404_NOT_FOUND
            )


########################PRODUCT########################################


class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['product'],
        description="Создание нового товара",
        request=ProductSerializer
    )
    def post(self, request):
        try:
            user_company = request.user.company
            storage = Storage.objects.get(company=user_company)

            request_data = request.data.copy()
            request_data['storage'] = storage.id

            serializer = ProductSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save(storage=storage)
                print(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Storage.DoesNotExist:
            return Response(
                {"detail": "У вашей компании ещё нет склада, чтобы добавить продукт"},
                status=status.HTTP_404_NOT_FOUND
            )


class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['product'],
        description="Получение списка продуктов компании"
    )
    def get(self, request):
        user_company = request.user.company
        storage = Storage.objects.get(company=user_company)

        products = Product.objects.filter(storage=storage)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['product'],
        description="Обновление информации о продукте",
        request=ProductSerializer
    )
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)

            serializer = ProductSerializer(
                product,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"detail": "Продукт не найден"}, status=status.HTTP_404_NOT_FOUND)


class ProductDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['product'],
        description="Удаление продукта",
        request=ProductSerializer
    )
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Продукт с указанным ID не найден"},
                status=status.HTTP_404_NOT_FOUND
            )


#################################SUPLY####################################


class SupplyCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['supply'],
        description="Создание новой поставки товаров",
        request=SupplySerializer
    )
    def post(self, request):
        serializer = SupplySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        supplier = validated_data['supplier']
        delivery_date = validated_data['delivery_date']
        products_data = request.data.get('products', [])

        if not products_data:
            return Response(
                {"detail": "Список продуктов не может быть пустым"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if supplier.company != request.user.company:
            return Response(
                {"detail": "Поставщик принадлежит другой компании"},
                status=status.HTTP_403_FORBIDDEN
            )

        supply = Supply.objects.create(
            supplier=supplier,
            delivery_date=delivery_date
        )

        for product_data in products_data:
            product_id = product_data.get('product')
            quantity = product_data.get('quantity')

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"detail": f"Товар с ID {product_id} не найден"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if product.storage.company != request.user.company:
                return Response(
                    {"detail": "В списке есть товары, которые принадлежат другой компании"},
                    status=status.HTTP_403_FORBIDDEN
                )

            SupplyProduct.objects.create(
                supply=supply,
                product=product,
                quantity=quantity
            )

            product.quantity += quantity
            product.save()

        supply = Supply.objects.prefetch_related('supplyproduct_set').get(id=supply.id)
        serializer = SupplySerializer(supply)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SupplyListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['supply'],
        description="Получение списка поставок компании"
    )
    def get(self, request):
        supplies = Supply.objects.filter(supplier__company=request.user.company).order_by('delivery_date')

        serializer = SupplySerializer(supplies, many=True)
        return Response(serializer.data)


class SaleCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['sales'],
        description="Создание новой продажи",
        request=SaleSerializer
    )
    def post(self, request):
        serializer = SaleSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not serializer.validated_data.get('product_sales'):
            return Response(
                {"detail": "Список товаров не может быть пустым"},
                status=status.HTTP_400_BAD_REQUEST
            )

        products_info = []
        for product_sale in serializer.validated_data['product_sales']:
            product_id = product_sale['product_id']
            quantity = product_sale['quantity']

            try:
                product = Product.objects.get(id=product_id)
                if product.quantity < quantity:
                    return Response(
                        {
                            "detail": f"Недостаточно товара {product.title}. Доступно: {product.quantity}, запрошено: {quantity}"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                products_info.append((product, quantity))
            except Product.DoesNotExist:
                return Response(
                    {"detail": f"Товар с ID {product_id} не найден"},
                    status=status.HTTP_404_NOT_FOUND
                )

        try:
            sale = Sale.objects.create(
                buyer_name=serializer.validated_data['buyer_name'],
                company=request.user.company,
                sale_date=serializer.validated_data['sale_date']
            )

            for product, quantity in products_info:
                ProductSale.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity
                )
                product.quantity -= quantity
                product.save()

            serializer = SaleSerializer(sale)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SaleListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]
    pagination_class = PageNumberPagination

    @extend_schema(
        tags=['sales'],
        description="Получение списка продаж"
    )
    def get(self, request):
        company = request.user.company
        queryset = Sale.objects.filter(company=company)

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(sale_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(sale_date__lte=end_date)

        serializer = SaleSerializer(queryset, many=True)
        return Response(serializer.data)


class SaleUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]
    serializer_class = SaleUpdateSerializer

    @extend_schema(
        tags=['sales'],
        description="Обновление существующей продажи",
        request = SaleUpdateSerializer,
    )

    def put(self, request, pk):
        try:
            sale = Sale.objects.get(
                id=pk,
                company=request.user.company
            )

            serializer = self.serializer_class(
                sale,
                data=request.data,
                partial=True,
                context={'request': request}
            )

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data

            if 'product_sales' in validated_data:
                return Response(
                    {"detail": "Изменение списка товаров запрещено"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            sale.buyer_name = validated_data.get('buyer_name', sale.buyer_name)
            sale.sale_date = validated_data.get('sale_date', sale.sale_date)
            sale.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Sale.DoesNotExist:
            return Response(
                {"detail": "Продажа не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )


class SaleDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsRelatedToCompany]

    @extend_schema(
        tags=['sales'],
        description="Удаление продажи"
    )
    def delete(self, request, pk):
        try:
            sale = Sale.objects.get(
                id=pk,
                company=request.user.company
            )
            sale.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Sale.DoesNotExist:
            return Response(
                {"detail": "Продажа не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )
