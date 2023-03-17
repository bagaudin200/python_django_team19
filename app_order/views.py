from contextlib import suppress

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import FormView

from app_order.forms import OrderStepTwoForm, OrderStepThreeForm, OrderStepFourForm, OrderStepOneForm


class OrderStepOneView(FormView):
    form_class = OrderStepOneForm
    template_name = 'app_order/order_step_1.jinja2'

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        with suppress(ObjectDoesNotExist):
            my_group = Group.objects.get(name='Пользователи')
            my_group.user_set.add(user)
        login(request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('order_step_2'))
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('order_step_2')



class OrderStepTwoView(FormView):
    form_class = OrderStepTwoForm
    template_name = 'app_order/order_step_2.jinja2'

    def form_valid(self, form):
        self.request.session['delivery'] = form.cleaned_data['delivery_type']
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        return super().form_valid(request)

    def get_success_url(self):
        return reverse('order_step_3')



class OrderStepThreeView(FormView):
    form_class = OrderStepThreeForm
    template_name = 'app_order/order_step_3.jinja2'

    def form_valid(self, form):
        self.request.session = form.cleaned_data

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print('request', request)
        return super().form_valid(request)

    def get_success_url(self):
        return reverse('order_step_4')


class OrderStepFourView(FormView):
    form_class = OrderStepFourForm
    template_name = 'app_order/order_step_4.jinja2'

    def form_valid(self, form):
        self.request.session = form.cleaned_data
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('order_step_4')

