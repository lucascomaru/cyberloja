from django import forms
class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label='Lembrar Usuário', required=False)