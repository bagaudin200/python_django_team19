from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from .forms import PaymentForm
from .tasks import pay


class PaymentWithCardView(FormMixin, TemplateView):
    """Отображение шаблона оплаты заказа с карты"""
    form_class = PaymentForm
    template_name = 'app_payment/payment_with_card.jinja2'
    http_method_names = ['get', 'post']

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            pay(1, 22222222, 500).delay()
            return HttpResponseRedirect(reverse('goods:catalog'))


class PaymentFromSomeonesAccount(FormMixin, TemplateView):
    """Отображение шаблона оплаты с чужого счета"""
    form_class = PaymentForm
    template_name = 'app_payment/payment_someone.jinja2'


class ProgressPaymentView(TemplateView):
    template_name = 'app_payment/progressPayment.jinja2'
