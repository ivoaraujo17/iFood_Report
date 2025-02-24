from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'campo', 'placeholder': 'E-mail'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'campo', 'placeholder': 'Senha'})
    )
