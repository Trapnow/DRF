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


class Supplier(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    inn = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Поставщик {self.title}"


class Supply(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    delivery_date = models.DateTimeField()

    def __str__(self):
        return f"Поставка - {self.supplier}"


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)

    def __str__(self):
        return f"Продукт - {self.title}"


class SupplyProduct(models.Model):
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} {self.product.title} в поставке {self.supply.id}"


class Sale(models.Model):
    buyer_name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    sale_date = models.DateTimeField()

    def __str__(self):
        return f"Продажа - {self.buyer_name}"


class ProductSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, related_name='product_sales', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
