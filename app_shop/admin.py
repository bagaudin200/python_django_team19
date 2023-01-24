from django.contrib import admin
from .models import Shops


class ShopsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')



admin.site.register(Shops, ShopsAdmin)
