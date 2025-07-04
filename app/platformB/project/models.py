from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    inn = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Storage(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return f"Склад компании {self.company.name}"
