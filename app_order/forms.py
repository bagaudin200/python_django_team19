from django import forms
from django.forms import TextInput, Textarea, RadioSelect

from app_order.models import Order
from app_users.forms import UserCreateForm


class OrderStepOneForm(UserCreateForm):
    """
    Форма для обработки первого шага заказа товара
    """
    pass


class OrderStepTwoForm(forms.ModelForm):
    """
    Форма для обработки второго шага заказа товара
    """
    class Meta:
        model = Order
        fields = ('delivery_type', 'city', 'address',)
        widgets = {
            'city': TextInput(attrs={'class': 'form-input'}),
            'address': Textarea(attrs={'class': 'form-textarea'}),
            'delivery_type': RadioSelect,
        }


class OrderStepThreeForm(forms.ModelForm):
    """
    Форма для обработки третьего заказа товара
    """
    class Meta:
        model = Order
        fields = ('payment_type',)
        widgets = {
            'payment_type': RadioSelect,
        }


class OrderStepFourForm(forms.ModelForm):
    """
    Форма для обработки четвертого шага заказа товара
    """
    class Meta:
        model = Order
        fields = ('delivery_type', 'city', 'address', 'payment_type',)
