from django.contrib import admin
from .models import Shops, SiteSettings


class ShopsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class SiteSettingsAdmin(admin.ModelAdmin):
    change_form_template = 'admin/settings.html'


admin.site.register(SiteSettings, SiteSettingsAdmin)
