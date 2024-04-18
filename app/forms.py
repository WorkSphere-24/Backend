from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
from django import forms

class SignUpForm(UserCreationForm):
    name = forms.CharField(label = "Name")
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)
    class Meta(UserCreationForm):
        model=CustomUser
        fields=['name','email']
        labels={'email':'Email' }

class EditUserProfileForm(UserChangeForm):
    password=None
    class Meta:
        model=CustomUser
        fields=['name','email','date_joined','last_login']
        labels={'email':'Email'}

class EditAdminProfileForm(UserChangeForm):
    password=None
    class Meta:
        model=CustomUser
        fields='__all__'
        labels={'email':'Email'}

class CustomLoginForm(AuthenticationForm):
    email=forms.EmailField(label='email',required=True)
    password=forms.CharField(max_length=255, required=True)