from django import forms
from .models import Review


class Reviewsform(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('text',)


