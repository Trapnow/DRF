from django.urls import path, include

from .views import CompanyAPIView

urlpatterns = [
    path('companies/', CompanyAPIView.as_view({
        'post': 'post',
        'put': 'put',
        'delete': 'delete'
    }), name='company-operations'),
]
