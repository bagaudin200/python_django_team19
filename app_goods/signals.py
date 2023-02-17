from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from app_goods.models import Product


@receiver(post_save, sender=Product)
def clear_cache_after_update_product_info(created, **kwargs):
    instance = kwargs['instance']
    if not created:
        cache.delete(f"product:{instance.slug}")
