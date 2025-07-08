from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.permissions import IsCompanyOwnerOrReadOnly

from .models import User
from .serializer import UserSerializer, AttachUserSerializer


@extend_schema(tags=['users'])
class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(tags=['users'], description="Прикрепление пользователя к компании",
               request=AttachUserSerializer)
class AttachUserToCompanyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrReadOnly]
    serializer_class = AttachUserSerializer

    def post(self, request):
        serializer = AttachUserSerializer(data=request.data)
        user_company = request.user.company
        if not user_company:
            return Response(
                {"detail": "У вас нет компании для прикрепления пользователей"},
                status=status.HTTP_403_FORBIDDEN
            )
        if serializer.is_valid():
            email = serializer.validated_data['email']

        try:
            user_to_attach = User.objects.get(email=email)

            if user_to_attach.company_id:
                return Response(
                    {"detail": "Пользователь уже прикреплен к другой компании"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if user_to_attach.is_company_owner:
                return Response(
                    {"detail": "Пользователь уже является владельцем другой компании"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_to_attach.company = user_company
            user_to_attach.save()

            return Response(
                {"detail": "Пользователь успешно прикреплен к вашей компании"},
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"detail": "Пользователь с таким email не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
