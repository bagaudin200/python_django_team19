from django import forms
from .models import Reviews


class Reviewsform(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = ('comment',)


