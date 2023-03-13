from django import forms

from app_goods.models import Review


class FilterForm(forms.Form):
    price_from = forms.DecimalField()
    price_to = forms.DecimalField()
    name = forms.CharField()
    in_stock = forms.BooleanField()
    free_delivery = forms.BooleanField()


class Reviewsform(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('text',)