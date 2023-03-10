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
            return HttpResponseRedirect(reverse('payment:progress_payment'))
        return render(request=self.request, template_name='app_payment/payment_with_card.jinja2',
                      context={'form': form})


class PaymentFromSomeonesAccount(FormMixin, TemplateView):
    """Отображение шаблона оплаты с чужого счета"""
    form_class = PaymentForm
    template_name = 'app_payment/payment_someone.jinja2'
    http_method_names = ['get', 'post']

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('payment:progress_payment'))
        return render(request=self.request, template_name='app_payment/payment_someone.jinja2',
                      context={'form': form})


class ProgressPaymentView(TemplateView):
    template_name = 'app_payment/progressPayment.jinja2'

    def get(self, request, *args, **kwargs):
        pay.delay(1, 2222222, 500)
        return HttpResponseRedirect(reverse('catalog'))
