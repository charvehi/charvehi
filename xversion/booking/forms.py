from django import forms
from booking.models import UserProfileInfo
from django.contrib.auth.models import User

class UserForm(forms.Form):
    lat = forms.DecimalField(max_digits=9, decimal_places=6)
    lon = forms.DecimalField(max_digits=9, decimal_places=6)

class Meta():
    model = User
    fields = ('lat', 'lon')


class UserProfileInfoForm(forms.Form):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_photos')