from django import forms
from django.forms import TextInput, Textarea

from app_cart.models import ProductInCart
from .models import Review


class AddProductToCardForm(forms.ModelForm):
    """
    Форма для добавления товара в корзину
    """
    class Meta:
        model = ProductInCart
        fields = ('quantity',)
        widgets = {
            'quantity': TextInput(attrs={'class': 'Amount-input form-input',
                                         'value': "1"
                                         }
                                  ),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            quantity = 1
        return quantity


class ReviewsForm(forms.ModelForm):
    """
    Форма для добавления комментария к товару
    """
    class Meta:
        model = Review
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'class': 'form-textarea',
                                    'placeholder': 'Review',
                                    'id': 'review',
                                    }
                             ),
        }


class FilterForm(forms.Form):
    price_from = forms.DecimalField()
    price_to = forms.DecimalField()
    name = forms.CharField()
    in_stock = forms.BooleanField()
    free_delivery = forms.BooleanField()
