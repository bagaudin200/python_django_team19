from django.db import models

from app_goods.models import Product
from app_users.models import User


class Cart(models.Model):
    """Модель корзины"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')
    products = models.ManyToManyField(Product, through='Cart2Product')

    class Meta:
        db_table = 'cart'
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    def __str__(self):
        return f"{self.user}"


class Cart2Product(models.Model):
    """Промежуточная модель между Cart и Product"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product')
    quantity = models.PositiveIntegerField(verbose_name='quantity')
