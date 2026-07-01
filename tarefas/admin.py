from django.contrib import admin
from .models import Departamento, EmpresaTarefaAjuste, PlanoTarefa, PlanoTarefaItem, Tarefa, TipoTarefa


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    search_fields = ['nome']
    list_filter = ['ativo']
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = [
        ('Dados principais', {
            'fields': ['nome', 'descricao', 'ativo']
        }),
        ('Controle', {
            'fields': ['criado_em', 'atualizado_em']
        }),
    ]


@admin.register(TipoTarefa)
class TipoTarefaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    search_fields = ['nome']
    list_filter = ['ativo']
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = [
        ('Dados principais', {
            'fields': ['nome', 'descricao', 'ativo']
        }),
        ('Controle', {
            'fields': ['criado_em', 'atualizado_em']
        }),
    ]


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'departamento', 'tipo', 'periodicidade', 'ativo']
    search_fields = ['nome', 'departamento__nome', 'tipo__nome']
    list_filter = ['periodicidade', 'tipo_dia_vencimento', 'departamento', 'tipo', 'ativo']
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = [
        ('Dados principais', {
            'fields': ['nome', 'departamento', 'tipo', 'periodicidade', 'ativo']
        }),
        ('Vencimento recorrente', {
            'fields': ['tipo_dia_vencimento', 'dia_vencimento', 'meses_apos_competencia', 'inicio_competencia']
        }),
        ('Vencimento esporadico', {
            'fields': ['data_vencimento_esporadica']
        }),
        ('Observacoes', {
            'fields': ['observacao']
        }),
        ('Controle', {
            'fields': ['criado_em', 'atualizado_em']
        }),
    ]


class PlanoTarefaItemInline(admin.TabularInline):
    model = PlanoTarefaItem
    extra = 1
    autocomplete_fields = ['tarefa']
    readonly_fields = ['tipo_tarefa']
    fields = ['tarefa', 'tipo_tarefa', 'ativo', 'observacao']

    def tipo_tarefa(self, obj):
        if obj and obj.tarefa_id:
            return obj.tarefa.tipo
        return '-'

    tipo_tarefa.short_description = 'Tipo'


@admin.register(PlanoTarefa)
class PlanoTarefaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tributacao', 'padrao', 'ativo']
    search_fields = ['nome', 'descricao']
    list_filter = ['tributacao', 'padrao', 'ativo']
    readonly_fields = ['criado_em', 'atualizado_em']
    inlines = [PlanoTarefaItemInline]
    fieldsets = [
        ('Dados principais', {
            'fields': ['nome', 'tributacao', 'descricao', 'padrao', 'ativo']
        }),
        ('Origem', {
            'fields': ['baseado_em']
        }),
        ('Controle', {
            'fields': ['criado_em', 'atualizado_em']
        }),
    ]


@admin.register(EmpresaTarefaAjuste)
class EmpresaTarefaAjusteAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'tarefa', 'tipo_ajuste', 'ativo']
    search_fields = ['empresa__nome', 'empresa__cnpj', 'tarefa__nome']
    list_filter = ['tipo_ajuste', 'ativo', 'tarefa__tipo', 'tarefa__departamento']
    autocomplete_fields = ['empresa', 'tarefa']
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = [
        ('Dados principais', {
            'fields': ['empresa', 'tarefa', 'tipo_ajuste', 'ativo']
        }),
        ('Observacoes', {
            'fields': ['observacao']
        }),
        ('Controle', {
            'fields': ['criado_em', 'atualizado_em']
        }),
    ]
