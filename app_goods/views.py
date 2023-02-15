from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from app_goods.forms import Reviewsform
from app_goods.models import Items


class GoodsDetailView(FormMixin, DetailView):
    form_class = Reviewsform
    model = Items
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







