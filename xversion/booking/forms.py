from django import forms
from orders.models import UserOrderInfo
from django.contrib.auth.models import User


class IndexBookForm(forms.ModelForm):
    #lat = forms.DecimalField(max_digits=9, decimal_places=6)
    #lon = forms.DecimalField(max_digits=9, decimal_places=6)
    location = forms.CharField(widget=forms.TextInput(attrs={'id': 'loc'}), max_length=200)
    start_time = forms.CharField(widget=forms.TextInput(attrs={'class': 'time'}), max_length=50)
    end_time = forms.CharField(widget=forms.TextInput(attrs={'class': 'time'}), max_length=50)

    REQUIRED_FIELDS = ['location', 'start_date', 'start_time', 'end_date', 'end_time']

    class Meta:
        model = UserOrderInfo
        fields = ['location', 'start_date', 'end_date']
        exclude = ('uid', 'mid', 'lat', 'lon')

