from django.shortcuts import render, redirect
from .models import Produto, Carrinho, LISTA_CATEGORIAS
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import  get_user_model, logout, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from .forms import RegistrationForm
from django.views import View
from .forms import CustomResetPasswordForm, CustomAuthenticationForm
from django.shortcuts import  get_object_or_404
import stripe
from django.conf import settings
from dotenv import load_dotenv
import os
from .models import UsuarioPersonalizado
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm




# Create your views here.
def homepage(request):
    return render(request, "homepage.html")

def contato(request):
    return render(request, "contato.html")

def detalhes_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    return render(request, 'detalhes_produto.html', {'produto': produto})

def carrinho(request):
    itens_do_carrinho = Carrinho.objects.filter(usuario=request.user)
    context = {'itens_do_carrinho': itens_do_carrinho}
    return render(request, 'carrinho.html', context)

def produtos_por_categoria(request, categoria_nome):
    categoria = None
    for cat in LISTA_CATEGORIAS:
        if cat[0] == categoria_nome:
            categoria = cat
            break

    if categoria:
        produtos = Produto.objects.filter(categoria=categoria[0])
    else:
        produtos = Produto.objects.none()

    context = {
        'categoria': categoria[1],
        'produtos': produtos,
    }
    return render(request, 'produtos_por_categoria.html', context)


    if categoria:
        produtos = Produto.objects.filter(categoria=categoria)
    else:
        produtos = Produto.objects.none()


    context = {
        'categoria': categoria,
        'produtos': produtos,
    }
    return render(request, 'produtos_por_categoria.html', context)

User = get_user_model()

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            cpf = form.cleaned_data.get('cpf')
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Este e-mail já está em uso.')
            elif UsuarioPersonalizado.objects.filter(cpf=cpf).exists():
                form.add_error('cpf', 'Este CPF já está em uso.')
            else:
                user = form.save(commit=False)
                user.usuario_personalizado.telefone = form.cleaned_data.get('telefone')
                user.usuario_personalizado.cpf = cpf
                user.usuario_personalizado.nome = form.cleaned_data.get('nome')
                user.save()
                user.usuario_personalizado.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return redirect('produtos_destaque')
    else:
        form = RegistrationForm()
    return render(request, 'criar_conta.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # login successful
            # redirect user to home page or some other page
            pass
    else:
        form = CustomAuthenticationForm(request)
    return render(request, 'login.html', {'form': form})
def profile(request):
    return render(request, 'homepage.html')
def logout_view(request):
    logout(request)
    return redirect('/')
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            if password and password != password_confirm:
                messages.error(request, 'As senhas não correspondem.')
            else:
                if password:
                    user.set_password(password)
                user.save()
                messages.success(request, 'Seu perfil foi atualizado com sucesso.')
                return redirect('editar_perfil')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'editar_perfil.html', {'form': form})



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

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def checkout(request):
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
        'STRIPE_PUBLIC_KEY': os.getenv('STRIPE_PUBLIC_KEY'), # Define a chave pública do Stripe como variável de ambiente
    })


    return render(request, 'checkout.html', {
        'session_id': checkout_session.id,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    })


def lista_produtos_recentes(request=None):
    lista_produtos = Produto.objects.all().order_by('-data_criacao')[0:9]
    if lista_produtos:
        produto_destaque = lista_produtos[0]
        lista_produtos = lista_produtos[1:]  # Exclui o produto_destaque da lista
    else:
        produto_destaque = None
    return {"lista_produtos_recentes": lista_produtos, "produto_destaque": produto_destaque}


def produtos_destaque(request):
    context = lista_produtos_recentes(request)
    return render(request, 'homepage.html', context)


def search(request):
    query = request.GET.get('q', '').lower()
    if query == 'tv' or query == 'televisão':
        query = 'televisão'

    produtos = Produto.objects.filter(nome__icontains=query)
    context = {
        'query': query,
        'produtos': produtos,
    }
    return render(request, 'search_results.html', context)





