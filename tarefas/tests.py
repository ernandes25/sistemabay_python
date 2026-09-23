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
from tarefas.services import (
    buscar_tarefas_da_empresa,
    calcular_data_alerta,
    calcular_data_execucao,
    calcular_data_vencimento,
    gerar_ocorrencias_da_competencia,
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

    def test_nao_permite_dois_planos_padrao_na_mesma_organizacao_e_tributacao(self):
        organizacao = Organizacao.objects.create(nome='Organização Teste')
        PlanoTarefa.objects.create(
            organizacao=organizacao,
            nome='Plano Padrão 1',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
            padrao=True,
        )

        with self.assertRaises(IntegrityError):
            PlanoTarefa.objects.create(
                organizacao=organizacao,
                nome='Plano Padrão 2',
                tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
                padrao=True,
            )


class PlanoTarefaItemModelTests(TestCase):
    def test_nao_permite_tarefa_de_outra_organizacao(self):
        organizacao_a = Organizacao.objects.create(nome='Organização A')
        organizacao_b = Organizacao.objects.create(nome='Organização B')
        departamento_a = Departamento.objects.create(
            organizacao=organizacao_a, nome='Fiscal')
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


class TarefaPrincipalComSubtarefaTests(TestCase):
    def test_permite_salvar_tarefa_principal_nova_sem_subtarefa(self):
        organizacao = Organizacao.objects.create(nome='Organização Teste')
        departamento = Departamento.objects.create(
            organizacao=organizacao,
            nome='Pessoal',
        )
        tipo = TipoTarefa.objects.create(nome='Folha de Pagamento')
        principal = Tarefa.objects.create(
            nome='Folha de Pagamento',
            natureza=Tarefa.Natureza.PRINCIPAL,
            departamento=departamento,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            controla_execucao=True,
            dia_execucao=5,
        )

        self.assertIsNotNone(principal.pk)

    def test_nao_permite_tarefa_principal_sem_subtarefa(self):
        organizacao = Organizacao.objects.create(nome='Organização Teste')
        departamento = Departamento.objects.create(
            organizacao=organizacao,
            nome='Pessoal',
        )
        tipo = TipoTarefa.objects.create(nome='Folha de Pagamento')
        principal = Tarefa.objects.create(
            nome='Folha de Pagamento',
            natureza=Tarefa.Natureza.PRINCIPAL,
            departamento=departamento,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            controla_execucao=True,
            dia_execucao=5,
        )

        with self.assertRaises(ValidationError):
            principal.full_clean()

    def test_permite_tarefa_principal_com_subtarefa(self):
        organizacao = Organizacao.objects.create(nome='Organização Teste')
        departamento = Departamento.objects.create(
            organizacao=organizacao,
            nome='Pessoal',
        )
        tipo = TipoTarefa.objects.create(nome='Folha de Pagamento')
        principal = Tarefa.objects.create(
            nome='Folha de Pagamento',
            natureza=Tarefa.Natureza.PRINCIPAL,
            departamento=departamento,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            controla_execucao=True,
            dia_execucao=5,
        )
        Tarefa.objects.create(
            nome='Calcular folha',
            natureza=Tarefa.Natureza.SUBTAREFA,
            tarefa_principal=principal,
            departamento=departamento,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            dia_vencimento=10,
        )

        principal.full_clean()

    def test_nao_exige_subtarefa_de_tarefa_simples(self):
        organizacao = Organizacao.objects.create(nome='Organização Teste')
        departamento = Departamento.objects.create(
            organizacao=organizacao,
            nome='Fiscal',
        )
        tipo = TipoTarefa.objects.create(nome='Apuração Fiscal')
        simples = Tarefa.objects.create(
            nome='Enviar DAS',
            natureza=Tarefa.Natureza.SIMPLES,
            departamento=departamento,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            dia_vencimento=20,
        )

        simples.full_clean()


class CalculoDatasTests(TestCase):
    def test_calcula_vencimento_no_mes_seguinte(self):
        competencia = date(2026, 1, 1)
        tarefa = Tarefa(
            tipo_dia_vencimento=Tarefa.TipoDiaVencimento.DIA_FIXO,
            dia_vencimento=20,
            meses_apos_competencia=Tarefa.MomentoCompetencia.MES_SEGUINTE,
        )
        vencimento_esperado = date(2026, 2, 20)
        vencimento_calculado = calcular_data_vencimento(tarefa, competencia)
        self.assertEqual(vencimento_calculado, vencimento_esperado)

    def test_calcula_vencimento_no_ano_seguinte(self):
        competencia = date(2026, 12, 1)
        tarefa = Tarefa(
            tipo_dia_vencimento=Tarefa.TipoDiaVencimento.DIA_FIXO,
            dia_vencimento=10,
            meses_apos_competencia=Tarefa.MomentoCompetencia.MES_SEGUINTE,
        )
        vencimento_esperado = date(2027, 1, 10)
        vencimento_calculado = calcular_data_vencimento(tarefa, competencia)
        self.assertEqual(vencimento_calculado, vencimento_esperado)

    def test_calcula_ultimo_dia_do_mes(self):
        competencia = date(2026, 1, 1)
        tarefa = Tarefa(
            tipo_dia_vencimento=Tarefa.TipoDiaVencimento.ULTIMO_DIA_MES,
            meses_apos_competencia=Tarefa.MomentoCompetencia.MES_SEGUINTE,
        )
        vencimento_esperado = date(2026, 2, 28)
        vencimento_calculado = calcular_data_vencimento(tarefa, competencia)
        self.assertEqual(vencimento_calculado, vencimento_esperado)

    def test_calcula_ultimo_dia_util(self):
        competencia = date(2026, 1, 1)
        tarefa = Tarefa(
            tipo_dia_vencimento=Tarefa.TipoDiaVencimento.ULTIMO_DIA_UTIL,
            meses_apos_competencia=Tarefa.MomentoCompetencia.MES_SEGUINTE,
            ajuste_dia_nao_util=Tarefa.AjusteDiaNaoUtil.ANTECIPAR,

        )
        vencimento_esperado = date(2026, 2, 27)
        vencimento_calculado = calcular_data_vencimento(tarefa, competencia)
        self.assertEqual(vencimento_calculado, vencimento_esperado)

    def test_calcula_data_execucao(self):
        competencia = date(2026, 1, 1)
        tarefa = Tarefa(
            tipo_dia_execucao=Tarefa.TipoDiaVencimento.DIA_FIXO,
            dia_execucao=15,
            meses_apos_competencia_execucao=Tarefa.MomentoCompetencia.PROPRIA_COMPETENCIA,
        )
        execucao_esperada = date(2026, 1, 15)
        execucao_calculada = calcular_data_execucao(tarefa, competencia)
        self.assertEqual(execucao_calculada, execucao_esperada)

    def test_calcula_alerta_de_tarefa_simples(self):
        competencia = date(2026, 1, 1)
        tarefa = Tarefa(
            natureza=Tarefa.Natureza.SIMPLES,
            tipo_dia_vencimento=Tarefa.TipoDiaVencimento.DIA_FIXO,
            dia_vencimento=20,
            meses_apos_competencia=Tarefa.MomentoCompetencia.MES_SEGUINTE,
            dias_antecedencia_alerta=5,
        )
        alerta_esperado = date(2026, 2, 15)
        alerta_calculado = calcular_data_alerta(tarefa, competencia)
        self.assertEqual(alerta_calculado, alerta_esperado)

    def test_calcula_alerta_de_tarefa_principal(self):
        competencia = date(2026, 1, 1)
        tarefa = Tarefa(
            natureza=Tarefa.Natureza.PRINCIPAL,
            tipo_dia_execucao=Tarefa.TipoDiaVencimento.DIA_FIXO,
            dia_execucao=10,
            meses_apos_competencia_execucao=Tarefa.MomentoCompetencia.PROPRIA_COMPETENCIA,
            dias_antecedencia_alerta_execucao=3,
        )
        alerta_esperado = date(2026, 1, 7)
        alerta_calculado = calcular_data_alerta(tarefa, competencia)
        self.assertEqual(alerta_calculado, alerta_esperado)


class BuscarTarefasDaEmpresaTests(TestCase):
    def test_devolve_as_tarefas_do_plano_da_empresa(self):
        organizacao = Organizacao.objects.create(nome='Organização Teste')
        departamento = Departamento.objects.create(
            organizacao=organizacao,
            nome='Fiscal',
        )
        tipo = TipoTarefa.objects.create(nome='Apuração Fiscal')
        tarefa = Tarefa.objects.create(
            nome='Apuração Fiscal',
            departamento=departamento,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            dia_vencimento=10,
        )
        plano = PlanoTarefa.objects.create(
            organizacao=organizacao,
            nome='Plano Teste',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
        )
        PlanoTarefaItem.objects.create(plano=plano, tarefa=tarefa)
        empresa = Empresa.objects.create(
            organizacao=organizacao,
            nome='Empresa Teste',
            cnpj='11.111.111/0001-11',
            logradouro='Rua Teste',
            numero='100',
            bairro='Centro',
            cidade='Cidade Teste',
            uf='SP',
            cep='00000-000',
            telefone_whatsapp='11999999999',
            email='empresa@exemplo.com',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
            plano_tarefas=plano,
        )

        tarefas = buscar_tarefas_da_empresa(empresa)

        self.assertEqual(list(tarefas), [tarefa])

    def test_inclui_as_subtarefas_da_tarefa_principal(self):
        organizacao = Organizacao.objects.create(nome='Organização Teste')
        departamento = Departamento.objects.create(
            organizacao=organizacao,
            nome='Pessoal',
        )
        tipo = TipoTarefa.objects.create(nome='Folha de Pagamento')
        principal = Tarefa.objects.create(
            nome='Folha de Pagamento',
            natureza=Tarefa.Natureza.PRINCIPAL,
            departamento=departamento,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            controla_execucao=True,
            dia_execucao=5,
        )
        subtarefa = Tarefa.objects.create(
            nome='Calcular folha',
            natureza=Tarefa.Natureza.SUBTAREFA,
            tarefa_principal=principal,
            departamento=departamento,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            dia_vencimento=10,
        )
        plano = PlanoTarefa.objects.create(
            organizacao=organizacao,
            nome='Plano Teste',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
        )
        PlanoTarefaItem.objects.create(plano=plano, tarefa=principal)
        empresa = Empresa.objects.create(
            organizacao=organizacao,
            nome='Empresa Teste',
            cnpj='22.222.222/0001-22',
            logradouro='Rua Teste',
            numero='100',
            bairro='Centro',
            cidade='Cidade Teste',
            uf='SP',
            cep='00000-000',
            telefone_whatsapp='11999999999',
            email='empresa@exemplo.com',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
            plano_tarefas=plano,
        )

        tarefas = buscar_tarefas_da_empresa(empresa)

        self.assertEqual(list(tarefas), [principal, subtarefa])


class GerarOcorrenciasDaCompetenciaTests(TestCase):
    def test_gera_as_ocorrencias_da_empresa(self):
      
        organizacao = Organizacao.objects.create(nome='Organização Teste')
        departamento = Departamento.objects.create(
            organizacao=organizacao,
            nome='Fiscal',
        )

        tipo = TipoTarefa.objects.create(nome='Apuração Fiscal')
        tarefa = Tarefa.objects.create(
            nome='Apuração Fiscal',
            departamento=departamento,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            dia_vencimento=10,
        )
        plano = PlanoTarefa.objects.create(
            organizacao=organizacao,
            nome='Plano Teste',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
        )
        PlanoTarefaItem.objects.create(plano=plano, tarefa=tarefa)
        empresa = Empresa.objects.create(
            organizacao=organizacao,
            nome='Empresa Teste',
            cnpj='33.333.333/0001-33',
            logradouro='Rua Teste',
            numero='100',
            bairro='Centro',
            cidade='Cidade Teste',
            uf='SP',
            cep='00000-000',
            telefone_whatsapp='11999999999',
            email='empresa@exemplo.com',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
            plano_tarefas=plano,
        )

        competencia = date(2026, 9, 1)
        criadas = gerar_ocorrencias_da_competencia(empresa, competencia)

        self.assertEqual(criadas, 1)
        self.assertEqual(OcorrenciaTarefa.objects.count(), 1)


    def test_nao_duplica_ocorrencia_da_mesma_competencia(self):
      
        organizacao = Organizacao.objects.create(nome='Organização Teste')
        departamento = Departamento.objects.create(
            organizacao=organizacao,
            nome='Fiscal',
        )

        tipo = TipoTarefa.objects.create(nome='Apuração Fiscal')
        tarefa = Tarefa.objects.create(
            nome='Apuração Fiscal',
            departamento=departamento,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            dia_vencimento=10,
        )
        plano = PlanoTarefa.objects.create(
            organizacao=organizacao,
            nome='Plano Teste',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
        )
        PlanoTarefaItem.objects.create(plano=plano, tarefa=tarefa)
        empresa = Empresa.objects.create(
            organizacao=organizacao,
            nome='Empresa Teste',
            cnpj='44.444.444/0001-44',
            logradouro='Rua Teste',
            numero='100',
            bairro='Centro',
            cidade='Cidade Teste',
            uf='SP',
            cep='00000-000',
            telefone_whatsapp='11999999999',
            email='empresa@exemplo.com',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
            plano_tarefas=plano,
        )

        competencia = date(2026, 9, 1)
        primeira_vez = gerar_ocorrencias_da_competencia(empresa, competencia)
        segunda_vez = gerar_ocorrencias_da_competencia(empresa, competencia)

        self.assertEqual(primeira_vez, 1)
        self.assertEqual(segunda_vez, 0)
        self.assertEqual(OcorrenciaTarefa.objects.count(), 1)

    def test_gera_ocorrencia_de_tarefa_principal_com_execucao(self):
        organizacao = Organizacao.objects.create(nome='Organização Teste')
        departamento = Departamento.objects.create(
            organizacao=organizacao,
            nome='Pessoal',
        )
        tipo = TipoTarefa.objects.create(nome='Folha de Pagamento')

        principal = Tarefa.objects.create(
            nome='Folha de Pagamento',
            natureza=Tarefa.Natureza.PRINCIPAL,
            departamento=departamento,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            controla_execucao=True,
            tipo_dia_execucao=Tarefa.TipoDiaVencimento.DIA_FIXO,
            dia_execucao=5,
            meses_apos_competencia_execucao=Tarefa.MomentoCompetencia.PROPRIA_COMPETENCIA,
            dias_antecedencia_alerta_execucao=2,
            dia_vencimento=10,
            meses_apos_competencia=Tarefa.MomentoCompetencia.PROPRIA_COMPETENCIA,
        )
        subtarefa = Tarefa.objects.create(
            nome='Calcular folha',
            natureza=Tarefa.Natureza.SUBTAREFA,
            tarefa_principal=principal,
            departamento=departamento,
            tipo=tipo,
            periodicidade=Tarefa.Periodicidade.MENSAL,
            dia_vencimento=10,
        )

        plano = PlanoTarefa.objects.create(
            organizacao=organizacao,
            nome='Plano Teste',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
        )
        PlanoTarefaItem.objects.create(plano=plano, tarefa=principal)
        empresa = Empresa.objects.create(
            organizacao=organizacao,
            nome='Empresa Teste',
            cnpj='55.555.555/0001-55',
            logradouro='Rua Teste',
            numero='100',
            bairro='Centro',
            cidade='Cidade Teste',
            uf='SP',
            cep='00000-000',
            telefone_whatsapp='11999999999',
            email='empresa@exemplo.com',
            tributacao=Empresa.Tributacao.SIMPLES_NACIONAL,
            plano_tarefas=plano,
        )

        competencia = date(2026, 9, 1)
        criadas = gerar_ocorrencias_da_competencia(empresa, competencia)

        self.assertEqual(criadas, 2)
        self.assertEqual(OcorrenciaTarefa.objects.count(), 2)

        ocorrencia_principal = OcorrenciaTarefa.objects.get(tarefa=principal)
        ocorrencia_subtarefa = OcorrenciaTarefa.objects.get(tarefa=subtarefa)

        self.assertEqual(ocorrencia_principal.data_execucao, date(2026, 9, 5))
        self.assertIsNone(ocorrencia_subtarefa.data_execucao)
        