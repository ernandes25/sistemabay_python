from calendar import monthrange
from datetime import date

from tarefas.models import (
    PlanoTarefaItem,
    Tarefa,
)


def calcular_data_vencimento(tarefa, competencia):
    ano = competencia.year
    mes = competencia.month + tarefa.meses_apos_competencia
    if mes > 12:
        mes = mes - 12
        ano = ano + 1
    dia = tarefa.dia_vencimento
    if tarefa.tipo_dia_vencimento == Tarefa.TipoDiaVencimento.ULTIMO_DIA_MES:
        dia = monthrange(ano, mes)[1]

    return date(ano, mes, dia)


def buscar_tarefas_da_empresa(empresa):
    if not empresa.plano_tarefas:
        return []

    itens_do_plano = PlanoTarefaItem.objects.filter(
        plano=empresa.plano_tarefas,
        ativo=True
    )
    return itens_do_plano
