from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=40)


class Items(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=100, verbose_name='Категория')
    image = models.ImageField(upload_to='static/', verbose_name='Изображение')
    description = models.CharField(max_length=1000, verbose_name='Описание')
    #price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена')
    reviews = models.PositiveIntegerField(default=0, verbose_name='Количество отзывов')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name}'


class ShopItems(models.Model):

    code = models.ForeignKey(Items, max_length=100, on_delete=models.CASCADE, verbose_name='Артикул')
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE, verbose_name='Магазин')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена')
    number = models.PositiveIntegerField(default=0, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в магазине'
        verbose_name_plural = 'Товары в магазине'

    def __str__(self):
        return f'{self.code}'
