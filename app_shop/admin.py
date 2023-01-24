from django.contrib import admin
from .models import Shops


class ShopsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


from app_shop.models import SiteSettings


class SiteSettingsAdmin(admin.ModelAdmin):
    change_form_template = 'admin/settings.html'


admin.site.register(SiteSettings, SiteSettingsAdmin)
