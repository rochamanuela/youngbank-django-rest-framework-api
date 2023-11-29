from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return False
    
    soma = 0
    peso = 10
    for i in range(9):
        soma += int(cpf[i]) * peso
        peso -= 1

    resto = soma % 11
    if resto < 2:
        digito_verificador1 = 0
    else:
        digito_verificador1 = 11 - resto

    if digito_verificador1 != int(cpf[9]):
        return False

    soma = 0
    peso = 11
    for i in range(10):
        soma += int(cpf[i]) * peso
        peso -= 1

    resto = soma % 11
    if resto < 2:
        digito_verificador2 = 0
    else:
        digito_verificador2 = 11 - resto

    if digito_verificador2 != int(cpf[10]):
        return False
    
    return True
    
# validação para o campo de inscricao_municipal
def validate_inscricao_municipal(value):
    if not value.isdigit() or len(value) != 11:
        raise ValidationError("O valor deve conter exatamente 11 dígitos numéricos.")

# validação para o campo de inscricao_estadual
def validate_inscricao_estadual(value):
    if not value.isdigit() or len(value) != 9:
        raise ValidationError("O valor deve conter exatamente 9 dígitos numéricos.")
    

class ClientePF(models.Model):
    id_cliente_pf = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True, null=False, validators=[validate_cpf])
    rg = models.CharField(max_length=20)
    numero = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=120)


class ClientePJ(models.Model):
    id_cliente_pj = models.AutoField(primary_key=True)
    razao_social = models.CharField(max_length=255)
    data_abertura = models.DateField()
    cnpj = models.CharField(max_length=14, unique=True, null=False)
    numero = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=120)