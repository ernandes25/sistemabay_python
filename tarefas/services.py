from calendar import monthrange
from datetime import date, timedelta

from tarefas.dias_uteis import dia_util_anterior, dia_util_posterior
from tarefas.models import (
    EmpresaTarefaAjuste,
    PlanoTarefaItem,
    Tarefa,
    OcorrenciaTarefa,
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

    tarefas = []

    for item in itens_do_plano:
        tarefas.append(item.tarefa)
        tarefas.extend(item.tarefa.subtarefas.all())

    ajustes = EmpresaTarefaAjuste.objects.filter(empresa=empresa, ativo=True)

    for ajuste in ajustes:
        if ajuste.tipo_ajuste == EmpresaTarefaAjuste.TipoAjuste.ADICIONAR:
            tarefas.append(ajuste.tarefa)
        else:
            if ajuste.tarefa in tarefas:
                tarefas.remove(ajuste.tarefa)
            for subtarefa in ajuste.tarefa.subtarefas.all():
                if subtarefa in tarefas:
                    tarefas.remove(subtarefa)
    return tarefas


def gerar_ocorrencias_da_competencia(empresa, competencia):
    tarefas = buscar_tarefas_da_empresa(empresa)
    criadas = 0

    for tarefa in tarefas:
        vencimento = calcular_data_vencimento(tarefa, competencia)
        alerta = calcular_data_alerta(tarefa, competencia)

        if tarefa.natureza == Tarefa.Natureza.PRINCIPAL:
            execucao = calcular_data_execucao(tarefa, competencia)
        else:
            execucao = None

        alerta = calcular_data_alerta(tarefa, competencia)

        ocorrencia, criada = OcorrenciaTarefa.objects.get_or_create(
            empresa=empresa,
            tarefa=tarefa,
            competencia=competencia,
            defaults={
                'data_execucao': execucao,
                'data_vencimento': vencimento,
                'data_alerta': alerta,
            },
        )
        if criada:
            criadas = criadas + 1

    return criadas