from app_settings.models import SiteSettings


def load_settings(request):
    return {'site_settings': SiteSettings.load()}
