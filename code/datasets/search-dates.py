# Programa que cria uma lista de datas com horas 
# Encontra indeces por meio das datas
# Encontra as datas por meio dos indices

import xarray as xr
import os
import numpy as np
from datetime import datetime, timedelta

def generate_date_list_with_hours(start_date, end_date):
    dates = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current_date <= end_date:
        for hour in range(24):  # Adiciona horas do dia
            date_with_hour = current_date + timedelta(hours=hour)
            dates.append(date_with_hour.strftime('%Y-%m-%d-%H'))
        current_date += timedelta(days=1)
    
    return dates

def find_date_index(dates, target_date):
    try:
        return dates.index(target_date)
    except ValueError:
        return 'nao existe :('  # Retorna -1 se a data não for encontrada

def find_date_by_index(dates, index):
    if 0 <= index < len(dates):
        return dates[index]
    else:
        return 'nao existe :('  # Retorna None se o índice estiver fora do intervalo

# Observacao: o Brams comeca um dia depois de cada estacao por conta
# do spinup

dates_chuvosa = generate_date_list_with_hours('2014-02-15', '2014-02-24')
dates_seca = generate_date_list_with_hours('2014-09-01', '2014-09-10')
dates_transicao = generate_date_list_with_hours('2014-10-01', '2014-10-10')

target_date = '2014-10-10-20'
index = find_date_index(dates_transicao, target_date)
print(f'O índice da data {target_date} é: {index}')

index = 148
date_at_index = find_date_by_index(dates_seca, index)
print(f'A data no índice {index} é: {date_at_index}')
