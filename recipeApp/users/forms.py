from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from recipeApp.users.models import Profile


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_info', 'profile_picture']

# class UserProfileForm(forms.Form):
#     profile_info = forms.CharField(widget=forms.Textarea, required=False)
#     file = forms.ImageField(required=False)
