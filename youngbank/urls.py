from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from cliente import viewsets as clienteviewsets

route = routers.DefaultRouter()
route.register(r'cliente_pf', clienteviewsets.ClientePFViewSet, basename="ClientePF")
route.register(r'cliente_pj', clienteviewsets.ClientePJViewSet, basename="ClientePJ")
route.register(r'conta', clienteviewsets.ContaViewSet, basename="Conta")
route.register(r'cartao', clienteviewsets.CartaoViewSet, basename="Cartao")
route.register(r'emprestimo', clienteviewsets.EmprestimoViewSet, basename="Emprestimo")
route.register(r'transferencia', clienteviewsets.TransferenciaViewSet, basename="Transferencia")
# route.register(r'transferencias', clienteviewsets.ListaTransferenciasView, basename='Transferencia')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(route.urls)),
    path('api/v1/auth/', include('djoser.urls.authtoken')),
    path('api/v1/auth/', include('djoser.urls')),
    # path('api/v1/transferencias/', clienteviewsets.ListaTransferenciasView.as_view(), name='lista_transferencias'),
]
