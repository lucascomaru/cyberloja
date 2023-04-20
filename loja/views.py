from django.shortcuts import render, redirect
from .models import Produto, Carrinho
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import  get_user_model, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from .forms import RegistrationForm
from django.views import View
from .forms import CustomLoginForm, CustomResetPasswordForm
from django.shortcuts import render
import stripe
from django.conf import settings
from dotenv import load_dotenv
import os
from .models import Produto

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



def sair(request):
    logout(request)
    return redirect('homepage.html')


def cadastrar_usuario(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login.html')
    else:
        form = RegistrationForm()
    return render(request, 'criar_conta.html', {'form': form})

    return render(request, 'homepage.html')
def profile(request):
    return render(request, 'homepage.html')
def logout_view(request):
    logout(request)
    return redirect('/')

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


def recuperar_senha(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='password_reset_email.html',
                subject_template_name='password_reset_subject.txt',
            )
            return render(request, 'password_reset_done.html')
    else:
        form = PasswordResetForm()
    return render(request, 'recuperar_senha.html', {'form': form})


Usuario = get_user_model()

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomResetPasswordForm
    success_url = reverse_lazy('login')
    template_name = 'recuperar_senha_confirm.html'

class CustomResetPasswordView(View):
    def get(self, request, *args, **kwargs):
        form = CustomLoginForm()
        context = {'form': form}
        return render(request, 'recuperar_senha.html', context)

    def post(self, request, *args, **kwargs):
        form = CustomLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = Usuario.objects.filter(email=email).first()
            if user:
                form = PasswordResetForm({'email': user.email})
                if form.is_valid():
                    form.save(
                        request=request,
                        use_https=request.is_secure(),
                        token_generator=default_token_generator,
                        email_template_name='recuperar_senha_email.html',
                        subject_template_name='recuperar_senha_subject.txt',
                    )
                return redirect('recuperar_senha_sucesso')
        context = {'form': form}
        return render(request, 'recuperar_senha.html', context)

class CustomPasswordResetSuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'recuperar_senha_sucesso.html')

load_dotenv()

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY


    price = stripe.Price.create(
        unit_amount=1000,
        currency='brl',
        product='prod_NjXyNriQPULuwz',
    )


    checkout_session = stripe.checkout.Session.create(
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
        payment_method_types=['card', 'boleto'],
        line_items=[{
            'price': price.id,
            'quantity': 1,
        }],
        mode='payment',
    )


    return render(request, 'checkout.html', {
        'session_id': checkout_session.id,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    })

def home(request):
    products = Produto.objects.all()
    context = {'products': products}
    return render(request, 'homepage.html', context)





