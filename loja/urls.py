# url - #view - template

from django.urls import path, include
from.views import homepage, contato, lista_produtos, carrinho

urlpatterns = [
    path('', homepage),
    path('contato', contato),
    path('produtos/', lista_produtos, name='produtos'),
    path('carrinho/', carrinho, name='carrinho'),
]
