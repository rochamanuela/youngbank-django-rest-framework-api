from rest_framework import serializers
from cliente import models
from rest_framework.exceptions import ValidationError

from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from requests import request
import random, string

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = models.User(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
    

class ClientePFSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientePF
        fields = '__all__'
    
    def create(self, validated_data):
        usuario_logado = self.context['request'].user
        
        if models.ClientePJ.objects.filter(usuario=usuario_logado).first() or models.ClientePF.objects.filter(usuario=usuario_logado).first():
            raise ValidationError("Este usuário já possui um cliente associado.", code='invalid')

        cliente = models.ClientePF.objects.create(usuario=usuario_logado, **validated_data)

        return cliente
        

class ClientePJSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientePJ
        fields = '__all__'
        
    def create(self, validated_data):
        usuario_logado = self.context['request'].user
        
        if models.ClientePJ.objects.filter(usuario=usuario_logado).first() or models.ClientePF.objects.filter(usuario=usuario_logado).first():
            raise ValidationError("Este usuário já possui um cliente associado.", code='invalid')
        cliente = models.ClientePJ.objects.create(usuario=usuario_logado, **validated_data)

        return cliente

class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conta
        fields = '__all__'


def generate_random_number():
    return ''.join(random.choices(string.digits, k=16))

def generate_random_cvv():
    return ''.join(random.choices(string.digits, k=3))  


class CartaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cartao
        fields = '__all__'
        
    def create(self, validated_data):
        usuario_logado = self.context['request'].user
        
        cliente_pj = models.ClientePJ.objects.filter(usuario=usuario_logado).first()
        cliente_pf = models.ClientePF.objects.filter(usuario=usuario_logado).first()
        
        if cliente_pf:
            conta_existente = models.Conta.objects.filter(cliente_pf=cliente_pf.id_cliente_pf).first()
            
        if cliente_pj:
            conta_existente = models.Conta.objects.filter(cliente_pj=cliente_pj.id_cliente_pj).first()
        
        try:
            
            if conta_existente.saldo >= 1000:
                novo_cartao = models.Cartao.objects.create(
                    fk_conta = conta_existente,
                    numero = generate_random_number(),
                    validade = '2025-12-30',
                    cvv = generate_random_cvv(),
                    bandeira = 'Martercard',
                    situacao = 'ativo',
                    limite = 1000
                )
                conta_existente.save()
                return novo_cartao
            
            else:
                raise ValidationError("É necessário ter saldo igual ou superior a 1000 reais para possuir cartao de credito.", code='invalid')

        except models.Conta.DoesNotExist:
            return Response({'error': 'Conta não encontrada'}, status=status.HTTP_404_NOT_FOUND)

    
class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Emprestimo
        fields = '__all__'
        
    def create(self, validated_data):
        usuario_logado = self.context['request'].user
        valor_emprestimo = validated_data['valor_solicitado']
        parcelas_emprestimo = validated_data['numero_parcelas']
        
        cliente_pj = models.ClientePJ.objects.filter(usuario=usuario_logado).first()
        cliente_pf = models.ClientePF.objects.filter(usuario=usuario_logado).first()
        
        if cliente_pf:
            conta_existente = models.Conta.objects.filter(cliente_pf=cliente_pf.id_cliente_pf).first()
            
        if cliente_pj:
            conta_existente = models.Conta.objects.filter(cliente_pj=cliente_pj.id_cliente_pj).first()
        
        try:
            
            def calcular_parcelas_com_juros():
                valor_por_parcela = (float(valor_emprestimo) * 1.05) / parcelas_emprestimo
                return valor_por_parcela
            
            if conta_existente.saldo >= 2500:
                novo_emprestimo = models.Emprestimo.objects.create(
                    fk_conta = conta_existente,
                    data_solicitacao = timezone.now(),
                    valor_solicitado = valor_emprestimo,
                    juros = 0.05,
                    numero_parcelas = parcelas_emprestimo,
                    valor_por_parcela = calcular_parcelas_com_juros(),
                    data_aprovacao = timezone.now().date()
                )
                conta_existente.save()
                return novo_emprestimo
            
            else:
                raise ValidationError("É necessário ter saldo igual ou superior a 2500 reais para que o empréstimo seja aprovado.", code='invalid')

        except models.Conta.DoesNotExist:
            return Response({'error': 'Conta não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        
class TransferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transferencia
        fields = '__all__'
        
    def create(self, validated_data):
        transferencia = models.Transferencia.objects.create(**validated_data)
        return transferencia