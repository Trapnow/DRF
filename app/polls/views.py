from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from django.db.models import Avg

from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from .models import *


class UniversityViewSet(ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    @action(detail=True, methods=['GET'], url_path="courses",
            url_name="university-courses")
    def university_courses(self, request, pk=None):
        university = self.get_object()
        courses = UniversityCourse.objects.filter(university=university)
        university_serializer = UCSerializer(courses, many=True)
        return Response(university_serializer.data, status=200)

    @action(detail=True, methods=['get'])
    def course_stats(self, request, pk=None):
        university = self.get_object()
        courses = UniversityCourse.objects.filter(university=university)

        total_courses = courses.count()
        average_duration = courses.aggregate(avg_duration=Avg('duration_weeks'))['avg_duration']

        stats = {
            'total-courses': total_courses,
            'average_duration': average_duration
        }

        return Response(stats)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class UCViewSet(ModelViewSet):
    queryset = UniversityCourse.objects.all()
    serializer_class = UCSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["duration_weeks"]
    filterset_fields = {
        "course__name": ["exact", "contains"],
    }
