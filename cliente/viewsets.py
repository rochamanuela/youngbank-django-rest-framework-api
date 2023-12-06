from rest_framework import viewsets
from .serializers import ClientePFSerializer, ClientePJSerializer, ContaSerializer, CartaoSerializer, EmprestimoSerializer
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
    
    def get_queryset(self):
        user = self.request.user
        print(user)

        queryset = models.ClientePJ.objects.filter(usuario=user).first()

        return [queryset]
    

class ContaViewSet(viewsets.ModelViewSet):
    serializer_class = ContaSerializer
    queryset = models.Conta.objects.all()

    def get_queryset(self):
        user = self.request.user
        print(user)
        
        cliente_pj = models.ClientePJ.objects.filter(usuario=user).first()
        cliente_pf = models.ClientePF.objects.filter(usuario=user).first()
        
        if cliente_pf:
            queryset = models.Conta.objects.filter(cliente_pf_id=cliente_pf.id_cliente_pf).first()
        
        elif cliente_pj:
            queryset = models.Conta.objects.filter(cliente_pj_id=cliente_pj.id_cliente_pj).first()

        return [queryset]


class CartaoViewSet(viewsets.ModelViewSet):
    serializer_class = CartaoSerializer
    queryset = models.Cartao.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        print(user)
        
        cliente_pj = models.ClientePJ.objects.filter(usuario=user).first()
        cliente_pf = models.ClientePF.objects.filter(usuario=user).first()
        
        if cliente_pf:
            queryset = models.Cartao.objects.filter(cliente_pf_id=cliente_pf.id_cliente_pf).first()
        
        elif cliente_pj:
            queryset = models.Cartao.objects.filter(cliente_pj_id=cliente_pj.id_cliente_pj).first()

        return [queryset]


class EmprestimoViewSet(viewsets.ModelViewSet):
    serializer_class = EmprestimoSerializer
    queryset = models.Emprestimo.objects.all()
    
    def get_queryset(self):
        user = self.request.user
        print(user)
        
        cliente_pj = models.ClientePJ.objects.filter(usuario=user).first()
        cliente_pf = models.ClientePF.objects.filter(usuario=user).first()
        
        if cliente_pf:
            queryset = models.Emprestimo.objects.filter(cliente_pf_id=cliente_pf.id_cliente_pf).first()
        
        elif cliente_pj:
            queryset = models.Emprestimo.objects.filter(cliente_pj_id=cliente_pj.id_cliente_pj).first()

        return [queryset]
    
