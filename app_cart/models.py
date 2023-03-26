from django.contrib.auth import get_user_model
from django.db import models

from app_goods.models import Product

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # class Meta:
    #     db_table = 'cart'

    def __str__(self):
        return f'Cart {self.user}'


class ProductInCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField()
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_in_cart'
        verbose_name = 'product in cart'
        verbose_name_plural = 'products in cart'
        # ordering = ('-created_at',)

    def __str__(self):
        return f"Product {self.product} in cart {self.cart}"
