from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from .models import User
from .serializer import UserSerializer


@extend_schema(tags=['users'])
class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

