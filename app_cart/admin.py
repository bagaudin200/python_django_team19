from django.contrib import admin
from .models import Cart, Cart2Product


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(Cart2Product)
class Cart2ProductAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
