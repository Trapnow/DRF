from django.contrib import admin
from . import models


@admin.register(models.University)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["name", "country"]


@admin.register(models.Course)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(models.UniversityCourse)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["university", "course"]
