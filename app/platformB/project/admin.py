from django.contrib import admin

from .models import Company, Storage, Supplier

admin.site.register(Company)
admin.site.register(Storage)
admin.site.register(Supplier)
