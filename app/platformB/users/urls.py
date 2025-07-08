from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path('attach-user/', views.AttachUserToCompanyAPIView.as_view(), name='attach-user-to-company'),
]
