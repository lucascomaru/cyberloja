from django.shortcuts import render, redirect
from .models import Produto, Carrinho
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.sessions.backends.db import SessionStore
# Create your views here.
def homepage(request):
    return render(request, "homepage.html")

def contato(request):
    return render(request, "contato.html")

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos.html', {'produtos': produtos})

def carrinho(request):
    itens_do_carrinho = Carrinho.objects.filter(usuario=request.user)
    context = {'itens_do_carrinho': itens_do_carrinho}
    return render(request, 'carrinho.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['loggedin'] = True # Definindo a variável loggedin na sessão
            return redirect('homepage')
        else:
            error_message = 'Usuário ou senha incorretos'
    else:
        error_message = ''
    return render(request, 'login.html', {'error_message': error_message})
def my_view(request):
    if request.session.get('loggedin', False):
        # O usuário está logado, execute o código aqui
        pass
    else:
        # O usuário não está logado, redirecione para a página de login
        return redirect('login.html')


def cadastrar_usuario(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    phone = request.POST['phone']
    cpf = request.POST['cpf']

    user = User.objects.create_user(username=email, email=email, password=password)
    user.phone = phone
    user.cpf = cpf
    user.save()

    return redirect('login.html')

  return render(request, 'criar_conta.html')

@login_required
def editar_perfil(request):
  if request.method == 'POST':
    user = request.user
    email = request.POST['email']
    phone = request.POST['phone']
    password = request.POST['password']
    if email != user.email:
      user.email = email
      user.username = email
    if phone != user.phone:
      user.phone = phone
    if password:
      user.set_password(password)
    user.save()
    return redirect('homepage.html')

  return render(request, 'editar_perfil.html')





