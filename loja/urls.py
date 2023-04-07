# url - #view - template

from django.urls import path, include
from.views import homepage, contato, lista_produtos, carrinho, cadastrar_usuario, editar_perfil
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', homepage),
    path('contato/', contato),
    path('produtos/', lista_produtos, name='produtos'),
    path('carrinho/', carrinho, name='carrinho'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
    path('logout/', auth_views.LogoutView.as_view(next_page=''), name='logout'),
    path('criar_conta/', cadastrar_usuario, name='criar_conta'),
]
