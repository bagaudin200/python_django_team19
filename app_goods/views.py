from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from app_cart.services import Cart
from app_goods.models import Product, Review
from .forms import AddProductToCardForm, ReviewsForm
from .services import get_cheapest_product, get_most_expensive_product, get_update_quantity_product
from django.contrib import messages


class GoodsDetailView(DetailView):
    model = Product
    template_name = 'app_goods/product.jinja2'
    context_object_name = 'product'
    form = AddProductToCardForm()

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
        context['reviews'] = Review.objects.filter(product_id=product.id)
        context['product_form'] = AddProductToCardForm()
        context['review_form'] = ReviewsForm()
        return context


class AddReview(View):
    def post(self, request, slug):
        print('request', request)
        print('slug', slug)
        return HttpResponse('1')


class CatalogView(FormMixin, ListView):
    template_name = 'app_goods/catalog.jinja2'
    context_object_name = 'products'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(FormMixin, self).get_context_data(**kwargs)
        context['cheapest'] = get_cheapest_product(self.get_queryset())
        context['most_expensive'] = get_most_expensive_product(self.get_queryset())
        return context

    def get_queryset(self):
        if self.request.GET:
            category_name = self.request.GET.get('category')
            return Product.objects.filter(category__name=category_name).select_related('category__parent',
                                                                                       'category').order_by('price')
        return Product.objects.select_related('category__parent', 'category').order_by('price')
