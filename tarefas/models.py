from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from empresas.models import Empresa


class Departamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nome


class TipoTarefa(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Tipo de tarefa'
        verbose_name_plural = 'Tipos de tarefa'

    def __str__(self):
        return self.nome


class Tarefa(models.Model):
    class Periodicidade(models.TextChoices):
        MENSAL = 'MENSAL', 'Mensal'
        BIMESTRAL = 'BIMESTRAL', 'Bimestral'
        TRIMESTRAL = 'TRIMESTRAL', 'Trimestral'
        SEMESTRAL = 'SEMESTRAL', 'Semestral'
        ANUAL = 'ANUAL', 'Anual'
        ESPORADICA = 'ESPORADICA', 'Esporadica'

    class TipoDiaVencimento(models.TextChoices):
        DIA_FIXO = 'DIA_FIXO', 'Dia fixo'
        ULTIMO_DIA_MES = 'ULTIMO_DIA_MES', 'Ultimo dia do mes'
        ULTIMO_DIA_UTIL = 'ULTIMO_DIA_UTIL', 'Ultimo dia util do mes'

    nome = models.CharField(max_length=150)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    tipo = models.ForeignKey(TipoTarefa, on_delete=models.PROTECT)
    periodicidade = models.CharField(max_length=20, choices=Periodicidade.choices)
    tipo_dia_vencimento = models.CharField(
        max_length=20,
        choices=TipoDiaVencimento.choices,
        default=TipoDiaVencimento.DIA_FIXO,
    )
    dia_vencimento = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
    )
    meses_apos_competencia = models.PositiveSmallIntegerField(default=0)
    data_vencimento_esporadica = models.DateField(null=True, blank=True)
    inicio_competencia = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    observacao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def clean(self):
        if self.periodicidade == self.Periodicidade.ESPORADICA:
            if not self.data_vencimento_esporadica:
                raise ValidationError({
                    'data_vencimento_esporadica': 'Informe a data de vencimento da tarefa esporadica.'
                })
            return

        if self.tipo_dia_vencimento == self.TipoDiaVencimento.DIA_FIXO and not self.dia_vencimento:
            raise ValidationError({
                'dia_vencimento': 'Informe o dia de vencimento para tarefas com dia fixo.'
            })

    def __str__(self):
        return self.nome


class PlanoTarefa(models.Model):
    nome = models.CharField(max_length=150)
    tributacao = models.CharField(max_length=20, choices=Empresa.Tributacao.choices)
    descricao = models.TextField(blank=True)
    padrao = models.BooleanField(default=False)
    baseado_em = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='planos_derivados',
    )
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tributacao', 'nome']
        verbose_name = 'Plano de tarefas'
        verbose_name_plural = 'Planos de tarefas'

    def clean(self):
        if self.padrao:
            plano_padrao = PlanoTarefa.objects.filter(
                tributacao=self.tributacao,
                padrao=True,
            ).exclude(pk=self.pk)

            if plano_padrao.exists():
                raise ValidationError({
                    'padrao': 'Ja existe um plano padrao para esta tributacao.'
                })

    def __str__(self):
        return self.nome


class PlanoTarefaItem(models.Model):
    plano = models.ForeignKey(PlanoTarefa, on_delete=models.CASCADE, related_name='itens')
    tarefa = models.ForeignKey(Tarefa, on_delete=models.PROTECT)
    ativo = models.BooleanField(default=True)
    observacao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tarefa__tipo__nome', 'tarefa__nome']
        verbose_name = 'Item do plano de tarefas'
        verbose_name_plural = 'Itens do plano de tarefas'
        constraints = [
            models.UniqueConstraint(
                fields=['plano', 'tarefa'],
                name='unique_tarefa_por_plano',
            )
        ]

    def __str__(self):
        return f'{self.plano} - {self.tarefa}'


class EmpresaTarefaAjuste(models.Model):
    class TipoAjuste(models.TextChoices):
        ADICIONAR = 'ADICIONAR', 'Adicionar tarefa'
        REMOVER = 'REMOVER', 'Remover tarefa'

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='ajustes_tarefas')
    tarefa = models.ForeignKey(Tarefa, on_delete=models.PROTECT)
    tipo_ajuste = models.CharField(max_length=20, choices=TipoAjuste.choices)
    ativo = models.BooleanField(default=True)
    observacao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['empresa__nome', 'tarefa__nome']
        verbose_name = 'Ajuste de tarefa por empresa'
        verbose_name_plural = 'Ajustes de tarefas por empresa'
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'tarefa'],
                name='unique_ajuste_tarefa_por_empresa',
            )
        ]

    def __str__(self):
        return f'{self.empresa} - {self.tarefa} ({self.get_tipo_ajuste_display()})'
