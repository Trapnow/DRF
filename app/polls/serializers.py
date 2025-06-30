from rest_framework.decorators import action
from rest_framework import serializers
from .models import *
from rest_framework.response import Response


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        read_only_fields = ['id']
        fields = [
            "id",
            "name",
            "description",
        ]


class UniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        read_only_fields = ['id']
        fields = [
            "id",
            "name",
            "country",
        ]


class UCSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    university = UniversitySerializer()

    class Meta:
        model = UniversityCourse
        read_only_fields = ['id']
        fields = [
            "id",
            "university",
            "course",
            "semester",
            "duration_weeks",
        ]
