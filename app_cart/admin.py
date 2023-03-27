from django.contrib import admin

from app_cart.models import Cart, ProductInCart


class ProductInCartInline(admin.TabularInline):
    model = ProductInCart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    inlines = [ProductInCartInline]


@admin.register(ProductInCart)
class ProductInCartAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity']
