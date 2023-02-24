from django import forms


class FilterForm(forms.Form):
    price_from = forms.DecimalField()
    price_to = forms.DecimalField()
    name = forms.CharField()
    in_stock = forms.BooleanField()
    free_delivery = forms.BooleanField()
