from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from app_order.forms import OrderForm


class OrderView(FormMixin, TemplateView):
    form_class = OrderForm
    template_name = 'app_order/order.jinja2'
