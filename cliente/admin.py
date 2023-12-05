from django.contrib import admin
from .models import Conta, ClientePF, ClientePJ, User, Cartao, Emprestimo
# Register your models here.



@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('agencia', 'numero', 'tipo', 'limite', 'saldo', 'ativa', 'cliente_pf', 'cliente_pj', 'id_conta' )
    


@admin.register(ClientePF)
class ClientePFAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_nascimento', 'cpf', 'rg', 'numero', 'usuario')



@admin.register(ClientePJ)
class ClientePJAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_abertura', 'cnpj', 'razao_social', 'numero')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =('email', 'username')






