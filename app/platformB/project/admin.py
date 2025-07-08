from django.contrib import admin

from .models import Company, Storage, Supplier, Supply, Product

admin.site.register(Company)
admin.site.register(Storage)
admin.site.register(Supplier)
admin.site.register(Supply)
admin.site.register(Product)


