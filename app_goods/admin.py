from django.contrib import admin
from .models import Items, Category, Reviews


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'image', 'description', 'price', 'number')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment', 'item', 'create_date')



admin.site.register(Items, ItemsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reviews, ReviewsAdmin)
