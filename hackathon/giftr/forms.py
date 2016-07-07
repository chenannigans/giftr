from django import forms
from django.contrib.auth.models import User
from .models import *
from .forms import *

from django.contrib.auth.models import User


class GiftForm(forms.ModelForm):
    """
    Form for adding a new gift
    """
    class Meta:
        model=Gift
        fields = ('picture', 'description', 'price', 'url','category','recipient_category')
    def clean(self):
        cleaned_data = super(GiftForm, self).clean()
        first_name = cleaned_data.get("category")
        last_name = cleaned_data.get("last_name")
        if first_name =='':
            raise forms.ValidationError("Must provide gift category")
        return cleaned_data

class LoginForm(forms.ModelForm):
    """
    Form for user login
    """
    class Meta:
        model=User
        fields = ('email', 'password')
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if first_name =='':
            raise forms.ValidationError("Must provide gift category")
        return cleaned_data


class RegisterForm(forms.ModelForm):
    """
    Form for reguistering a new user
    """
    email = forms.EmailField(widget=forms.EmailInput(),label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput(),
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(),
                                label="Password (again)")
    class Meta:
        model=User
        fields = ['email', 'password1', 'password2']
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            print self.cleaned_data['password1']
            print self.cleaned_data['password2']
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                print "THEY DONT MATCH YO"
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data