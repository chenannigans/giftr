from django import forms
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.forms.utils import flatatt
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.html import format_html, format_html_join
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
from collections import OrderedDict

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20)
    email = forms.EmailField(
        widget=forms.EmailInput)
    age = forms.CharField(max_length = 2)
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    password1 = forms.CharField(max_length = 200,
                                label='Password',
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                label='Confirm Password',
                                widget = forms.PasswordInput())
    bio = forms.CharField(max_length = 420)
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already Taken.")
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("email is already Taken.")
        return email
    def clean_age(self):
        age = self.cleaned_data.get("age")
        if not age.isdigit():
            raise forms.ValidationError("Age must be number")
        return age

class EditProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ('first_name', 'last_name')
    def clean(self):
        cleaned_data = super(EditProfileForm, self).clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if first_name =='' or last_name =='':
            raise forms.ValidationError("Must provide full name")
        return cleaned_data

class EditProfileForm2(forms.ModelForm):
    class Meta:
        model=Profile
        exclude = ('user',)
        widgets= {'picture': forms.FileInput()}
    def clean(self):
        cleaned_data = super(EditProfileForm2, self).clean()
        return cleaned_data
    def clean_age(self):
        cleaned_data = super(EditProfileForm2, self).clean()
        age = self.cleaned_data.get("age")
        if not age.isdigit():
            raise forms.ValidationError("Age must be number")
        return age

class RegistrationForm2(forms.ModelForm):
    class Meta:
        model=Profile
        exclude = ('user','bio','age')
        widgets= {'picture': forms.FileInput()}

class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        exclude = ('user',)
    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        return cleaned_data
