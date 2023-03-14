from django.db import models

from products.models import Basket
from users.models import User

class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан заказ'),
        (PAID, 'Заказ оплачен'),
        (ON_WAY, 'Заказ в пути'),
        (DELIVERED, 'Заказ доставлен'),
    )

    first_name = models.CharField(max_length=64, verbose_name='Имя заказчика')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия заказчика')
    email = models.EmailField(max_length=256, verbose_name='Электронная почта')
    address = models.CharField(max_length=256, verbose_name='Адрес')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    basket_history = models.JSONField(default=dict)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order #{self.id}. {self.first_name}  {self.last_name}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchase_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
            }
        baskets.delete()
        self.save()
