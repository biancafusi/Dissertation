import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use('Agg')

'''
This code reads the .txt file and do some spatial plots.
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

def plot_TimeSeries_L_org(L_org):
    x = time

    plt.figure(figsize=(16, 4))
    plt.plot(x, L_org, label='ERA5')

    #plt.xlabel('X-axis Label')  # Customize as needed
    #plt.ylabel('L_org')  # Customize as needed
    #plt.title('L_org Comparison')
    #plt.legend()
    #plt.grid(True)
    plt.savefig('time_series.png')

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

def plot_TimeSeries_L_org(L_org):
    # Supondo que você tenha uma variável 'time' que representa o eixo x
    time = np.arange(len(L_org))  # Substitua por seus dados reais de tempo se disponíveis

    plt.figure(figsize=(16, 4))
    plt.plot(time, L_org, label='ERA5')
    plt.xlabel('Tempo')  # Customize conforme necessário
    plt.ylabel('L_org')  # Customize conforme necessário
    plt.title('Serie Temporal para Janeiro')
    plt.legend()
    plt.grid(True)
    plt.savefig('time_series.png')

file_ERA5 = '/home/bianca.fusinato/output/metrics/era5_metrics_varying.txt'
L_org_ERA5 =  ler_matriz(file_ERA5)
plot_TimeSeries_L_org(L_org_ERA5)