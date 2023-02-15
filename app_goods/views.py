from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from app_goods.forms import Reviewsform
from app_goods.models import Product
from .services import get_cheapest_product, get_most_expensive_product


class GoodsDetailView(FormMixin, DetailView):
    form_class = Reviewsform
    model = Product
    template_name = 'app_goods/product.jinja2'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('product', kwargs={'product_slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if request.user.is_authenticated:
            form.instance.user = request.user
            form.instance.item = self.object
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_review = form.save(commit=False)
        new_review.save()
        return super(GoodsDetailView, self).form_valid(form)



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
            return Product.objects.filter(category__name=category_name).select_related('category__parent', 'category').order_by('price')
        return Product.objects.select_related('category__parent', 'category').order_by('price')
