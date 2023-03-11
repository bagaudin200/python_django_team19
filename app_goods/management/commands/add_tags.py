from django.core.management.base import BaseCommand

from app_goods.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            tags = [tag.lower() for tag in product.name.split() if len(tag) > 2 and tag.isalpha()]
            for t in tags:
                product.tags.add(t)
            product.save()
        print('Теги добавлены')
