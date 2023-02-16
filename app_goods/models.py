from django.db import models


class Category(MPTTModel):
    """Модель категорий товара"""
    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(blank=True, upload_to='category/', verbose_name='Изображение')

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_absolute_url(self):
        return reverse('product-by-category', args=[str(self.slug)])

    def get_min(self):
        sub_categories = self.get_descendants(include_self=True)
        price = Product.objects.values('price').filter(category__in=sub_categories).filter(available=True).aggregate(
            Min('price'))['price__min']
        return price

    def __str__(self):
        return f'{self.name}'


class Items(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=100, verbose_name='category')
    image = models.ImageField(upload_to='static/', verbose_name='image')
    description = models.CharField(max_length=1000, verbose_name='description')
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='price')
    number = models.PositiveIntegerField(default=0, verbose_name='number')

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'

    def __str__(self):
        return f'{self.name}'


class Reviews(models.Model):

    user = models.ForeignKey('app_users.User', default=None, null=True, on_delete=models.CASCADE, related_name='user',
                             verbose_name='user')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    comment = models.CharField(max_length=1000, default='', verbose_name='comment')
    item = models.ForeignKey(Items, max_length=100, on_delete=models.CASCADE, related_name='reviews',
                             verbose_name='item')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='date')

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'

    def __str__(self):
        return f'{self.item}'
