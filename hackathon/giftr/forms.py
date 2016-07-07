from django import forms
from django.contrib.auth.models import User
from .models import *
from .forms import *

class GiftForm(forms.ModelForm):
    """
    Form for adding a new gift
    """
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


class RegisterForm(forms.ModelForm):
    """
    Form for reguistering a new user
    """
    class Meta:
        model=User
        fields = ('email', 'password1', 'password2')
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data