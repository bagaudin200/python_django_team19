from django.contrib import admin
from .models import Items, ShopItems, Category


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'image', 'description', 'reviews')


class ShopItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'shop', 'price', 'number')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')



admin.site.register(Items, ItemsAdmin)
admin.site.register(ShopItems, ShopItemsAdmin)
admin.site.register(Category, CategoryAdmin)
