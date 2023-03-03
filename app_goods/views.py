from django.core.paginator import Page
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from app_goods.forms import Reviewsform
from app_goods.models import Product
from app_goods.services.catalog_services import CatalogPaginator, CatalogQueryStringBuilder, CatalogQuerySetBuilder
from .forms import FilterForm
from .services.services import get_top_products, get_limited_product


class GoodsDetailView(FormMixin, DetailView):
    form_class = Reviewsform
    model = Product
    template_name = 'app_goods/product.jinja2'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('product', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if request.user.is_authenticated:
            form.instance.user = request.user
            form.instance.product = self.object
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_review = form.save(commit=False)
        new_review.save()
        return super(GoodsDetailView, self).form_valid(form)


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
    template_name = 'index.jinja2'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = get_top_products()
        context['is_limited'] = get_limited_product()

        return context
