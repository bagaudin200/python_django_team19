from django.contrib import admin
from .models import SiteSettings


class SiteSettingsAdmin(admin.ModelAdmin):
    change_form_template = 'app_settings/settings.html'


admin.site.register(SiteSettings, SiteSettingsAdmin)

