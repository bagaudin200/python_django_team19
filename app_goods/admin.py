from django.contrib import admin
from .models import Items, ShopItems


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'image', 'description', 'reviews')


class ShopItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'shop', 'price', 'number')



admin.site.register(Items, ItemsAdmin)
admin.site.register(ShopItems, ShopItemsAdmin)
