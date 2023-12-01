from rest_framework import serializers
from cliente import models

class ClientePFSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientePF
        fields = '__all__'


class ClientePJSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientePJ
        fields = '__all__'
        

class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conta
        fields = '__all__'



        
        
class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Emprestimo
        fields = '__all__'


class EmprestimoParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmprestimoParcela
        fields = '__all__'