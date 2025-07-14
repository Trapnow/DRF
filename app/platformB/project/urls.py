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

    path('suppliers/list/', SupplierListAPIView.as_view(), name='suppliers-list'),
    path('suppliers/create/', SupplierCreateAPIView.as_view(), name='supplier-create'),
    path('suppliers/<int:pk>/update/', SupplierUpdateAPIView.as_view(), name='supplier-update'),
    path('suppliers/<int:pk>/delete/', SupplierDestroyAPIView.as_view(), name='supplier-delete'),

    path('products/list/', ProductListAPIView.as_view(), name='products-list'),
    path('products/add/', ProductCreateAPIView.as_view(), name='product-add'),
    path('products/<int:pk>/update/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDestroyAPIView.as_view(), name='product-delete'),

    path('supplies/list/', SupplyListAPIView.as_view(), name='supply-list'),
    path('supplies/create/', SupplyCreateAPIView.as_view(), name='supply-add'),

    path('sales/list/', SaleListAPIView.as_view(), name='sales-list'),
    path('sales/add/', SaleCreateAPIView.as_view(), name='sale-add'),
    path('sales/<int:pk>/update/', SaleUpdateAPIView.as_view(), name='sale-update'),
    path('sales/<int:pk>/delete/', SaleDestroyAPIView.as_view(), name='sale-delete'),
]
