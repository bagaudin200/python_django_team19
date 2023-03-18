from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from app_order.forms import OrderForm
from app_order.models import Order


class OrderView(FormMixin, TemplateView):
    form_class = OrderForm
    template_name = 'app_order/order.jinja2'


class OrderListView(ListView):
    model = Order
    template_name = 'app_order/history.jinja2'
    context_object_name = 'orders'



class OrderDetailView(DetailView):
    model = Order
    template_name = 'app_order/detail_order.jinja2'

