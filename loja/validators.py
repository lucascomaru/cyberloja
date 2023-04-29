from validate_docbr import CPF
from django.core.exceptions import ValidationError

def validar_cpf(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError("CPF inválido.")