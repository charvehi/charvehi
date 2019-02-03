from django import forms
from django.forms import ModelForm, Textarea
from review.models import Review

class ReviewForm(ModelForm):
    #rating = forms.IntegerField(widget=forms.TextInput(attrs={'id': 'reviewRating'}))
    comment = forms.CharField(widget=forms.TextInput(attrs={'id': 'reviewComment'}), max_length=200, required=True)

    REQUIRED_FIELDS = ['comment']

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 40, 'rows': 3})
        }
