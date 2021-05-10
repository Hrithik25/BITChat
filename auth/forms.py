from django.contrib.auth.forms import UserCreationForm # Form for creating user
from django.contrib.auth.models import User
from django import forms


class SignupForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2') # Fields will appear in this order in signup form