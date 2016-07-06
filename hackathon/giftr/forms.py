from django import forms
from django.contrib.auth.models import User
from .models import *
from .forms import *

class GiftForm(forms.ModelForm):
    class Meta:
        model=Gift
        fields = ('picture', 'description', 'price', 'url','category','recipient_catetory')
    def clean(self):
        cleaned_data = super(GiftForm, self).clean()
        first_name = cleaned_data.get("category")
        last_name = cleaned_data.get("last_name")
        if first_name =='':
            raise forms.ValidationError("Must provide gift category")
        return cleaned_data