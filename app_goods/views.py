from django.core.cache import cache
from django.core.paginator import Page
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from app_cart.services import Cart
from app_goods.forms import AddProductToCardForm, ReviewsForm

from app_goods.models import Category, Review
from .forms import FilterForm
from .services import get_cheapest_product_price, get_most_expensive_product_price, get_top_products, \
    get_limited_product, get_update_quantity_product, ReviewService
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
            product = self.get_object()
            user = self.request.user
            quantity = form.cleaned_data['quantity']
            update_product = get_update_quantity_product(product=product,
                                                         user=user
                                                         )
            cart = Cart(user)
            cart.add(product=product,
                     quantity=quantity,
                     update_quantity=update_product,
                     )
        return redirect(request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        user = self.request.user
        review_service = ReviewService(user)
        context['reviews'] = review_service.get_reviews_for_product(product)
        context['product_form'] = AddProductToCardForm()
        context['review_form'] = ReviewsForm()
        return context

    # class GoodsDetailView(FormMixin, DetailView):
    #     form_class = Reviewsform
    #     model = Product
    #     template_name = 'app_goods/product.jinja2'
    #     slug_url_kwarg = 'slug'
    #     context_object_name = 'product'
    #
    #     def get_success_url(self):
    #         return reverse('product', kwargs={'slug': self.object.slug})
    #
    #     def post(self, request, *args, **kwargs):
    #         self.object = self.get_object()
    #         form = self.get_form()
    #         if request.user.is_authenticated:
    #             form.instance.user = request.user
    #             form.instance.product = self.object
    #         if form.is_valid():
    #             return self.form_valid(form)
    #         else:
    #             return self.form_invalid(form)
    #
    #     def form_valid(self, form):
    #         new_review = form.save(commit=False)
    #         new_review.save()
    #         return super(GoodsDetailView, self).form_valid(form)


class AddReview(View):
    def post(self, request, *args, **kwargs):
        form = ReviewsForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            user = request.POST.user
            review_service = ReviewService(user)
            review_service.add()
        return redirect(request.META.get('HTTP_REFERER'))



class CatalogView(FormMixin, ListView):
    form_class = FilterForm
    template_name = 'app_goods/catalog.jinja2'
    context_object_name = 'products'
    paginator_class = CatalogPaginator
    paginate_by = 8
    __order_by = {'popular': 'Популярности', 'price': 'Цене', 'reviews': 'Отзывам', 'novelty': 'Новизне'}
    queryset = Product.objects.select_related('category', 'category__parent').defer('description', 'quantity').order_by(
        'price')

    def get_context_data(self, **kwargs):
        context = super(FormMixin, self).get_context_data(**kwargs)
        context['orders_by'] = self.__order_by
        context['cheapest'] = get_cheapest_product_price(self.queryset)
        context['most_expensive'] = get_most_expensive_product_price(self.queryset)
        page: Page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number)
        context['popular_tags'] = Product.tags.most_common()[:20]
        return context

    def get_queryset(self):
        category = self._get_category()
        order = self._get_order()
        order_by = self._get_order_by()
        price_from, price_to = self._get_price_range()
        name = self.request.GET.get('title')
        in_stock = self._get_in_stock()
        free_delivery = self._get_free_delivery()
        tag = self._get_tag()

        qs = self.queryset
        if category:
            filter_kwargs = dict(category__parent=category) if category.get_children() else dict(category=category)
            qs = qs.filter(**filter_kwargs)
        if price_from and price_to:
            qs = qs.filter(price__range=[price_from, price_to])
        if name:
            qs = qs.filter(name__icontains=name)
        if in_stock:
            qs = qs.filter(quantity__gt=0)
        if free_delivery:
            qs = qs.filter(free_delivery=free_delivery)
        if tag:
            qs = Product.objects.select_related('category', 'category__parent').prefetch_related('tags').filter(
                tags__slug=tag)
        qs = qs.order_by(f"{order}{order_by}")
        self.queryset = qs
        return qs

    def _get_category(self):
        category = self.request.GET.get('category')
        if category not in Category.objects.values_list('slug', flat=True):
            return None
        return Category.objects.get(slug=category)

    def _get_order(self):
        order = self.request.GET.get('order')
        if order == 'desc':
            return '-'
        return ''

    def _get_order_by(self):
        order_by = self.request.GET.get('order_by')
        if not (order_by in self.__order_by):
            return 'price'
        if order_by == 'novelty':
            order_by = 'created_at'
        return order_by

    def _get_price_range(self):
        prices = self.request.GET.get('price')
        return tuple(prices.split(';')) if prices else (None, None)

    def _get_in_stock(self):
        in_stock = self.request.GET.get('in_stock')
        try:
            result = bool(int(in_stock))
            return result
        except (TypeError, ValueError):
            return False

    def _get_free_delivery(self):
        free_delivery = self.request.GET.get('free_delivery')
        try:
            result = bool(int(free_delivery))
            return result
        except (TypeError, ValueError):
            return False

    def _get_tag(self):
        tag = self.request.GET.get('tag')
        return tag


class ShopView(TemplateView):
    template_name = 'index.jinja2'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = get_top_products()
        context['is_limited'] = get_limited_product()

        return context