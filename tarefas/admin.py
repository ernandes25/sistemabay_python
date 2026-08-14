from django.contrib import admin
from django import forms
from .models import (
    Departamento,
    EmpresaTarefaAjuste,
    OcorrenciaTarefa,
    PlanoTarefa,
    PlanoTarefaItem,
    Tarefa,
    TipoTarefa,
)


class TarefaPrincipalSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)

        if value and hasattr(value, 'instance'):
            option['attrs']['data-departamento'] = value.instance.departamento_id

        return option


class TarefaAdminForm(forms.ModelForm):
    CAMPOS_EXECUCAO_INTERNA = [
        'controla_execucao',
        'tipo_dia_execucao',
        'dia_execucao',
        'meses_apos_competencia_execucao',
        'ajuste_dia_execucao_nao_util',
        'dias_antecedencia_alerta_execucao',
    ]
    CAMPOS_VENCIMENTO_RECORRENTE = [
        'tipo_dia_vencimento',
        'dia_vencimento',
        'meses_apos_competencia',
        'ajuste_dia_nao_util',
        'dias_antecedencia_alerta',
        'inicio_competencia',
    ]

    class Meta:
        model = Tarefa
        fields = '__all__'
        widgets = {
            'tarefa_principal': TarefaPrincipalSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tarefa_principal'].queryset = Tarefa.objects.filter(
            natureza=Tarefa.Natureza.PRINCIPAL,
            ativo=True,
        ).order_by('departamento__nome', 'nome')

        natureza = self.data.get('natureza') if self.data else self.instance.natureza

        if natureza != Tarefa.Natureza.PRINCIPAL:
            for campo in self.CAMPOS_EXECUCAO_INTERNA:
                self.fields[campo].disabled = True
                self.fields[campo].help_text = 'Usado somente em tarefa principal.'

        if natureza == Tarefa.Natureza.PRINCIPAL:
            for campo in self.CAMPOS_VENCIMENTO_RECORRENTE:
                self.fields[campo].disabled = True
                self.fields[campo].help_text = 'Usado em tarefa simples ou subtarefa.'


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['organizacao', 'nome', 'ativo']
    list_display_links = ['nome']
    search_fields = ['organizacao__nome', 'nome']
    list_filter = ['organizacao', 'ativo']
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = [
        ('Dados principais', {
            'fields': ['organizacao', 'nome', 'descricao', 'ativo']
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
    form = TarefaAdminForm
    list_display = [
        'nome',
        'natureza',
        'departamento',
        'tipo',
        'periodicidade',
        'tarefa_principal',
        'controla_execucao',
        'dias_antecedencia_alerta',
        'ativo',
    ]
    search_fields = ['nome', 'tarefa_principal__nome', 'departamento__nome', 'tipo__nome']
    list_filter = [
        'natureza',
        'periodicidade',
        'controla_execucao',
        'tipo_dia_vencimento',
        'ajuste_dia_nao_util',
        'departamento',
        'tipo',
        'ativo',
    ]
    readonly_fields = ['criado_em', 'atualizado_em']
    fieldsets = [
        ('Dados principais', {
            'fields': ['nome', 'natureza', 'departamento', 'tipo', 'periodicidade', 'tarefa_principal', 'ativo']
        }),
        ('Prazo interno de execução', {
            'fields': [
                'controla_execucao',
                'tipo_dia_execucao',
                'dia_execucao',
                'meses_apos_competencia_execucao',
                'ajuste_dia_execucao_nao_util',
                'dias_antecedencia_alerta_execucao',
            ]
        }),
        ('Vencimento oficial da tarefa', {
            'fields': [
                'tipo_dia_vencimento',
                'dia_vencimento',
                'meses_apos_competencia',
                'ajuste_dia_nao_util',
                'dias_antecedencia_alerta',
                'inicio_competencia',
            ]
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

    def classificacao_tarefa(self, obj):
        return obj.classificacao()

    classificacao_tarefa.short_description = 'Classificacao'

    class Media:
        css = {
            'all': ('tarefas/admin_tarefa.css',)
        }
        js = ('tarefas/admin_tarefa.js',)


class PlanoTarefaItemInline(admin.TabularInline):
    model = PlanoTarefaItem
    extra = 1
    autocomplete_fields = ['tarefa']
    readonly_fields = ['tipo_tarefa', 'classificacao_tarefa']
    fields = ['tarefa', 'tipo_tarefa', 'classificacao_tarefa', 'ativo', 'observacao']

    def tipo_tarefa(self, obj):
        if obj and obj.tarefa_id:
            return obj.tarefa.tipo
        return '-'

    tipo_tarefa.short_description = 'Tipo'

    def classificacao_tarefa(self, obj):
        if obj and obj.tarefa_id:
            return obj.tarefa.classificacao()
        return '-'

    classificacao_tarefa.short_description = 'Classificacao'


@admin.register(PlanoTarefa)
class PlanoTarefaAdmin(admin.ModelAdmin):
    list_display = ['organizacao', 'nome', 'tributacao', 'padrao', 'ativo']
    list_display_links = ['nome']
    search_fields = ['organizacao__nome', 'nome', 'descricao']
    list_filter = ['organizacao', 'tributacao', 'padrao', 'ativo']
    readonly_fields = ['criado_em', 'atualizado_em']
    inlines = [PlanoTarefaItemInline]
    fieldsets = [
        ('Dados principais', {
            'fields': ['organizacao', 'nome', 'tributacao', 'descricao', 'padrao', 'ativo']
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


@admin.register(OcorrenciaTarefa)
class OcorrenciaTarefaAdmin(admin.ModelAdmin):
    list_display = [
        'empresa',
        'tarefa',
        'competencia',
        'data_referencia_admin',
        'data_alerta',
        'status',
        'status_exibicao_admin',
    ]
    search_fields = ['empresa__nome', 'empresa__cnpj', 'tarefa__nome']
    list_filter = ['status', 'competencia', 'tarefa__departamento', 'tarefa__tipo', 'tarefa__natureza']
    autocomplete_fields = ['empresa', 'tarefa', 'concluida_por', 'reaberta_por', 'cancelada_por']
    readonly_fields = ['criado_em', 'atualizado_em', 'status_exibicao_admin']
    fieldsets = [
        ('Dados principais', {
            'fields': ['empresa', 'tarefa', 'competencia', 'status', 'status_exibicao_admin']
        }),
        ('Datas da ocorrencia', {
            'fields': ['data_execucao', 'data_vencimento', 'data_alerta']
        }),
        ('Conclusao', {
            'fields': ['concluida_em', 'concluida_por']
        }),
        ('Reabertura', {
            'fields': ['reaberta_em', 'reaberta_por', 'motivo_reabertura']
        }),
        ('Cancelamento', {
            'fields': ['cancelada_em', 'cancelada_por']
        }),
        ('Observacoes', {
            'fields': ['observacao']
        }),
        ('Controle', {
            'fields': ['criado_em', 'atualizado_em']
        }),
    ]

    def data_referencia_admin(self, obj):
        return obj.data_referencia()

    data_referencia_admin.short_description = 'Data referencia'

    def status_exibicao_admin(self, obj):
        return obj.status_exibicao()

    status_exibicao_admin.short_description = 'Status exibido'
