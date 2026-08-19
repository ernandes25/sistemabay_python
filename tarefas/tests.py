from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from empresas.models import Empresa, Organizacao
from tarefas.models import (
    Departamento,
    PlanoTarefa,
    PlanoTarefaItem,
    Tarefa,
    TipoTarefa,
)


class DepartamentoModelTests(TestCase):
    def test_nao_permite_nome_repetido_na_mesma_organizacao(self):
        organizacao = Organizacao.objects.create(nome='Organização Teste')
        Departamento.objects.create(organizacao=organizacao, nome='Fiscal')
        with self.assertRaises(IntegrityError):
            Departamento.objects.create(organizacao=organizacao, nome='Fiscal')

    def test_permite_nome_repetido_em_organizacoes_diferentes(self):
        organizacao_a = Organizacao.objects.create(nome='Organização A')
        organizacao_b = Organizacao.objects.create(nome='Organização B')
        Departamento.objects.create(organizacao=organizacao_a, nome='Fiscal')
        Departamento.objects.create(organizacao=organizacao_b, nome='Fiscal')


class PlanoTarefaItemModelTests(TestCase):
    def test_nao_permite_tarefa_de_outra_organizacao(self):
        organizacao_a = Organizacao.objects.create(nome='Organização A')
        organizacao_b = Organizacao.objects.create(nome='Organização B')
        departamento_a = Departamento.objects.create(organizacao=organizacao_a, nome='Fiscal')
        tipo = TipoTarefa.objects.create(nome='Apuração Fiscal')
        tarefa_a = Tarefa.objects.create(
            nome='Apuração Fiscal',
            departamento=departamento_a,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            dia_vencimento=10,
        )

        plano_b = PlanoTarefa.objects.create(
            organizacao=organizacao_b,
            nome='Plano Organização B',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
        )
        item = PlanoTarefaItem(
            plano=plano_b,
            tarefa=tarefa_a,
        )

        with self.assertRaises(ValidationError):
            item.full_clean()