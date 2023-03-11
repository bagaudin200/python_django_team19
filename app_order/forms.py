from django import forms


class OrderForm(forms.Form):
    fio = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.PasswordInput()
    password2 = forms.PasswordInput()
    delivery_type = forms.RadioSelect()
    city = forms.CharField(required=True)
    address = forms.CharField(required=True)
    payment_type = forms.RadioSelect()
