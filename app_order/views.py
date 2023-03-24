from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView, FormMixin

from app_users.views import MyRegistration
from .forms import OrderStepTwoForm, OrderStepThreeForm, OrderStepFourForm, OrderStepOneForm
from .models import Order
from app_cart.models import Cart

user = get_user_model()

class OrderStepOneView(MyRegistration):
    template_name = 'app_order/order_step_1.jinja2'
    success_url = reverse_lazy('order:order_step_2')

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('order:order_step_2'))
        return super().post(request, *args, **kwargs)


class OrderStepTwoView(FormView):
    form_class = OrderStepTwoForm
    template_name = 'app_order/order_step_2.jinja2'

    def form_valid(self, form):
        self.request.session['delivery'] = form.cleaned_data['delivery_type']
        self.request.session['city'] = form.cleaned_data['city']
        self.request.session['address'] = form.cleaned_data['address']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('order:order_step_3')


class OrderStepThreeView(FormView):
    form_class = OrderStepThreeForm
    template_name = 'app_order/order_step_3.jinja2'

    def form_valid(self, form):
        self.request.session['payment'] = form.cleaned_data['payment_type']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('order:order_step_4')


class OrderStepFourView(ListView):
    model = Cart
    paginate_by = 5
    template_name = 'app_order/order_step_4.jinja2'

    '''При добавлении корзины, методы будут настроен в соответствии с новыми моделями и сервисами корзины'''
    # def get_queryset(self):
    #     # queryset = CardInProduct.objects.filter(card=Cart)
    #     return queryset

    # def post(self, request, *args, **kwargs):
    #     cart = Cart.objects.get(user=request.user)
    #     try:
    #         Order.objects.create(
    #             delivery_type = request.session['delivery'],
    #             city=request.session['city'],
    #             address=request.session['address'],
    #             payment_type=request.session['payment'],
    #             cart=cart,
    #             total_price=###
    #         )
    #     except:
    #         messages.error(request, "Проблемы на сервере, попробуйте ещё раз")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivery'] = Order.DELIVERY_TYPES_DICT[self.request.session['delivery']]
        context['payment'] = Order.PAYMENT_TYPES_DICT[self.request.session['payment']]
        context['user_phone'] = '+7 ({}{}{}) {}{}{}-{}{}-{}{}'.format(
            self.request.user.phoneNumber[0],
            self.request.user.phoneNumber[1],
            self.request.user.phoneNumber[2],
            self.request.user.phoneNumber[3],
            self.request.user.phoneNumber[4],
            self.request.user.phoneNumber[5],
            self.request.user.phoneNumber[6],
            self.request.user.phoneNumber[7],
            self.request.user.phoneNumber[8],
            self.request.user.phoneNumber[9],
        )
        return context


class OrderListView(ListView):
    model = Order
    template_name = 'app_order/history.jinja2'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'app_order/detail_order.jinja2'

