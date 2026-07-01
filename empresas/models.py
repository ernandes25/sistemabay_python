from django.db import models


class Empresa(models.Model):
    class Tributacao(models.TextChoices):
        SIMPLES_NACIONAL = 'SIMPLES_NACIONAL', 'Simples Nacional'
        LUCRO_PRESUMIDO = 'LUCRO_PRESUMIDO', 'Lucro Presumido'
        LUCRO_REAL = 'LUCRO_REAL', 'Lucro Real'
        MEI = 'MEI', 'MEI'
        PF = 'PF', 'PF'

    nome = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, unique=True)
    logradouro = models.CharField(max_length=150)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    telefone_whatsapp = models.CharField(max_length=20)
    email = models.EmailField(max_length=150)
    tributacao = models.CharField(max_length=20, choices=Tributacao.choices)
    plano_tarefas = models.ForeignKey(
        'tarefas.PlanoTarefa',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    observacao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.nome
