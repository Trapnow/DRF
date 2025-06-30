from django.db import models
from django.db.models import CASCADE


class University(models.Model):
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}({self.country})"


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class UniversityCourse(models.Model):
    university = models.ForeignKey(University, on_delete=CASCADE, related_name='university')
    course = models.ForeignKey(Course, on_delete=CASCADE, related_name='course')
    semester = models.CharField(max_length=20)
    duration_weeks = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'semester', 'university'], name="unique course and semester and university")
        ]

    def __str__(self):
        return f"{self.university.name} - {self.course.name}"