from django import forms
from orders.models import UserOrderInfo
from django.contrib.auth.models import User


class IndexBookForm(forms.ModelForm):
    #lat = forms.DecimalField(max_digits=9, decimal_places=6)
    #lon = forms.DecimalField(max_digits=9, decimal_places=6)
    location = forms.CharField(max_length=100)
    start = forms.CharField(max_length=50)
    end = forms.CharField(max_length=50)

    REQUIRED_FIELDS = ['location', 'start', 'end']

    class Meta:
        model = UserOrderInfo
        fields = ['location']

