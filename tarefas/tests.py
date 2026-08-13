from django.db import IntegrityError
from django.test import TestCase

from empresas.models import Organizacao
from tarefas.models import Departamento


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