from rest_framework import viewsets
from .serializers import ClientePFSerializer, ClientePJSerializer, ContaSerializer
from cliente import models


class ClientePFViewSet(viewsets.ModelViewSet):
    serializer_class = ClientePFSerializer
    queryset = models.ClientePF.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        print(user)

        queryset = models.ClientePF.objects.filter(usuario=user).first()

        return [queryset]


class ClientePJViewSet(viewsets.ModelViewSet):
    serializer_class = ClientePJSerializer
    queryset = models.ClientePJ.objects.all()
    
    

class ContaViewSet(viewsets.ModelViewSet):
    serializer_class = ContaSerializer
    queryset = models.Conta.objects.all()



