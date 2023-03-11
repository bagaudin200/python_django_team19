
from app_goods.services.catalog_services import CatalogPaginator, CatalogQueryStringBuilder, CatalogQuerySetBuilder
from .services.services import get_top_products, get_limited_product
from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import Page
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from app_cart.services import Cart
from app_goods.forms import AddProductToCardForm, ReviewsForm

from app_goods.models import Category, Review, Image
from .forms import FilterForm
from .services import get_cheapest_product_price, get_most_expensive_product_price, get_top_products, \
    get_limited_product, get_update_quantity_product, ReviewService, check_product_quantity
from .utils import CatalogPaginator
from app_goods.models import Product


class GoodsDetailView(DetailView):
    model = Product
    template_name = 'app_goods/product.jinja2'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        obj = cache.get(f"product:{slug}")
        if not obj:
            obj = super(GoodsDetailView, self).get_object()
            cache.set(f"product:{slug}", obj)
        return obj

    def post(self, request, *args, **kwargs):
        form = AddProductToCardForm(request.POST)
        if form.is_valid():
            user = self.request.user
            product = self.get_object()
            quantity = form.cleaned_data['quantity']
            if check_product_quantity(product=product, quantity=quantity):
                update_product = get_update_quantity_product(product=product,
                                                             user=user
                                                             )
                cart = Cart(user)
                cart.add(product=product,
                         quantity=quantity,
                         update_quantity=update_product,
                         )
                messages.success(request, 'Successful! Product added to cart!')
            else:
                messages.error(request, f"Unsuccessful. Have only {quantity}")
        return redirect(request.META.get('HTTP_REFERER'))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        user = self.request.user
        review_service = ReviewService(user)
        images = Image.objects.filter(product=product)[1:]
        context['images'] = images
        context['reviews'] = review_service.get_reviews_for_product(product)
        context['product_form'] = AddProductToCardForm()
        context['review_form'] = ReviewsForm()
        return context


def add_review(request):
    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():
            review = ReviewService(request.user)
            text = form.cleaned_data['text']
            review.add(request.POST['product'], text)
    return redirect(request.META.get('HTTP_REFERER'))


class CatalogView(FormMixin, ListView):
    form_class = FilterForm
    template_name = 'app_goods/catalog.jinja2'
    context_object_name = 'products'
    paginator_class = CatalogPaginator
    paginate_by = 8
    __order_by = {'popular': 'Популярности', 'price': 'Цене', 'reviews': 'Отзывам', 'novelty': 'Новизне'}

    def get_context_data(self, **kwargs):
        context = super(FormMixin, self).get_context_data(**kwargs)
        context['orders_by'] = self.__order_by
        page: Page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number)
        context['popular_tags'] = Product.tags.most_common()[:20]
        context['query_string_builder'] = CatalogQueryStringBuilder
        return context

    def get_queryset(self):
        builder = CatalogQuerySetBuilder(request=self.request)
        return builder.build()


class ShopView(TemplateView):
    template_name = 'app_goods/index.jinja2'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = get_top_products()
        context['is_limited'] = get_limited_product()

        return context
