
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    cpf = forms.CharField(max_length=14, required=True)
    phone_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'cpf', 'phone_number', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label='Lembrar Usuário', required=False)

class RecuperarSenhaForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=255)

