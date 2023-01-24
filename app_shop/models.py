from django.db import models

class Shops(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return f'{self.name}'
