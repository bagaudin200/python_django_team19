from django.core.validators import MaxValueValidator
from django.db import models


class SiteSettings(models.Model):
        """Модель настроек сайта"""
        min_order_price_for_free_shipping = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='минимальная стоимость заказа для бесплатной доставки')
        standard_order_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='цена стандартной доставки')
        express_order_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='цена экспресс доставки')
        banners_count = models.PositiveIntegerField(validators=[MaxValueValidator(3)], verbose_name='количество баннеров')
        days_offer = models.BooleanField(verbose_name='показывать предложение дня')
        top_items_count = models.PositiveIntegerField(validators=[MaxValueValidator(8)], verbose_name='количество топ товаров')
        limited_edition_count = models.PositiveIntegerField(validators=[MaxValueValidator(16)], verbose_name='количество товаров ограниченного тиража')

        def __str__(self) -> str:
            return "настройки сайта"


        def save(self, *args, **kwargs):
            if self.__class__.objects.count():
                self.pk = self.__class__.objects.first().pk
            super().save(*args, **kwargs)

        class Meta:
            verbose_name_plural = 'настройки'
            verbose_name = 'настройки'
