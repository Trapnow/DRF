from drf_spectacular.utils import extend_schema
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Company
from .serializer import CompanySerializer
from .permissions import IsCompanyOwnerOrReadAndCreate


@extend_schema(tags=['company'])
class CompanyAPIView(generics.GenericAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrReadAndCreate]

    @extend_schema(
        description="Получение компании по ID. Доступно всем авторизованным пользователям.")
    def get(self, request, pk, *args, **kwargs):
        company = Company.objects.get(pk=pk)
        serializer = self.get_serializer(company)
        return Response(serializer.data)

    @extend_schema(
        description="Создание компании. Доступно только авторизированным пользователям.")
    def post(self, request, *args, **kwargs):
        if request.user.company is not None:
            return Response({"detail": "У Вас уже есть компания"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()

        request.user.is_company_owner = True
        request.user.company = company
        request.user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Удаление компании. Доступно только владельцу компании.")
    def delete(self, request):
        company = request.user.company

        if not (request.user.is_company_owner and company):
            return Response({
                "detail": "Вы не являетесь владельцем этой компании"
            }, status=status.HTTP_403_FORBIDDEN)

        company.delete()

        request.user.is_company_owner = False
        request.user.company = None
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        description="Редактирование компании. Доступно только владельцу компании.")
    def put(self, request):
        company = request.user.company

        if not (request.user.is_company_owner and company):
            return Response({
                "detail": "У вас нет прав на изменение компании"
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(
            company,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
