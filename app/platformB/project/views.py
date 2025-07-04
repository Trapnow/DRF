from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .serializer import CompanySerializer
from .permissions import IsCompanyOwnerOrReadOnly


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrReadOnly]

    def perform_create(self, serializer):
        self.request.user.is_company_owner = True
        company = serializer.save()
        self.request.user.company = company
        self.request.user.save()
