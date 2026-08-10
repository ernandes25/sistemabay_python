from django.contrib import admin
from .models import Empresa, Organizacao


@admin.register(Organizacao)
class OrganizacaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'documento', 'email', 'telefone_whatsapp', 'ativa']
    search_fields = ['nome', 'documento', 'email']
    list_filter = ['ativa']
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = [
        ('Dados principais', {
            'fields': ['nome', 'documento', 'ativa']
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


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'organizacao', 'cnpj', 'cidade', 'uf', 'tributacao', 'plano_tarefas']
    search_fields = ['nome', 'cnpj', 'cidade']
    list_filter = ['organizacao', 'tributacao', 'plano_tarefas', 'uf']
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = [
        ('Dados principais', {
            'fields': ['organizacao', 'nome', 'cnpj', 'tributacao', 'plano_tarefas']
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
