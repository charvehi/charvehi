from django import forms
from orders.models import UserOrderInfo
from django.contrib.auth.models import User


class IndexBookForm(forms.ModelForm):
    #lat = forms.DecimalField(max_digits=9, decimal_places=6)
    #lon = forms.DecimalField(max_digits=9, decimal_places=6)
    location = forms.CharField(widget=forms.TextInput(attrs={'id': 'loc','class': 'form-control','placeholder':"Enter your location"}), max_length=200)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'startDate',
                                                               'aria-hidden': 'true','placeholder':"Start Date",'readonly':''}))
    start_time = forms.CharField(widget=forms.TextInput(attrs={'class': 'time start form-control', 'id': 'startTime','placeholder':"Start Time"}), max_length=50)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'endDate','placeholder':"End Date",'readonly':''}))
    end_time = forms.CharField(widget=forms.TextInput(attrs={'class': 'time end form-control', 'id': 'endTime','placeholder':"EndTime"}), max_length=50)

    REQUIRED_FIELDS = ['location', 'start_date', 'start_time', 'end_date', 'end_time']

    class Meta:
        model = UserOrderInfo
        fields = ['location', 'start_date', 'end_date']
        exclude = ('uid', 'mid', 'lat', 'lon')