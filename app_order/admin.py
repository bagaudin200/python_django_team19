from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['cart', 'created_at', 'delivery_type', 'payment_type', 'status']
