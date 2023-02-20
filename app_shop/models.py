from django.core.validators import MaxValueValidator
from django.db import models


class Shops(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'shop'
        verbose_name_plural = 'shops'

    def __str__(self):
        return f'{self.name}'

class SiteSettings(models.Model):
    """Модель настроек сайта"""
    min_order_price_for_free_shipping = models.DecimalField(max_digits=6, decimal_places=2,
                                                            verbose_name='minimum order price for free shipping')
    standard_order_price = models.DecimalField(max_digits=6, decimal_places=2,
                                               verbose_name='standard order price')
    express_order_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='express order price')
    banners_count = models.PositiveIntegerField(validators=[MaxValueValidator(3)],
                                                verbose_name='banners count')
    days_offer = models.BooleanField(verbose_name='show days offer')
    top_items_count = models.PositiveIntegerField(validators=[MaxValueValidator(8)],
                                                  verbose_name='top items count')
    limited_edition_count = models.PositiveIntegerField(validators=[MaxValueValidator(16)],
                                                        verbose_name='limited edition count')

    def __str__(self) -> str:
        return "site settings"

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'settings'
        verbose_name = 'settings'
