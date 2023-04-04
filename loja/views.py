from django.shortcuts import render
from .models import Produto, Carrinho
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