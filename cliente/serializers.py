from rest_framework import serializers
from cliente import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = models.User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
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

        seu_modelo = models.ClientePF.objects.create(usuario=usuario_logado, **validated_data)

        return seu_modelo
        
        


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