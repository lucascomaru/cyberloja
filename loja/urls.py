# url - #view - template

from django.urls import path, include
from.views import homepage, contato, lista_produtos, carrinho, cadastrar_usuario, editar_perfil, recuperar_senha, logout_view, checkout
from django.contrib.auth.views import LoginView
from . import views



urlpatterns = [
    path('', homepage),
    path('contato/', contato,name='contato'),
    path('produtos/', lista_produtos, name='produtos'),
    path('carrinho/', carrinho, name='carrinho'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
    path('logout/', logout_view, name='logout'),
    path('criar_conta/', cadastrar_usuario, name='criar_conta'),
    path('recuperar_senha/', recuperar_senha,name ='recuperar_senha'),
    path('accounts/profile/', views.profile, name='profile'),
    path('checkout/', checkout, name='checkout'),
]
