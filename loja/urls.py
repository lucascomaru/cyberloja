# url - #view - template

from django.urls import path, include
from.views import homepage, contato, detalhes_produto, carrinho, cadastrar_usuario, editar_perfil, recuperar_senha, logout_view, checkout, produtos_destaque,produtos_por_categoria
from django.contrib.auth.views import LoginView
from . import views



urlpatterns = [
    path('', views.produtos_destaque, name='produtos_destaque'),
    path('contato/', contato,name='contato'),
    path('produto/<int:produto_id>/', detalhes_produto, name='detalhes_produto'),
    path('carrinho/', carrinho, name='carrinho'),
    path('categoria/<str:categoria_nome>/', views.produtos_por_categoria, name='produtos_por_categoria'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
    path('logout/', logout_view, name='logout'),
    path('criar_conta/', cadastrar_usuario, name='criar_conta'),
    path('recuperar_senha/', recuperar_senha,name ='recuperar_senha'),
    path('accounts/profile/', views.profile, name='profile'),
    path('checkout/', checkout, name='checkout'),
    path('search/', views.search, name='search'),
    path('produtos/produtos_destaque', views.produtos_destaque, name='produtos_destaque')
]
