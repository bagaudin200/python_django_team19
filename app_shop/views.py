import json

from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import render
from app_shop.forms import OrderSettingForm


def admin_settings_view(request):
    """
    Сохраняет настройки в файл и выполняет очистку кэша
    """
    if request.user.is_superuser:
        if request.method == "POST":
            if "saveSettings" in request.POST:
                print(request.POST)
                form = OrderSettingForm(request.POST)
                if form.is_valid():
                    form_data = form.cleaned_data
                    with open("config/admin_settings.json", "w") as file:
                        json.dump(form_data, file)
                        messages.success(request, 'Data updated.')
                else:
                    form = OrderSettingForm()
                return render(request, 'admin/settings.html', {'form': form})
            elif "clearCache" in request.POST:
                cache.clear()
                form = OrderSettingForm()
                messages.success(request, 'cache cleared')
                return render(request, 'admin/settings.html', {'form': form})
