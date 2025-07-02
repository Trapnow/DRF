from rest_framework.authtoken.views import obtain_auth_token

from . import views
from django.urls import path, include

urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("auth-token/", obtain_auth_token, name="obtain-auth-token")
]
