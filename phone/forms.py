from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Payment



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = {'username', 'password'}

class Paymentform(ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'number', 'expiration', 'CVV']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'number': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'expiration': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'CVV': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }


