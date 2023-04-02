from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from app_order.models import Order
from app_cart.services import CartServices
from .tasks import pay
from .mixins import PaymentMixin


class PaymentWithCardView(PaymentMixin, TemplateView):
    """Отображение шаблона оплаты заказа с карты"""
    template_name = 'app_payment/payment_with_card.jinja2'


class PaymentFromSomeonesAccount(PaymentMixin, TemplateView):
    """Отображение шаблона оплаты с чужого счета"""
    template_name = 'app_payment/payment_someone.jinja2'


class ProgressPaymentView(TemplateView):
    template_name = 'app_payment/progressPayment.jinja2'

    def get(self, request, *args, **kwargs):
        cart = CartServices(request)
        order = Order.objects.get(cart=cart.cart)
        pay.delay(order.id, 22222222, order.total_price)
        return HttpResponseRedirect(reverse('catalog'))
