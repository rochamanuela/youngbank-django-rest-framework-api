from rest_framework import viewsets
from cliente.api import serializers
from cliente import models


class ClientePFViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientePFSerializer
    queryset = models.ClientePF.objects.all()


class ClientePJViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientePJSerializer
    queryset = models.ClientePJ.objects.all()