import re

from django import forms
from django.forms import TextInput, Textarea, RadioSelect

from app_order.models import Order
from app_users.forms import UserCreateForm


class OrderStepOneForm(UserCreateForm):
    pass


class OrderStepTwoForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('delivery_type', 'city', 'address',)
        widgets = {
            'city': TextInput(attrs={'class': 'form-input'}),
            'address': Textarea(attrs={'class': 'form-textarea'}),
            'delivery_type': RadioSelect,
        }

class OrderStepThreeForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('payment_type',)
        widgets = {
            'payment_type': RadioSelect,
        }


class OrderStepFourForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('delivery_type', 'city', 'address', 'payment_type',)
