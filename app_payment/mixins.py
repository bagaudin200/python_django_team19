from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin

from app_payment.forms import PaymentForm


class PaymentMixin(FormMixin):
    form_class = PaymentForm
    http_method_names = ['get', 'post']

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('payment:progress_payment'))
        return render(request=self.request, template_name='app_payment/payment_with_card.jinja2',
                      context={'form': form})
