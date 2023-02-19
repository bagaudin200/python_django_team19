from app_goods.models import Category


def categories(request):
    all_categories = Category.objects.all()
    slugs = [category.slug for category in all_categories]
    paths = [f"img/icons/categories/{category.slug}.png" for category in all_categories]
    return {
        'main_categories': all_categories.filter(level=0),
        'category_icons_paths': {slug: path for slug, path in zip(slugs, paths)}
    }
