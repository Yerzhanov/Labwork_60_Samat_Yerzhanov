from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')

    def __str__(self):
        return f'Продукт: {self.name} | Категория {self.category.name}'
