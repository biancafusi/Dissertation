import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import seaborn as sns

'''
This code reads the .txt file and do some histograms plots.
'''

def read_txt_files(nome_arquivo, indice):
    valores = {}
    try:
        with open(nome_arquivo, 'r') as file:
            for linha in file:
                if linha.startswith(f'Indice {indice}:'):
                    for _ in range(4):
                        linha = next(file).strip()
                        chave, valor = linha.split(': ')
                        valores[chave.strip()] = float(valor)
                    break
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
    return valores

def extract_metrics(file_path):
    L_org = []
    for indice in range(240):
        valores = read_txt_files(file_path, indice)
        if valores:
            #RI_org.append(valores.get('RI_org', None))
            L_org.append(valores.get('L_org', None))
        else:
            #RI_org.append(None)
            L_org.append(None)
    return L_org

def extract_IORG_metric(file_path):
    I_org = []
    for indice in range(240):
        valores = read_txt_files(file_path, indice)
        if valores:
            I_org.append(valores.get('I_org', None))
        else:
            I_org.append(None)
    return I_org

def plot_and_save_histogram(L_org, prefix, bin_edges):
    L_org = np.array([0 if x is None else x for x in L_org])

    plt.figure(figsize=(16, 4))

    counts, edges, patches = plt.hist(L_org, bins=bin_edges, density=False, label=f'$L_{{org}}$ {prefix}', color='orange', edgecolor='black')
    
    plt.ylabel('Frequency')
    plt.xlabel('Value of the metric')
    plt.title(f'Histogram for {prefix}')
    plt.legend(loc='upper right')

    total_count = np.sum(counts)
    

    for count, edge in zip(counts, edges[:-1]):
        if count > 0:
            percentage = (count / total_count) * 100
            plt.text(edge + (edges[1] - edges[0]) / 2, count, f'{percentage:.1f}%', ha='center', va='bottom', fontsize=8)

    y_ticks = np.arange(0, max(counts) + 5, 5)
    plt.yticks(y_ticks)

    plt.savefig(f'{prefix}_histogram.png')
    plt.close()

def plot_Iorg_histogram(I_org, prefix, bin_edges):
    I_org = np.array([0 if x is None else x for x in I_org])

    plt.figure(figsize=(16, 4))

    counts, edges, patches = plt.hist(I_org, bins=bin_edges,density=False, label=f'$I_{{org}}$ {prefix}', alpha=0.5, color='red', edgecolor='black')
    
    plt.ylabel('Frequency')
    plt.xlabel('Value of the metric')
    plt.title(f'Histogram for {prefix}')
    plt.legend(loc='upper right')

    total_count = np.sum(counts)
    
    for count, edge in zip(counts, edges[:-1]):
        if count > 0:
            percentage = (count / total_count) * 100
            plt.text(edge + (edges[1] - edges[0]) / 2, count, f'{percentage:.1f}%', ha='center', va='bottom', fontsize=8)

    y_ticks = np.arange(0, max(counts) + 5, 5)
    plt.yticks(y_ticks)

    plt.savefig(f'{prefix}_Iorg_histogram.png')
    plt.close()

def comparison_histogram(L_org1,L_org2,L_org3,L_org4, bin_edges):
    L_org1 = np.array([0 if x is None else x for x in L_org1])
    L_org2 = np.array([0 if x is None else x for x in L_org2])
    L_org3 = np.array([0 if x is None else x for x in L_org3])
    L_org4 = np.array([0 if x is None else x for x in L_org4])

    plt.figure(figsize=(16, 4))

    counts, edges, patches = plt.hist(L_org1, bins=bin_edges, density=False, color='red', edgecolor='black')
    #counts, edges, patches = plt.hist(L_org2, bins=bin_edges, histtype='step', density=False, color='blue', edgecolor='black')
    counts, edges, patches = plt.hist(L_org3, bins=bin_edges, density=False, alpha=0.5, color='green', edgecolor='black')
    #counts, edges, patches = plt.hist(L_org4, bins=bin_edges, histtype='step', density=False, color='yellow', edgecolor='black')
    
    plt.ylabel('Frequency')
    plt.xlabel('Value of the metric')
    plt.title(f'Histogram for all the types of data')
    
    total_count = np.sum(counts)

    for count, edge in zip(counts, edges[:-1]):
        if count > 0:
            percentage = (count / total_count) * 100
            plt.text(edge + (edges[1] - edges[0]) / 2, count, f'{percentage:.1f}%', ha='center', va='bottom', fontsize=8)

    y_ticks = np.arange(0, max(counts) + 5, 5)
    plt.yticks(y_ticks)

    #plt.legend([f'$L_{{org}}$ {prefix}'], loc='upper right')
    plt.savefig(f'all_histogram.png')
    plt.close()


def clean_data(metric):
    return [x for x in metric if x is not None]

def plot_boxplot_metrics(metric1, metric2, metric3, metric4, labels):
    # Limpar os dados para remover valores None
    data = [clean_data(metric1), clean_data(metric2), clean_data(metric3), clean_data(metric4)]

    # Calcular as médias
    means = [np.mean(metric) for metric in data]

    # Criar o box-plot usando seaborn
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data)
    
    for i, mean in enumerate(means):
        plt.scatter(i, mean, color='white', zorder=5)
        
    plt.xticks(ticks=np.arange(len(labels)), labels=labels)
    plt.title('Comparação de Métricas entre Datasets')
    plt.xlabel('Dataset')
    plt.ylabel('Valor da Métrica')
    
    # Mostrar a legenda apenas uma vez
    red_patch = plt.Line2D([0], [0], marker='o', color='red', markerfacecolor='red', markersize=10, label='Média')
    plt.legend(handles=[red_patch])

    # Mostrar o gráfico
    plt.savefig('box_plot.png')
    plt.show()

def calcular_percentis(amostra, output_file):
    amostra = clean_data(amostra)
    amostra = np.nan_to_num(amostra)
    percentis = list(range(10, 100, 1))
    valores_percentis = np.percentile(amostra, percentis)
    with open(output_file, 'w') as f:
        for p, val in zip(percentis, valores_percentis):
            f.write(f"Percentil {p}: {val}\n")

file_GPM = '/home/bianca/Documents/master_code/dataout/metrics/gpm_metrics.txt'
file_ERA5 = '/home/bianca/Documents/master_code/dataout/metrics/era5_metrics.txt'
file_CP = '/home/bianca/Documents/master_code/dataout/metrics/cp_metrics.txt'
file_OFF = '/home/bianca/Documents/master_code/dataout/metrics/off_metrics.txt'

L_org_GPM = np.array(extract_metrics(file_GPM))
L_org_ERA5 =  np.array(extract_metrics(file_ERA5))
L_org_CP =  np.array(extract_metrics(file_CP))
L_org_OFF =  np.array(extract_metrics(file_OFF))

I_org_GPM=np.array(extract_IORG_metric(file_GPM))
I_org_ERA5=np.array(extract_IORG_metric(file_ERA5))
I_org_CP=np.array(extract_IORG_metric(file_CP))
I_org_OFF=np.array(extract_IORG_metric(file_OFF))
'''
# Histograms
bin_edges = np.linspace(0, 0.02, num=30, endpoint=True, retstep=False, dtype=None, axis=0)
plot_and_save_histogram(L_org_GPM, 'GPM', bin_edges)
plot_and_save_histogram(L_org_ERA5, 'ERA5', bin_edges)
plot_and_save_histogram(L_org_CP, 'CP', bin_edges)
plot_and_save_histogram(L_org_OFF, 'OFF', bin_edges)

bin_edges2 = np.linspace(0, 1, num=30, endpoint=True, retstep=False, dtype=None, axis=0)
plot_Iorg_histogram(I_org_GPM,'GPM',bin_edges2)
plot_Iorg_histogram(I_org_ERA5,'ERA5',bin_edges2)
plot_Iorg_histogram(I_org_CP,'CP',bin_edges2)
plot_Iorg_histogram(I_org_OFF,'OFF',bin_edges2)
'''
# Box-plots
#plot_boxplot_metrics(L_org_GPM, L_org_ERA5, L_org_CP, L_org_OFF, ['GPM', 'ERA5', 'CP', 'OFF'])
#plot_boxplot_metrics(I_org_GPM, I_org_ERA5, I_org_CP, I_org_OFF, ['GPM', 'ERA5', 'CP', 'OFF'])

# Percentiles
calcular_percentis(L_org_GPM, 'percentile_GPM.txt')
calcular_percentis(L_org_ERA5,'percentile_ERA5.txt')
calcular_percentis(L_org_CP,'percentile_CP.txt')
calcular_percentis(L_org_OFF,'percentile_OFF.txt')