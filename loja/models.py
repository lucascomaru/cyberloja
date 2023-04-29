from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.utils import timezone
from .validators import validar_cpf
from django.conf import settings

LISTA_CATEGORIAS = (
    ("ELETRONICOS", "Eletrônicos"),
    ("UTILIDADES_DOMESTICAS", "Utilidades Domésticas"),
    ("LAZER", "Lazer"),
    ("OUTROS", "Outros"),
)

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos')
    categoria = models.CharField(max_length=21, choices=LISTA_CATEGORIAS, default='OUTROS')
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class UsuarioPersonalizado(AbstractUser):
    telefone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Telefone')
    cpf = models.CharField(max_length=14, validators=[validar_cpf], verbose_name='CPF')

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user_permissions',
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username

class Carrinho(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'

class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto)
    valor_total = models.DecimalField(max_digits=6, decimal_places=2)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.usuario.username} - {self.valor_total}'

class PrecoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade_minima = models.IntegerField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.produto.nome} - {self.quantidade_minima} unidades ou mais'

class EstoqueProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    def __str__(self):
        return f'{self.produto.nome} - {self.quantidade} unidades em estoque'

class DescontoQuantidade(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade_minima = models.IntegerField()
    desconto = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return f'{self.produto.nome} - {self.desconto}% de desconto para {self.quantidade_minima} unidades ou mais'




