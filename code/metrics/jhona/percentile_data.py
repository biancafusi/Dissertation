import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import os
from datetime import datetime, timedelta
'''
Made by: Bianca Fusinato
This codes takes the precipitation data, calculates 
the histogram saving into graphs and the percentiles in a .txt file
'''

def load_ERA5_prec_datasets(ds_path, dates):
    datasets = []
    
    if os.path.exists(ds_path):
        ds = xr.open_dataset(ds_path, engine='netcdf4')
        if 'tp' not in ds.variables:
            raise ValueError("tp isnt on the dataset.")
        
        for date in dates:
            dp = ds.sel(time=date)
            #dp_prec = dp.tp * 1000
            datasets.append(dp)
        
        combined_dataset = xr.concat(datasets, dim='time')
        return combined_dataset
    else:
        print(f"Arquivo não encontrado: {ds_path}")
        return None

def generate_date_list(start_date, end_date):
    dates = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    
    return dates

def plotagem_histogramas(data, type):
    data = np.nan_to_num(data)
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=100, edgecolor='black', log=True)
    plt.title(f'Histograma de Precipitação {type} (Escala Logarítmica)')
    plt.xlabel('Precipitação (mm/h)')
    plt.xticks(np.arange(0, max(data)+1, 1))
    plt.ylabel('Frequência (log escala)')
    plt.savefig(f'histograma_precip_log_{type}.png')
    plt.close()
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=100, edgecolor='black')
    plt.title(f'Histograma de Precipitação {type}')
    plt.xlabel('Precipitação (mm/h)')
    plt.xticks(np.arange(0, max(data)+1, 1))
    plt.ylabel('Frequência')
    plt.grid(True, which="both", ls="--")
    plt.savefig(f'histograma_precip_{type}.png')
    plt.close()

def calcular_percentis(vetor, output_file):
    vetor = np.nan_to_num(vetor)
    percentis = list(range(10, 100, 1))
    valores_percentis = np.percentile(vetor, percentis)
    with open(output_file, 'w') as f:
        for p, val in zip(percentis, valores_percentis):
            f.write(f"Percentil {p}: {val}\n")

era5_path = '/home/bianca.fusinato/caracterization_data/era5JF2014CARAC.nc'

january = generate_date_list('2014-01-01', '2014-01-31')
february = generate_date_list('2014-02-01','2014-02-28')

eraJ = load_ERA5_prec_datasets(era5_path, january)
rawprec_eraJ = eraJ['tp']
prec_eraJ = rawprec_eraJ.values*1000
eraJ_prec = prec_eraJ.flatten()

eraF = load_ERA5_prec_datasets(era5_path, february)
rawprec_eraF = eraF['tp']
prec_eraF = rawprec_eraF.values*1000
eraF_prec = prec_eraF.flatten()


calcular_percentis(eraJ_prec, 'eraJ_percentis.txt')
calcular_percentis(eraF_prec, 'eraF_percentis.txt')


