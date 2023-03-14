from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from app_order.forms import OrderForm
from app_users.forms import UserCreateForm


class OrderView(FormMixin, TemplateView):
    form_class = OrderForm
    template_name = 'app_order/order.jinja2'
    success_url = 'order'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreateForm()
        return context


def user_order(request):
    if request.method == 'POST':
        print('request', request)