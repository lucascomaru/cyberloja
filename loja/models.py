from django.db import models
from django.contrib.auth.models import User



class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos')

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Carrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
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




