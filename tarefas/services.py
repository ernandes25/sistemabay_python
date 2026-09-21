from calendar import monthrange
from datetime import date, timedelta

from tarefas.dias_uteis import dia_util_anterior, dia_util_posterior
from tarefas.models import (
    PlanoTarefaItem,
    Tarefa,
)


def calcular_data_vencimento(tarefa, competencia):
    ano = competencia.year
    mes = competencia.month + tarefa.meses_apos_competencia
    while mes > 12:
        mes = mes - 12
        ano = ano + 1

    dia = tarefa.dia_vencimento
    if tarefa.tipo_dia_vencimento == Tarefa.TipoDiaVencimento.ULTIMO_DIA_MES:
        dia = monthrange(ano, mes)[1]
    elif tarefa.tipo_dia_vencimento == Tarefa.TipoDiaVencimento.ULTIMO_DIA_UTIL:
        dia = monthrange(ano, mes)[1]

    data = date(ano, mes, dia)

    if tarefa.ajuste_dia_nao_util == Tarefa.AjusteDiaNaoUtil.ANTECIPAR:
        data = dia_util_anterior(data)
    elif tarefa.ajuste_dia_nao_util == Tarefa.AjusteDiaNaoUtil.PRORROGAR:
        data = dia_util_posterior(data)

    return data


def calcular_data_execucao(tarefa, competencia):
    ano = competencia.year
    mes = competencia.month + tarefa.meses_apos_competencia_execucao
    while mes > 12:
        mes = mes - 12
        ano = ano + 1

    dia = tarefa.dia_execucao
    if tarefa.tipo_dia_execucao == Tarefa.TipoDiaVencimento.ULTIMO_DIA_MES:
        dia = monthrange(ano, mes)[1]
    elif tarefa.tipo_dia_execucao == Tarefa.TipoDiaVencimento.ULTIMO_DIA_UTIL:
        dia = monthrange(ano, mes)[1]

    data = date(ano, mes, dia)

    if tarefa.ajuste_dia_execucao_nao_util == Tarefa.AjusteDiaNaoUtil.ANTECIPAR:
        data = dia_util_anterior(data)
    elif tarefa.ajuste_dia_execucao_nao_util == Tarefa.AjusteDiaNaoUtil.PRORROGAR:
        data = dia_util_posterior(data)

    return data


def calcular_data_alerta(tarefa, competencia):
    if tarefa.natureza == Tarefa.Natureza.PRINCIPAL:
        data = calcular_data_execucao(tarefa, competencia)
        dias = tarefa.dias_antecedencia_alerta_execucao
    else:
        data = calcular_data_vencimento(tarefa, competencia)
        dias = tarefa.dias_antecedencia_alerta

    return data - timedelta(days=dias)


def buscar_tarefas_da_empresa(empresa):
    if not empresa.plano_tarefas:
        return []

    itens_do_plano = PlanoTarefaItem.objects.filter(
        plano=empresa.plano_tarefas,
        ativo=True
    )
    return itens_do_plano
