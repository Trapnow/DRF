from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Company
from .serializer import CompanySerializer
from .permissions import IsCompanyOwnerOrReadAndCreate


@extend_schema(tags=['company'])
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrReadAndCreate]

    @extend_schema(
        description="Создание компании. Доступно только авторизированным пользователям.")
    @action(detail=False, methods=["POST"], url_path="create")
    def create_company(self, request, *args, **kwargs):
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
    @action(detail=False, methods=["DELETE"], url_path="delete")
    def delete_company(self, request):
        company = self.get_object()

        if not (request.user.is_company_owner and request.user.company == company):
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
    @action(detail=False, methods=['PUT'], url_path="update")
    def update_company(self, request):
        company = self.get_object()

        if not (request.user.is_company_owner and request.user.company == company):
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
