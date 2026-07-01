from django.contrib import admin
from .models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'cidade', 'uf', 'tributacao', 'plano_tarefas']
    search_fields = ['nome', 'cnpj', 'cidade']
    list_filter = ['tributacao', 'plano_tarefas', 'uf']
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = [
        ('Dados principais', {
            'fields': ['nome', 'cnpj', 'tributacao', 'plano_tarefas']
        }),
        ('Endereco', {
            'fields': ['logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'cep']
        }),
        ('Contato', {
            'fields': ['telefone_whatsapp', 'email']
        }),
        ('Observacoes', {
            'fields': ['observacao']
        }),
        ('Controle', {
            'fields': ['criado_em', 'atualizado_em']
        }),
    ]
