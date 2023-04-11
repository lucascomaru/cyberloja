from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Obrigatório, Coloque um e-mail válido.')
    phone = forms.CharField(max_length=20, help_text='Obrigatório, Coloque um número válido.')
    cpf = forms.CharField(max_length=14, help_text='Obrigatório, Coloque um CPF válido.')

    class Meta:
        model = User
        fields = ('email', 'phone', 'cpf', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label='Lembrar Usuário', required=False)

Usuario = get_user_model()

class CustomLoginForm(forms.Form):
    email = forms.EmailField(label='Endereço de email')

class CustomResetPasswordForm(forms.Form):
    senha_nova = forms.CharField(
        label='Nova senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    senha_nova_confirmacao = forms.CharField(
        label='Confirmação de nova senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)

    def clean_senha_nova_confirmacao(self):
        senha_nova = self.cleaned_data.get('senha_nova')
        senha_nova_confirmacao = self.cleaned_data.get('senha_nova_confirmacao')

        if senha_nova and senha_nova_confirmacao and senha_nova != senha_nova_confirmacao:
            raise forms.ValidationError('As senhas não são iguais')
        return senha_nova_confirmacao

    def save(self):
        senha_nova = self.cleaned_data.get('senha_nova')
        self.user.set_password(senha_nova)
        self.user.save()


