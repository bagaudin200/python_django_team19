from django import forms
from django.forms import TextInput, Textarea

from app_cart.models import Cart
from .models import Review


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
        widgets = {'text': Textarea(attrs={'class': 'form-textarea',
                                           'placeholder': "Review",
                                           'id': "review",
                                           }
                                    ),
                   }


class FilterForm(forms.Form):
    price_from = forms.DecimalField()
    price_to = forms.DecimalField()
    name = forms.CharField()
    in_stock = forms.BooleanField()
    free_delivery = forms.BooleanField()