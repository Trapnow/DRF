from django.contrib import admin

from .models import Company, Storage, Supplier, Supply, Product, Sale, ProductSale


class ProductSaleInline(admin.TabularInline):
    model = ProductSale
    extra = 1
    readonly_fields = ('product', 'quantity')

admin.site.register(Company)
admin.site.register(Storage)
admin.site.register(Supplier)
admin.site.register(Supply)
admin.site.register(Product)
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer_name', 'sale_date', 'company')
    search_fields = ('buyer_name',)
    list_filter = ('sale_date', 'company')
    inlines = [ProductSaleInline]
    readonly_fields = ('id',)
    date_hierarchy = 'sale_date'

    fieldsets = (
        (None, {
            'fields': ('buyer_name', 'company', 'sale_date')
        }),
    )


