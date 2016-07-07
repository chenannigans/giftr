from django import forms
from django.contrib.auth.models import User
from models import *
from forms import *

from django.contrib.auth.models import User


class GiftForm(forms.ModelForm):
    """
    Form for adding a new gift
    """
    class Meta:
        model=Gift
        exclude = ('user',)
        # fields = ('photo', 'description', 'price', 'url','category','recipient_category')
        widgets = {'photo' : forms.FileInput() }
    def clean(self):
        cleaned_data = super(GiftForm, self).clean()
        price = cleaned_data.get("price")
        description = cleaned_data.get("description")
        if not 'description' in self.cleaned_data:
            raise forms.ValidationError("Description is required")
        if description == "":
            print "description error"
            raise forms.ValidationError("Description is required")
        if price < 0:
            print "price error"
            raise forms.ValidationError("Must provide valid price")
        return cleaned_data

class LoginForm(forms.ModelForm):
    """
    Form for user login
    """
    class Meta:
        model=User
        fields = ('username', 'password')
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username =='':
            raise forms.ValidationError("Must enter username")
        if password =='':
            raise forms.ValidationError("Must enter password")
        user = authenticate(username=username, password=password)
        if user is None:   
            raise forms.ValidationError("Invalid username and password") 
        return cleaned_data


class RegisterForm(forms.ModelForm):
    """
    Form for reguistering a new user
    """
    username = forms.CharField(widget=forms.TextInput(),label="Username", max_length=254)
    password1 = forms.CharField(widget=forms.PasswordInput(),
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(),
                                label="Password again")
    class Meta:
        model=User
        fields = ['username', 'password1', 'password2']
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get("username")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if username =='':
            raise forms.ValidationError("Must enter username")
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        if password1 =='':
            raise forms.ValidationError("Must enter password")
        if password2 =='':  
            raise forms.ValidationError("Must re-enter password")
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data
