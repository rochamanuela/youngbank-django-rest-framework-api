from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from cliente.api import viewsets as clienteviewsets

route = routers.DefaultRouter()
route.register(r'cliente_pf', clienteviewsets.ClientePFViewSet, basename="ClientePF")
route.register(r'cliente_pj', clienteviewsets.ClientePJViewSet, basename="ClientePJ")
route.register(r'conta', clienteviewsets.ContaViewSet, basename="Conta")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(route.urls))
]
