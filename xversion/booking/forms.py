from django import forms
from orders.models import UserOrderInfo
from django.contrib.auth.models import User


class IndexBookForm(forms.ModelForm):
    #lat = forms.DecimalField(max_digits=9, decimal_places=6)
    #lon = forms.DecimalField(max_digits=9, decimal_places=6)
    location = forms.CharField(widget=forms.TextInput(attrs={'id': 'loc'}), max_length=200)
    start = forms.CharField(widget=forms.TextInput(attrs={'id': 'start'}), max_length=50)
    end = forms.CharField(widget=forms.TextInput(attrs={'id': 'end'}), max_length=50)

    REQUIRED_FIELDS = ['location', 'start', 'end']

    class Meta:
        model = UserOrderInfo
        #fields = ['location']
        exclude = ('uid', 'mid', 'lat', 'lon')

