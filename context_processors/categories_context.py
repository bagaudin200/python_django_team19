from app_goods.models import Category


def categories(request):
    main_categories = Category.objects.filter(parent=None)
    return {
        'main_categories': main_categories,
    }
