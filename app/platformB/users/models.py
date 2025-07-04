from django.db import models
from django.contrib.auth.models import Permission, AbstractUser
from project.models import Company

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_company_owner = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
