from django.db import models
import random

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
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


def criar_numero_conta():
    while True:
        numero_conta = str(random.randint(100000, 999999))  
        if not Conta.objects.filter(numero=numero_conta).exists():
            return numero_conta

# ------------------------------------------------------------------------------------------
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=80, unique=False)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class ClientePF(models.Model):
    id_cliente_pf = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True, null=False, validators=[validate_cpf])
    rg = models.CharField(max_length=20)
    numero = models.CharField(max_length=20)
    usuario = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)


class ClientePJ(models.Model):
    id_cliente_pj = models.AutoField(primary_key=True)
    razao_social = models.CharField(max_length=255)
    data_abertura = models.DateField()
    cnpj = models.CharField(max_length=14, unique=True, null=False)
    numero = models.CharField(max_length=20)
    usuario = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    
    
class Conta(models.Model):
    id_conta = models.AutoField(primary_key=True)
    agencia = models.CharField(max_length=4)
    numero = models.CharField(max_length=35)
    tipo = models.CharField(max_length=20)
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    ativa = models.BooleanField(default=True)
    cliente_pf = models.ForeignKey(ClientePF, on_delete=models.CASCADE, related_name="cliente_pf_conta", null=True, blank=True)
    cliente_pj = models.ForeignKey(ClientePJ, on_delete=models.CASCADE, related_name="cliente_pj_conta", null=True, blank=True)


@receiver(post_save, sender=ClientePF)
def criar_conta_automatica_pf(sender, instance, created, **kwargs):
    if created:
        nova_conta = Conta.objects.create(
            agencia="0001",
            numero=criar_numero_conta(),
            tipo="Poupança",
            limite=500000.00,
            saldo=0,
            ativa=True,
            cliente_pf=instance
        )
        nova_conta.save()


@receiver(post_save, sender=ClientePJ)
def criar_conta_automatica_pj(sender, instance, created, **kwargs):
    if created:
        nova_conta = Conta.objects.create(
            agencia="0002",
            numero=criar_numero_conta(),
            tipo="Corrente",
            limite=900000.00,
            saldo=0,
            ativa=True,
            cliente_pj=instance
        )
        nova_conta.save()
        

class Cartao(models.Model):
    id_cartao = models.AutoField(primary_key=True)
    fk_conta = models.ForeignKey(Conta, on_delete=models.CASCADE, null=True)
    numero = models.CharField(max_length=16, null=True)
    validade = models.DateField(null=True)
    cvv = models.CharField(max_length=3, null=True)
    bandeira = models.CharField(max_length=20, null=True)
    situacao = models.CharField(max_length=10, null=True)
    limite = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    

class Emprestimo(models.Model):
    id_emprestimo = models.AutoField(primary_key=True)
    fk_conta = models.ForeignKey(Conta, on_delete=models.CASCADE, null=True)
    data_solicitacao = models.DateTimeField(auto_now=True, null=True)
    valor_solicitado = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    juros = models.DecimalField(decimal_places=2, max_digits=4, null=True)
    numero_parcelas = models.IntegerField(blank=True, null=True)
    valor_por_parcela = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    data_aprovacao = models.DateField(blank=True, null=True)


class Transferencia(models.Model):
    OPCOES_DE_TIPO = [
        ('conta', 'Conta'),
        ('cartao', 'Cartão de Crédito'),
    ]
    
    tipo = models.CharField(max_length=10, choices=OPCOES_DE_TIPO)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    conta_remetente = models.ForeignKey('Conta', on_delete=models.CASCADE, blank=True, null=True)
    cartao_remetente = models.ForeignKey('Cartao', on_delete=models.CASCADE, blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
    conta_destinatario = models.ForeignKey('Conta', on_delete=models.CASCADE, blank=True, null=True, related_name='destinatario')
    
    def __str__(self):
        return f"Transferência - Tipo: {self.tipo}, Valor: {self.valor}"