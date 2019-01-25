from django import forms
from django.contrib.auth.forms import UserChangeForm

from booking.models import CategoryModel
from .models import Dealer


class DealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = "__all__"

class EditDealerForm(UserChangeForm):
    status = forms.BooleanField(required=False)

    class Meta:
        model = Dealer
        fields = {
        'status',
        
        }

class EditModelForm(UserChangeForm):
    status =forms.BooleanField(required=False)

    class Meta:
        model = CategoryModel
        fields = { 'status',}


