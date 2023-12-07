from rest_framework import viewsets, status, generics
from .serializers import ClientePFSerializer, ClientePJSerializer, ContaSerializer, CartaoSerializer, EmprestimoSerializer, TransferenciaSerializer
from cliente import models
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q


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
    

class TransferenciaViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, requisicao):
        valor = Decimal(requisicao.data.get('valor', 0))
        email_destinatario = requisicao.data.get('email_destinatario')
        tipo_transferencia = requisicao.data.get('tipo_transferencia', 'Pix')

        if valor > 0 and email_destinatario:
            conta_remetente = get_object_or_404(models.Conta, cliente_pf=requisicao.user.clientepf)
            usuario_destinatario = get_object_or_404(models.User, email=email_destinatario)
            conta_destinatario = get_object_or_404(models.Conta, cliente_pf=usuario_destinatario.clientepf)

            if conta_remetente.saldo >= valor:
                conta_remetente.saldo -= valor
                conta_remetente.save()

                conta_destinatario.saldo += valor
                conta_destinatario.save()

                operacao = tipo_transferencia.capitalize()

                dados_transacao_remetente = {
                    'conta': conta_remetente.cliente_pf,
                    'tipo_transferencia': 'Pix enviado',
                    'tipo_operacao': operacao,
                    'valor': valor
                }

                dados_transacao_destinatario = {
                    'conta': conta_destinatario.cliente_pf,
                    'tipo_transferencia': 'Pix recebido',
                    'tipo_operacao': operacao,
                    'valor': valor
                }

                for dados_transacao in [dados_transacao_remetente, dados_transacao_destinatario]:
                    serializer_transacao = TransferenciaSerializer(data=dados_transacao)
                    serializer_transacao.is_valid(raise_exception=True)
                    serializer_transacao.save()

                return Response({'sucesso': 'Transferencia realizada com sucesso'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'erro': 'Saldo insuficiente na conta do remetente'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'erro': 'Valores invalidos para a transferencia'}, status=status.HTTP_400_BAD_REQUEST)


# essa parte está comentada pois começou a dar muito erro
# class ListaTransferenciasView(generics.ListAPIView):
#     serializer_class = TransferenciaSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['tipo_transferencia']

#     def get_queryset(self):
#         user = self.request.user
#         return models.Transferencia.objects.filter(Q(account__cliente_pf=user.cliente_pf) | Q(account_destinatario__cliente_pf=user.clientepf))