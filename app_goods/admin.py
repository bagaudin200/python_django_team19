from django.contrib import admin
from .models import Product, Category, Image, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'quantity', 'slug', 'short_description', 'tag_list')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'product',)
    list_filter = ('product',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', )
