from django import template

register = template.Library()

@register.filter
def total_carrinho(itens):
    total = sum(item.produto.preco * item.quantidade for item in itens)
    return '{:.2f}'.format(total)
