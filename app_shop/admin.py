from django.contrib import admin

from app_shop.models import SiteSettings


class SiteSettingsAdmin(admin.ModelAdmin):
    change_form_template = 'admin/settings.html'


admin.site.register(SiteSettings, SiteSettingsAdmin)
