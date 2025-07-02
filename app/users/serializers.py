from rest_framework import serializers
from .models import User, Role
from django.contrib.auth.models import Permission


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "password"]

        def create(self, validated_data):
            user = User.objects.create_user(username=validated_data['username'],
                                            password=validated_data['password'])

            role, created = Role.objects.get_or_create(name="candidate")

            if created:
                role.description = "Может добавлять, просматривать и менять только своё резюме"
                role.save()
                view_question = Permission.objects.get(codename="view_question")
                add_question = Permission.objects.get(codename="add_question")
                change_question = Permission.objects.get(codename="change_question")
                role.permissions.set([view_question, add_question, change_question])

            user.role = role
            user.save()

            return user
