from django.core.validators import MaxValueValidator
from django.db import models
from app_settings.singleton_model import SingletonModel


class SiteSettings(SingletonModel):
    """Модель настроек сайта"""
    min_order_price_for_free_shipping = models.DecimalField(max_digits=6, decimal_places=2, default=100.00,
                                                            verbose_name='minimum order price for free shipping, $')
    standard_order_price = models.DecimalField(max_digits=6, decimal_places=2, default=10.00,
                                               verbose_name='standard order price, $')
    express_order_price = models.DecimalField(max_digits=6, decimal_places=2, default=25.00,
                                              verbose_name='express order price, $')
    banners_count = models.PositiveIntegerField(validators=[MaxValueValidator(3)], default=3,
                                                verbose_name='banners count')
    days_offer = models.BooleanField(verbose_name='show days offer', default=True)
    top_items_count = models.PositiveIntegerField(validators=[MaxValueValidator(8)], default=8,
                                                  verbose_name='top items count')
    limited_edition_count = models.PositiveIntegerField(validators=[MaxValueValidator(16)], default=16,
                                                        verbose_name='limited edition count')

    product_cache_time = models.PositiveIntegerField(default=1, verbose_name='product cache time, days')

    def __str__(self) -> str:
        return "site settings"

    class Meta:
        verbose_name_plural = 'settings'
        verbose_name = 'settings'
