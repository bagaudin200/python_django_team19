from django import forms


class OrderSettingForm(forms.Form):
    min_order_price_for_free_shipping = forms.IntegerField(min_value=100, max_value=100000)
    standard_order_price = forms.IntegerField(min_value=100, max_value=1000)
    express_order_price = forms.IntegerField(min_value=100, max_value=5000)

