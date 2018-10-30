from django import forms
from uaccounts.models import UserProfileInfo
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from localflavor.in_.forms import *

'''class PhoneModel(forms.Form):
    phone_regex = RegexValidator(regex=r'^d{6,10}$', message="Invalid number.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=10) # validators should be a list

class Gender(forms.Form):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.CharField(max_length=1, default=0)
'''

class UserForm(forms.ModelForm):
    #name = forms.CharField(max_length=60)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    #phone_regex = RegexValidator(regex=r'^d{6,10}$', message="Invalid number.")
    mobile = INZipCodeField(required=False)
    #gender = Gender
    #dob = forms.DateField(label='Birthday: ', initial="1990-06-21")
    #lat = forms.DecimalField(max_digits=9, decimal_places=6)
    #lon = forms.DecimalField(max_digits=9, decimal_places=6)

    class Meta():
        model = User
        fields = ('email', 'password')
        #db_table = 'uaccounts_userprofileinfo'


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('email', 'password')
        #db_table = 'uaccounts_userprofileinfo'
