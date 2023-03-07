from django import forms
from django.core.exceptions import ValidationError

from .utils import card_number_is_valid


class PaymentForm(forms.Form):
    card_number = forms.CharField(
        min_length=9,  # 4 цифры, пробел, 4 цифры = 9 символов
        max_length=9,  # 4 цифры, пробел, 4 цифры = 9 символов
        widget=forms.TextInput(
            attrs={
                'class': 'form-input Payment-bill',
                'id': 'numero1',
                'name': 'numero1',
                'type': 'text',
                'placeholder': '9999 9999',
                'data-mask': '9999 9999',
                'data-validate': 'require pay',
            }
        )
    )

    def clean_card_number(self):
        data = self.cleaned_data['card_number']
        if not card_number_is_valid(data):
            raise ValidationError('Номер карты должен быть четным и не заканчиваться на 0')
        return data
