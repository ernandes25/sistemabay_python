from datetime import timedelta

import holidays

feriados_brasil = holidays.Brazil()

def eh_feriado(data):
    return data in feriados_brasil

def eh_dia_util(data):
    if data.weekday() >= 5:
        return False
    
    return not eh_feriado(data)

def dia_util_anterior(data):
    while not eh_dia_util(data):
        data = data - timedelta(days=1)

    return data

def dia_util_posterior(data):
    while not eh_dia_util(data):
        data = data + timedelta(days=1)

    return data
 
