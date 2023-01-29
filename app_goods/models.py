from django.db import models
from app_shop.models import Shops


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.name}'


class Items(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=100, verbose_name='category')
    image = models.ImageField(upload_to='static/', verbose_name='image')
    description = models.CharField(max_length=1000, verbose_name='description')
    reviews = models.PositiveIntegerField(default=0, verbose_name='reviews')

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'

    def __str__(self):
        return f'{self.name}'


class ShopItems(models.Model):

    code = models.ForeignKey(Items, max_length=100, on_delete=models.CASCADE, verbose_name='code')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE, verbose_name='shop')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='price')
    number = models.PositiveIntegerField(default=0, verbose_name='number')

    class Meta:
        verbose_name = 'shopitem'
        verbose_name_plural = 'shopitems'

    def __str__(self):
        return f'{self.code}'
