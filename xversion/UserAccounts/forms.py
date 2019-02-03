from  django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, \
    PasswordChangeForm

from dealer.models import Dealer

User = get_user_model()


class MyAuthenticationForm(AuthenticationForm):
   username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','name':'email or phone','placeholder':'Email Address or phone','id':'inputEmail'}),required=True)
   password =forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','id':'inputPassword','name':'password'}),required=True)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address','id':'uemail',}),required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'create password','id':'inputPassword1',}),required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'confirm password', 'id': 'inputpassword2', }), required=True)
    phone = forms.RegexField(regex=r'^[6-9]\d{9}$',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number', 'id': 'mobile', }), required=True)
    city= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Address','id':'address',}),required=True)
    class Meta:
        model = User
        fields = {
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'phone',
            'city',
            }
        exclude = {'username'}

    def save(self, commit=True):
        user = super(RegistrationForm,self).save(commit = False)
        user.username=self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']


        if commit:
            user.save()

        return user

class DealerRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'id': 'demail', }),
        required=True)
    phone = forms.RegexField(regex=r'^[6-9]\d{9}$', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter mobile number', 'id': 'dmobile', }), required=True)

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'create password', 'id': 'inputPassword1', }), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'confirm password', 'id': 'inputpassword2', }), required=True)
    dealer_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name', 'id': 'dname', }),
        )
    '''status = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-control', 'placeholder': 'your status of available', 'id': 'dstatus', }),
        )'''
    dealer_lat=forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'latitude', 'id': 'dlat', }),
        )
    dealer_lon=forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'longitude', 'id': 'dlon', }),
        )

    opentime=forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'open time', 'id': 'dopen', }),
        )
    closetime=forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'close time', 'id': 'dclose', }),
        )

    class Meta:
        model = User
        fields = {
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'phone',
            'city',
            'dealer_name',
            'status',
            'dealer_lat',
            'dealer_lon',
            'opentime',
            'closetime',

            }
        exclude = {'username','first_name','last_name','city','status'}

    def save(self, commit=True):
        user = super(DealerRegistrationForm,self).save(commit = False)
        user.username=self.cleaned_data['email']
        #user.first_name = self.cleaned_data['first_name']
        #user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        user.is_vendor = True




        if commit:
            user.save()
            dealer_name=self.cleaned_data['dealer_name']
            #status=self.cleaned_data['status'] if we want to get from dealer
            dealer_lat= self.cleaned_data['dealer_lat']
            dealer_lon=self.cleaned_data['dealer_lon']
            opentime=self.cleaned_data['opentime']
            closetime=self.cleaned_data['closetime']
            dealer = Dealer.objects.create(user=user,dealer_name=dealer_name,
                      status=True,dealer_lat=dealer_lat,dealer_lon=dealer_lon,opentime=opentime,closetime=closetime)




        return user


'''class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ( 'city', 'phone')
'''


class PasswordChangeForm(PasswordChangeForm):
    old_password= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'old password','id':'oldPassword'}) ,required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'new password', 'id': 'newPassword'}), required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'confirm new password', 'id': 'newconfirmPassword'}), required=True)


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Email Address', 'id': 'uemail'}) ,required=True)
    first_name=forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control','placeholder': 'First Name', 'id': 'uemail', }),required=True,)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control','placeholder': 'Last Name', 'id': 'uemail', }),required = True)
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Address', 'id': 'address', }),
        required=True)
    phone = forms.RegexField(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}$', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter mobile number', 'id': 'mobile', }), required=True)


    class Meta:
        model = User
        fields = {
            'email',
            'first_name',
            'last_name',
            'city',
            'phone',
        }
        exclude = {

        }
        #we can use exclude = {}
class NewPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(widget=forms.TextInput(
        attrs={'class':'form-control','placeholder': 'Email Address', 'id': 'email', }),required=True)
