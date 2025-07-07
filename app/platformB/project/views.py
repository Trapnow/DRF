from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company, Storage, Supplier
from .serializer import CompanySerializer, StorageSerializer, StorageDetailSerializer, SupplierSerializer
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
        request_data['company'] = request.user.company.pk
        print(request_data)

        serializer = SupplierSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
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
        description="Удаление поставщика"
    )
    def delete(self, request, pk):
        try:
            supplier = Supplier.objects.get(pk=pk, company=request.user.company)
            supplier.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Supplier.DoesNotExist:
            return Response({"detail": "Поставщик не найден"}, status=status.HTTP_404_NOT_FOUND)


