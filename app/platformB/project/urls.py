from django.urls import path, include

from .views import *

urlpatterns = [
    path('companies/<int:pk>/', CompanyRetrieveAPIView.as_view(), name='company-retrieve'),
    path('companies/create/', CompanyCreateAPIView.as_view(), name='company-create'),
    path('companies/delete/', CompanyDestroyAPIView.as_view(), name='company-delete'),
    path('companies/update/', CompanyUpdateAPIView.as_view(), name='company-update'),


    path('storages/<int:pk>/', StorageRetrieveAPIView.as_view(), name='storage-retrieve'),
    path('storages/create/', StorageCreateAPIView.as_view(), name='storage-create'),
    path('storages/<int:pk>/update/', StorageUpdateAPIView.as_view(), name='storage-update'),
    path('storages/<int:pk>/delete/', StorageDestroyAPIView.as_view(), name='storage-delete'),

    path('suppliers/list/', SupplierListAPIView.as_view(), name='supplier-list'),
    path('suppliers/create/', SupplierCreateAPIView.as_view(), name='supplier-create'),
    path('suppliers/<int:pk>/update/', SupplierUpdateAPIView.as_view(), name='supplier-update'),
    path('suppliers/<int:pk>/delete/', SupplierDestroyAPIView.as_view(), name='supplier-delete'),
]
