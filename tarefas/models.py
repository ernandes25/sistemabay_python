from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from empresas.models import Empresa, Organizacao


class Departamento(models.Model):
    organizacao = models.ForeignKey(
        Organizacao,
        on_delete=models.PROTECT,
        related_name='departamentos',
    )
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        constraints = [
            models.UniqueConstraint(
                fields=['organizacao', 'nome'],
                name='unique_departamento_por_organizacao',
            ),
        ]

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
    class Natureza(models.TextChoices):
        PRINCIPAL = 'PRINCIPAL', 'Tarefa principal'
        SIMPLES = 'SIMPLES', 'Tarefa simples'
        SUBTAREFA = 'SUBTAREFA', 'Subtarefa'

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

    class AjusteDiaNaoUtil(models.TextChoices):
        MANTER_DATA = 'MANTER_DATA', 'Manter data'
        ANTECIPAR = 'ANTECIPAR', 'Antecipar para dia util anterior'
        PRORROGAR = 'PRORROGAR', 'Prorrogar para proximo dia util'

    class MomentoCompetencia(models.IntegerChoices):
        PROPRIA_COMPETENCIA = 0, 'Na própria competência'
        MES_SEGUINTE = 1, 'No mês seguinte'
        DOIS_MESES_DEPOIS = 2, 'Dois meses depois'
        TRES_MESES_DEPOIS = 3, 'Três meses depois'
        QUATRO_MESES_DEPOIS = 4, 'Quatro meses depois'
        CINCO_MESES_DEPOIS = 5, 'Cinco meses depois'
        SEIS_MESES_DEPOIS = 6, 'Seis meses depois'
        SETE_MESES_DEPOIS = 7, 'Sete meses depois'
        OITO_MESES_DEPOIS = 8, 'Oito meses depois'
        NOVE_MESES_DEPOIS = 9, 'Nove meses depois'
        DEZ_MESES_DEPOIS = 10, 'Dez meses depois'
        ONZE_MESES_DEPOIS = 11, 'Onze meses depois'
        DOZE_MESES_DEPOIS = 12, 'Doze meses depois'

    nome = models.CharField(max_length=150)
    natureza = models.CharField(
        max_length=20,
        choices=Natureza.choices,
        default=Natureza.SIMPLES,
    )
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    tipo = models.ForeignKey(TipoTarefa, on_delete=models.PROTECT)
    tarefa_principal = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='subtarefas',
    )
    periodicidade = models.CharField(max_length=20, choices=Periodicidade.choices)
    controla_execucao = models.BooleanField(default=False)
    tipo_dia_execucao = models.CharField(
        max_length=20,
        choices=TipoDiaVencimento.choices,
        default=TipoDiaVencimento.DIA_FIXO,
    )
    dia_execucao = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
    )
    meses_apos_competencia_execucao = models.PositiveSmallIntegerField(
        'Mês de execução',
        choices=MomentoCompetencia.choices,
        default=MomentoCompetencia.PROPRIA_COMPETENCIA,
    )
    ajuste_dia_execucao_nao_util = models.CharField(
        max_length=20,
        choices=AjusteDiaNaoUtil.choices,
        default=AjusteDiaNaoUtil.MANTER_DATA,
    )
    dias_antecedencia_alerta_execucao = models.PositiveSmallIntegerField(default=0)
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
    meses_apos_competencia = models.PositiveSmallIntegerField(
        'Mês do vencimento',
        choices=MomentoCompetencia.choices,
        default=MomentoCompetencia.PROPRIA_COMPETENCIA,
    )
    ajuste_dia_nao_util = models.CharField(
        max_length=20,
        choices=AjusteDiaNaoUtil.choices,
        default=AjusteDiaNaoUtil.MANTER_DATA,
    )
    dias_antecedencia_alerta = models.PositiveSmallIntegerField(default=0)
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

    def classificacao(self):
        return self.get_natureza_display()

    def clean(self):
        if self.tarefa_principal_id and self.tarefa_principal_id == self.pk:
            raise ValidationError({
                'tarefa_principal': 'Uma tarefa nao pode ser principal dela mesma.'
            })

        if self.natureza == self.Natureza.SUBTAREFA and not self.tarefa_principal_id:
            raise ValidationError({
                'tarefa_principal': 'Informe a tarefa principal desta subtarefa.'
            })

        if (
            self.natureza == self.Natureza.SUBTAREFA
            and self.tarefa_principal_id
            and self.departamento_id
            and self.tarefa_principal.departamento_id != self.departamento_id
        ):
            raise ValidationError({
                'tarefa_principal': 'A tarefa principal deve pertencer ao mesmo departamento da subtarefa.'
            })

        if self.natureza != self.Natureza.SUBTAREFA and self.tarefa_principal_id:
            raise ValidationError({
                'tarefa_principal': 'Somente subtarefas devem ter uma tarefa principal vinculada.'
            })

        if self.natureza != self.Natureza.PRINCIPAL and self.controla_execucao:
            raise ValidationError({
                'controla_execucao': 'Somente tarefas principais controlam execucao interna.'
            })

        if self.natureza == self.Natureza.PRINCIPAL and not self.controla_execucao:
            raise ValidationError({
                'controla_execucao': 'Tarefas principais devem controlar execucao interna.'
            })

        if self.controla_execucao and self.tipo_dia_execucao == self.TipoDiaVencimento.DIA_FIXO and not self.dia_execucao:
            raise ValidationError({
                'dia_execucao': 'Informe o dia de execucao para tarefas principais com dia fixo.'
            })

        if self.natureza == self.Natureza.PRINCIPAL:
            return

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
    organizacao = models.ForeignKey(
        Organizacao,
        on_delete=models.PROTECT,
        related_name='planos_tarefas',
    )
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
        if self.baseado_em_id and self.organizacao_id:
            if self.baseado_em.organizacao_id != self.organizacao_id:
                raise ValidationError({
                    'baseado_em': 'O plano de origem deve pertencer à mesma organização.'
                })

        if self.padrao:
            plano_padrao = PlanoTarefa.objects.filter(
                organizacao=self.organizacao,
                tributacao=self.tributacao,
                padrao=True,
            ).exclude(pk=self.pk)

            if plano_padrao.exists():
                raise ValidationError({
                    'padrao': 'Já existe um plano padrão para esta tributação nesta organização.'
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

    def clean(self):
        if self.plano_id and self.tarefa_id:
            if self.plano.organizacao_id != self.tarefa.departamento.organizacao_id:
                raise ValidationError({
                    'tarefa': 'A tarefa deve pertencer à mesma organização do plano.'
                })

        if self.tarefa_id and self.tarefa.natureza == Tarefa.Natureza.SUBTAREFA:
            raise ValidationError({
                'tarefa': 'Subtarefas nao devem ser adicionadas diretamente ao plano. Adicione a tarefa principal.'
            })

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

    def clean(self):
        if self.empresa_id and self.tarefa_id:
            if self.empresa.organizacao_id != self.tarefa.departamento.organizacao_id:
                raise ValidationError({
                    'tarefa': 'A tarefa deve pertencer à mesma organização da empresa.'
                })

    def __str__(self):
        return f'{self.empresa} - {self.tarefa} ({self.get_tipo_ajuste_display()})'


class OcorrenciaTarefa(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        CONCLUIDA = 'CONCLUIDA', 'Concluida'
        CANCELADA = 'CANCELADA', 'Cancelada'

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='ocorrencias_tarefas')
    tarefa = models.ForeignKey(Tarefa, on_delete=models.PROTECT, related_name='ocorrencias')
    competencia = models.DateField()
    data_execucao = models.DateField(null=True, blank=True)
    data_vencimento = models.DateField(null=True, blank=True)
    data_alerta = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )
    concluida_em = models.DateTimeField(null=True, blank=True)
    concluida_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tarefas_concluidas',
    )
    reaberta_em = models.DateTimeField(null=True, blank=True)
    reaberta_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tarefas_reabertas',
    )
    motivo_reabertura = models.TextField(blank=True)
    cancelada_em = models.DateTimeField(null=True, blank=True)
    cancelada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tarefas_canceladas',
    )
    observacao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['competencia', 'empresa__nome', 'tarefa__nome']
        verbose_name = 'Ocorrencia de tarefa'
        verbose_name_plural = 'Ocorrencias de tarefas'
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'tarefa', 'competencia'],
                name='unique_ocorrencia_tarefa_por_competencia',
            )
        ]

    def clean(self):
        if self.empresa_id and self.tarefa_id:
            if self.empresa.organizacao_id != self.tarefa.departamento.organizacao_id:
                raise ValidationError({
                    'tarefa': 'A tarefa deve pertencer à mesma organização da empresa.'
                })

    def data_referencia(self):
        if self.tarefa.natureza == Tarefa.Natureza.PRINCIPAL:
            return self.data_execucao

        return self.data_vencimento

    def esta_atrasada(self):
        data_referencia = self.data_referencia()

        if self.status != self.Status.PENDENTE or not data_referencia:
            return False

        return timezone.localdate() > data_referencia

    def status_exibicao(self):
        if self.esta_atrasada():
            return 'Atrasada'

        return self.get_status_display()

    def concluir(self, usuario=None):
        self.status = self.Status.CONCLUIDA
        self.concluida_em = timezone.now()
        self.concluida_por = usuario
        self.save(update_fields=['status', 'concluida_em', 'concluida_por', 'atualizado_em'])

    def reabrir(self, usuario=None, motivo=''):
        self.status = self.Status.PENDENTE
        self.reaberta_em = timezone.now()
        self.reaberta_por = usuario
        self.motivo_reabertura = motivo
        self.save(update_fields=['status', 'reaberta_em', 'reaberta_por', 'motivo_reabertura', 'atualizado_em'])

    def cancelar(self, usuario=None):
        self.status = self.Status.CANCELADA
        self.cancelada_em = timezone.now()
        self.cancelada_por = usuario
        self.save(update_fields=['status', 'cancelada_em', 'cancelada_por', 'atualizado_em'])

    def __str__(self):
        competencia = self.competencia.strftime('%m/%Y') if self.competencia else ''
        return f'{self.empresa} - {self.tarefa} - {competencia}'
