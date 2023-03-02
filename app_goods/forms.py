from django import forms
from django.forms import TextInput

from app_cart.models import Cart
from app_goods.models import Review


class AddProductToCardForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('quantity',)

        widgets = {
            'quantity': TextInput(attrs={'class': 'Amount-input form-input',
                                         'value': "1"
                                         }
                                  ),
        }


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text',)
