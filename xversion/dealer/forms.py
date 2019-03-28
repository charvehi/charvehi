from django import forms
from django.contrib.auth.forms import UserChangeForm

from booking.models import CategoryModel
from .models import Dealer


class DealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = "__all__"

class EditDealerForm(forms.ModelForm):
    status = forms.BooleanField(required=False)

    class Meta:
        model = Dealer
        fields = {
            'status',
        }
        exclude = {
            'password'
        }

class EditModelForm(forms.ModelForm):
    status =forms.BooleanField(required=False)

    class Meta:
        model = CategoryModel
        fields = { 'status'}
        exclude = { 'password', }