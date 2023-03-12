from django.db import models
from users.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, default='Other')
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name='Описание продукта')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', verbose_name='Картинка')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'Продукт: {self.name} | Категория {self.category.name}'

class BasketQuerrySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerrySet.as_manager()
    def __str__(self):
        return f'Корзина для {self.user.username} - {self.user.email} | Продукт {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity
