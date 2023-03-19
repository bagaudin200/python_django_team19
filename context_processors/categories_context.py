from app_goods.models import Category


def categories(request):
    all_categories = Category.objects.select_related('parent')
    slugs = [category.slug for category in all_categories]

    icons_paths = []
    banners_paths = []
    for category in all_categories:
        icons_paths.append(f"img/icons/categories/{category.slug}.png")
        banners_paths.append(f"img/content/home/{category.slug}.png")

    return {
        'main_categories': all_categories.filter(level=0),
        'category_icons_paths': {slug: path for slug, path in zip(slugs, icons_paths)},
        'category_banners_paths': {slug: path for slug, path in zip(slugs, banners_paths)},
    }
