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