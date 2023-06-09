from django.db import models

from app_cart.models import Cart


class Order(models.Model):
    """Модель заказа"""
    DELIVERY_TYPES_DICT = {
        'regular': 'обычная доставка',
        'express': 'экспресс-доставка'
    }

    DELIVERY_TYPES = [
        ('regular', 'обычная доставка'),
        ('express', 'экспресс-доставка')
    ]

    PAYMENT_TYPES_DICT = {
        'card': 'онлайн картой',
        'random': 'онлайн со случайного чужого счета'
    }

    PAYMENT_TYPES = [
        ('card', 'онлайн картой'),
        ('random', 'онлайн со случайного чужого счета')
    ]

    STATUS_CREATED = 'created'
    STATUS_OK = 'ok'
    STATUS_DELIVERED = 'delivered'
    STATUS_PAID = 'paid'
    STATUS_NOT_PAID = 'not paid'
    STATUS_CHOICES = [
        ('Success', (
            (STATUS_CREATED, 'создан'),
            (STATUS_OK, 'выполнен'),
            (STATUS_DELIVERED, 'доставляется'),
            (STATUS_PAID, 'оплачен'),
        )
         ),
        (STATUS_NOT_PAID, 'не оплачен')
    ]
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')
    delivery_type = models.CharField(max_length=50, choices=DELIVERY_TYPES, verbose_name='delivery type', blank=False,
                                     default=DELIVERY_TYPES[0])
    city = models.CharField(max_length=50, verbose_name='city')
    address = models.CharField(max_length=255, verbose_name='address')
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPES, blank=False, default=PAYMENT_TYPES[0],
                                    verbose_name='payment type')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name='status')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, verbose_name='cart')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='total price')

    class Meta:
        db_table = 'order'

    def __str__(self):
        return f"Order #{self.id} by {self.cart.user}"
