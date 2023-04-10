from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from app_cart.services import CartServices
from app_order.models import Order
from .mixins import PaymentMixin
from .tasks import pay


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
        card_number = request.session.get('card_number')
        message = pay.delay(order.id, card_number, order.total_price)
        request.session['payment_message'] = message.info
        del request.session['card_number']
        return HttpResponseRedirect(reverse('product:catalog'))
