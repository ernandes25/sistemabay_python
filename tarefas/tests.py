from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from empresas.models import Empresa, Organizacao
from tarefas.models import (
    Departamento,
    EmpresaTarefaAjuste,
    OcorrenciaTarefa,
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


class PlanoTarefaModelTests(TestCase):
    def test_nao_permite_plano_de_origem_de_outra_organizacao(self):
        organizacao_a = Organizacao.objects.create(nome='Organização A')
        organizacao_b = Organizacao.objects.create(nome='Organização B')
        plano_origem_b = PlanoTarefa.objects.create(
            organizacao=organizacao_b,
            nome='Plano de Origem B',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
        )
        plano_a = PlanoTarefa(
            organizacao=organizacao_a,
            nome='Plano A',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
            baseado_em=plano_origem_b,
        )

        with self.assertRaises(ValidationError):
            plano_a.full_clean()


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


class EmpresaTarefaAjusteModelTests(TestCase):
    def test_nao_permite_tarefa_de_outra_organizacao(self):
        organizacao_a = Organizacao.objects.create(nome='Organização A')
        organizacao_b = Organizacao.objects.create(nome='Organização B')
        departamento_b = Departamento.objects.create(
            organizacao=organizacao_b, nome='Fiscal'
        )
        tipo = TipoTarefa.objects.create(nome='Apuração Fiscal')
        tarefa_b = Tarefa.objects.create(
            nome='Apuração Fiscal',
            departamento=departamento_b,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            dia_vencimento=10,
        )
        empresa_a = Empresa.objects.create(
            organizacao=organizacao_a,
            nome='Empresa A',
            cnpj='00.000.000/0001-00',
            logradouro='Rua Teste',
            numero='100',
            bairro='Centro',
            cidade='Cidade Teste',
            uf='SP',
            cep='00000-000',
            telefone_whatsapp='11999999999',
            email='empresa@exemplo.com',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
        )

        ajuste = EmpresaTarefaAjuste(
            empresa=empresa_a,
            tarefa=tarefa_b,
            tipo_ajuste=EmpresaTarefaAjuste.TipoAjuste.ADICIONAR,
        )

        with self.assertRaises(ValidationError):
            ajuste.full_clean()


class OcorrenciaTarefaModelTests(TestCase):
    def test_nao_permite_tarefa_de_outra_organizacao(self):
        organizacao_a = Organizacao.objects.create(nome='Organização A')
        organizacao_b = Organizacao.objects.create(nome='Organização B')
        departamento_b = Departamento.objects.create(
            organizacao=organizacao_b,
            nome='Fiscal',
        )
        tipo = TipoTarefa.objects.create(nome='Apuração Fiscal')
        tarefa_b = Tarefa.objects.create(
            nome='Apuração Fiscal',
            departamento=departamento_b,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            dia_vencimento=10,
        )
        empresa_a = Empresa.objects.create(
            organizacao=organizacao_a,
            nome='Empresa A',
            cnpj='00.000.000/0001-00',
            logradouro='Rua Teste',
            numero='100',
            bairro='Centro',
            cidade='Cidade Teste',
            uf='SP',
            cep='00000-000',
            telefone_whatsapp='11999999999',
            email='empresa@exemplo.com',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
        )

        ocorrencia = OcorrenciaTarefa(
            empresa=empresa_a,
            tarefa=tarefa_b,
            competencia=date(2026, 1, 1),
        )

        with self.assertRaises(ValidationError):
            ocorrencia.full_clean()