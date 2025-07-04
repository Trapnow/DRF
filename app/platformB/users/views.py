from rest_framework.generics import CreateAPIView
from .models import User
from .serializer import UserSerializer

class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

