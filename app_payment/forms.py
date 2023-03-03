from django import forms


class PaymentForm(forms.Form):
    card_number = forms.CharField(
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
