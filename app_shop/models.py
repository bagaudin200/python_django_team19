from django.db import models

class Shops(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'shop'
        verbose_name_plural = 'shops'

    def __str__(self):
        return f'{self.name}'
