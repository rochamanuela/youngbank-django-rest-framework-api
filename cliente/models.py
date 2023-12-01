from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
    
class Conta(models.Model):
    id_conta = models.AutoField(primary_key=True)
    agencia = models.CharField(max_length=4)
    numero = models.CharField(max_length=35)
    tipo = models.CharField(max_length=20)
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    ativa = models.BooleanField(default=True)
    cliente_pf = models.ForeignKey(ClientePF, on_delete=models.CASCADE, related_name="cliente_pf_conta", null=True)
    cliente_pj = models.ForeignKey(ClientePJ, on_delete=models.CASCADE, related_name="cliente_pj_conta", null=True)


# class ClientePFConta(models.Model):
#     fk_cliente = models.ForeignKey(ClientePF, on_delete=models.CASCADE)
#     fk_conta = models.ForeignKey(Conta, on_delete=models.CASCADE)


# class ClientePJConta(models.Model):
#     fk_cliente = models.ForeignKey(ClientePJ, on_delete=models.CASCADE)
#     fk_conta = models.ForeignKey(Conta, on_delete=models.CASCADE)


@receiver(post_save, sender=ClientePF)
def criar_conta_automatica_pf(sender, instance, created, **kwargs):
    if created:
        nova_conta = Conta.objects.create(
            agencia="1234",
            numero="567890",
            tipo="Poupança",
            limite=1000.00,
            ativa=True,
            cliente_pf=instance
        )
        nova_conta.save()


@receiver(post_save, sender=ClientePJ)
def criar_conta_automatica_pj(sender, instance, created, **kwargs):
    if created:
        nova_conta = Conta.objects.create(
            agencia="1234",
            numero="567890",
            tipo="Corrente",
            limite=1000.00,
            ativa=True,
            cliente_pj=instance
        )
        nova_conta.save()
        

class Cartao(models.Model):
    id_cartao = models.AutoField(primary_key=True)
    fk_conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    numero = models.CharField(max_length=16)
    validade = models.DateField()
    cvv = models.CharField(max_length=3)
    bandeira = models.CharField(max_length=20)
    situacao = models.CharField(max_length=10)
    

class Emprestimo(models.Model):
    id_emprestimo = models.AutoField(primary_key=True)
    fk_conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    data_solicitacao = models.DateTimeField(auto_now=True)
    valor_solicitado = models.DecimalField(decimal_places=2, max_digits=6)
    juros = models.DecimalField(decimal_places=2, max_digits=4)
    aprovado = models.BooleanField(default=False)
    numero_parcelas = models.IntegerField(blank=True)
    data_aprovacao = models.DateField(blank=True)


class EmprestimoParcela(models.Model):
    id_parcela = models.AutoField(primary_key=True)
    fk_emprestimo = models.ForeignKey(Emprestimo, on_delete=models.CASCADE)
    numero = models.CharField(max_length=60)
    data_vencimento = models.DateField()
    valor_parcela = models.DecimalField(decimal_places=2, max_digits=6)
    data_pagamento = models.DateTimeField(blank=True)
    valor_pago = models.DecimalField(blank=True, decimal_places=2, max_digits=6)

