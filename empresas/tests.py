from django.core.exceptions import ValidationError
from django.test import TestCase

from empresas.models import Empresa, Organizacao
from tarefas.models import PlanoTarefa


class EmpresaModelTests(TestCase):
    def test_nao_permite_plano_de_outra_organizacao(self):
        organizacao_a = Organizacao.objects.create(nome="Organização A")
        organizacao_b = Organizacao.objects.create(nome="Organização B")
        plano_b = PlanoTarefa.objects.create(
            organizacao=organizacao_b,
            nome="Plano da Organização B",
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
        )
        empresa = Empresa(
            organizacao=organizacao_a,
            nome="Empresa Teste",
            cnpj="00.000.000/0001-00",
            logradouro="Rua Teste",
            numero="100",
            bairro="Centro",
            cidade="Cidade Teste",
            uf="SP",
            cep="00000-000",
            telefone_whatsapp="11999999999",
            email="teste@exemplo.com",
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
            plano_tarefas=plano_b,
        )

        with self.assertRaises(ValidationError):
            empresa.full_clean()

    def test_nao_permite_plano_com_tributacao_diferente(self):
        organizacao = Organizacao.objects.create(nome='Organização Teste')
        plano = PlanoTarefa.objects.create(
            organizacao=organizacao,
            nome='Plano Lucro Presumido',
            tributacao=Empresa.Tributacao.LUCRO_PRESUMIDO,
        )
        empresa = Empresa(
            organizacao=organizacao,
            nome='Empresa Simples Nacional',
            cnpj='00.000.000/0001-00',
            logradouro='Rua Teste',
            numero='100',
            bairro='Centro',
            cidade='Cidade Teste',
            uf='SP',
            cep='00000-000',
            telefone_whatsapp='11999999999',
            email='teste@exemplo.com',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
            plano_tarefas=plano,
        )

        with self.assertRaises(ValidationError):
            empresa.full_clean()
