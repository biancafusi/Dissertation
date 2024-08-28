import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd
from percentile_data import *

matplotlib.use('Agg')

'''
Made by: Bianca Fusinato
This code reads the .txt file and do some spatial 
over time plots.
'''

def plot_L_org(L_org_GPM, L_org_ERA5, L_org_CP, L_org_OFF, rmax=25, dxy=1):
    bin_w = 2 * dxy
    bins = np.arange(0, rmax + bin_w * dxy, bin_w * dxy)
    x = np.arange(0, rmax)

    plt.figure(figsize=(16, 4))
    plt.plot(x, L_org_GPM, label='GPM')
    plt.plot(x, L_org_ERA5, label='ERA5')
    plt.plot(x, L_org_CP, label='CP')
    plt.plot(x, L_org_OFF, label='OFF')
    plt.xlim(0,50)
    plt.xlabel('X-axis Label')  # Customize as needed
    plt.ylabel('L_org')  # Customize as needed
    plt.title('L_org Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('all.png')

def ler_matrizes(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    matrizes = []
    for line in lines:
        if line.strip().startswith("L_org = ["):
            matriz_str = line.strip()[8:]
            matriz_str = matriz_str.replace('[', '').replace(']', '')
            matriz = [float(num) if num != 'nan' else 0 for num in matriz_str.split(", ")]
            matriz = matriz[1:]
            matrizes.append(matriz)
    
    matrizes_array = np.array(matrizes)
    return matrizes_array

def calcular_media_desvio_padrao(file_path):
    L_org_data = ler_matrizes(file_path)
    media_por_ponto = np.mean(L_org_data, axis=0)
    desvio_padrao_por_ponto = np.std(L_org_data, axis=0)
    return media_por_ponto, desvio_padrao_por_ponto

def ler_matriz(file_path):
    listas_L_org = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_L_org = []

    for line in lines:
        if line.strip().startswith("L_org:"):
            matriz_str = line.strip().split(": ")[1]
            matriz_str = matriz_str.strip('[]')
            current_L_org = [float(num) if num != 'nan' else 0 for num in matriz_str.split()]
            listas_L_org.append(current_L_org)

    matriz_array = np.array(listas_L_org)

    return matriz_array

def plot_TimeSeries_L_org(L_org, save_name, month):
    time = np.arange(len(L_org))  

    plt.figure(figsize=(16, 4))
    plt.plot(time, L_org, label='ERA5')
    plt.xlabel('Tempo')  # Customize conforme necessário
    plt.ylabel('L_org')  # Customize conforme necessário
    plt.title(f'Serie Temporal para {month}')
    plt.legend()
    plt.grid(True)
    plt.savefig(save_name)

def plot_TimeSeries_L_org_precip(L_org, rawprec_era_month, month, year, save_name):
    """
    Plota a série temporal de L_org e precipitação média em uma região,
    ajustando as escalas e convertendo a precipitação para mm/h.

    Args:
        L_org: Série temporal de L_org.
        rawprec_era_month: Array 3D com as séries temporais de precipitação (tempo, lat, lon).
        month: Mês a ser plotado.
        save_name: Nome do arquivo para salvar o gráfico.
    """

    precip_mmh = rawprec_era_month * 1000
    precip_mean = np.mean(precip_mmh, axis=(1, 2)) 
    precip_mean = precip_mean[:-1]
    time = np.arange(len(L_org))

    fig, ax1 = plt.subplots(figsize=(20, 4))
    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('L_org', color=color)
    ax1.plot(time, L_org, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Precipitation Mean (over space) (mm/h)', color=color)
    ax2.plot(time, precip_mean, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Time Serie for {month}{year}')
    plt.grid(True)
    plt.savefig(save_name)

def plot_TimeSeries_L_org_precip_panel(L_org_list, rawprec_era_month_list, months, years, save_name):
    num_plots = len(L_org_list)
    fig, axs = plt.subplots(num_plots, 1, figsize=(20, 4 * num_plots), sharex=True)
    axs = np.atleast_1d(axs)  # Garantir que axs seja uma lista, mesmo com um único subplot

    for i in range(num_plots):
        L_org = L_org_list[i]
        rawprec_era_month = rawprec_era_month_list[i]
        month = months[i]
        year = years[i]

        precip_mmh = rawprec_era_month * 1000
        precip_mean = np.mean(precip_mmh, axis=(1, 2))
        precip_mean = precip_mean[:]  # Remover o último elemento para ajustar o comprimento
        print(precip_mean.shape)
        time = np.arange(len(L_org))
        print(time.shape)
       

        ax1 = axs[i]
        color = 'tab:red'
        ax1.set_ylabel('L_org', color=color)
        ax1.plot(time, L_org[:,0], color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Precipitation Mean (over space) (mm/h)', color=color)
        ax2.plot(time, precip_mean, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        ax1.set_title(f'Time Series for {month} {year}')
        ax1.grid(True)

    plt.xlabel('Time')
    plt.savefig(save_name)
    plt.show()



def diurnal_cycle(dataset, time_index, month, year, save_name):
    prec = dataset[time_index, :, :] * 1000
    lat_mean_prec = np.mean(prec, axis=2)
    lon_mean_prec = np.mean(lat_mean_prec, axis=1)

    hourly_prec = np.zeros(24)
    time_index = np.array(time_index)
    for hour in range(24):
        hour_indices = np.where((time_index % 24) == hour)[0]
        hourly_prec[hour] = np.mean(lon_mean_prec[hour_indices])
    
    plt.figure(figsize=(10, 8))
    plt.plot(range(24), hourly_prec, marker='o')
    plt.title(f'Diurnal Cycle of {month} {year}')
    plt.xlabel('Hour')
    plt.ylabel('Precipitation (mm)')
    
    # Salvando o gráfico
    plt.savefig(save_name)
    plt.close()

def calcular_ciclo_diurno(matriz_array):
    horas_dia = 24
    num_dias = matriz_array.shape[0] // horas_dia
    ciclo_diurno = np.zeros(horas_dia)

    for h in range(horas_dia):

        valores_hora = matriz_array[h::horas_dia]
        ciclo_diurno[h] = np.nanmean(valores_hora)
    
    return ciclo_diurno

def diurnal_cycle_Lorg(dataset, ciclo_diurno_Lorg, time_index, month, year, save_name):
    # Convertendo precipitação para mm/dia
    prec = dataset[time_index, :, :] * 1000
    lat_mean_prec = np.mean(prec, axis=2)
    lon_mean_prec = np.mean(lat_mean_prec, axis=1)

    hourly_prec = np.zeros(24)
    time_index = np.array(time_index)
    for hour in range(24):
        hour_indices = np.where((time_index % 24) == hour)[0]
        hourly_prec[hour] = np.mean(lon_mean_prec[hour_indices])

    fig, ax1 = plt.subplots(figsize=(10, 8))

    # Plot para Precipitação
    ax1.plot(range(24), hourly_prec, marker='o', color='b', label='Precipitation')
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Precipitation (mm)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # Criar o segundo eixo y para L_org
    ax2 = ax1.twinx()
    ax2.plot(range(24), ciclo_diurno_Lorg, marker='o', color='r', label='L_org', linestyle='--')
    ax2.set_ylabel('L_org', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    plt.title(f'Diurnal Cycle of {month} {year}')
    fig.tight_layout()

    plt.savefig(save_name)
    plt.close()

def diurnal_cycle_Lorg_panel(data_info_list, panel_save_name):
    fig, axs = plt.subplots(1, 3, figsize=(18, 6), sharey=False)

    for i, (dataset, ciclo_diurno_Lorg, time_index, month, year, save_name) in enumerate(data_info_list):
        prec = dataset[time_index, :, :] * 1000
        lat_mean_prec = np.mean(prec, axis=2)
        lon_mean_prec = np.mean(lat_mean_prec, axis=1)

        hourly_prec = np.zeros(24)
        time_index = np.array(time_index)
        for hour in range(24):
            hour_indices = np.where((time_index % 24) == hour)[0]
            hourly_prec[hour] = np.mean(lon_mean_prec[hour_indices])

        ax1 = axs[i]

        # Plot para Precipitação
        ax1.plot(range(24), hourly_prec, marker='o', color='b', label='Precipitation')
        ax1.set_xlabel('Hour')
        ax1.set_ylabel('Precipitation (mm)', color='b')
        ax1.tick_params(axis='y', labelcolor='b')

        # Criar o segundo eixo y para L_org
        ax2 = ax1.twinx()
        ax2.plot(range(24), ciclo_diurno_Lorg, marker='o', color='r', label='L_org', linestyle='--')
        ax2.set_ylabel('L_org', color='r')
        ax2.tick_params(axis='y', labelcolor='r')

        ax1.set_title(f'Diurnal Cycle of {month} {year}')
    
    fig.tight_layout()
    plt.savefig(panel_save_name)
    plt.close()
'''
def plot_multi_timeseries(dir_base, anos, meses, nome_arquivo, rawprec_era_month, *args, **kwargs):
    """
    Plota séries temporais para múltiplos anos e meses, utilizando a função
    plot_TimeSeries_L_org_precip.

    Args:
        dir_base (str): Diretório base dos arquivos.
        anos (list): Lista de anos.
        meses (list): Lista de meses.
        nome_arquivo (str): Padrão do nome do arquivo.
        func_ler (function): Função para ler os dados.
        *args: Outros argumentos para a função de plotar.
        **kwargs: Outros argumentos nomeados para a função de plotar.
    """

    for ano in anos:
        for mes in meses:
            arquivo = os.path.join(dir_base, nome_arquivo.format(ano=ano, mes=mes))
            L_org = ler_matriz(arquivo)
            plot_TimeSeries_L_org_precip(L_org, rawprec_era_month, mes, ano, f'plot_{ano}_{mes}.png')
'''
