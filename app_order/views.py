from django.views.generic import ListView

from app_goods.models import Product
from app_users.forms import UserCreateForm


class OrderView(ListView):
    template_name = 'app_order/order.jinja2'
    queryset = Product

    def post(self, request):
        print(request.POST)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserCreateForm()
        return context





