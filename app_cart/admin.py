from django.contrib import admin
from app_cart.models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quantity', 'price']


admin.site.register(Cart, CartAdmin)
