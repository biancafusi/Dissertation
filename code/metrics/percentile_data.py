import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import os
from datetime import datetime, timedelta
import calendar
'''
Made by: Bianca Fusinato
This codes takes the precipitation data, calculates 
the histogram saving into graphs and the percentiles in a .txt file
The variables can be used on the others programs, such as binary_matrix.py,
metrics_text.py and plot_metrics_txt.py
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

def plot_histograms(data, type):
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

def calculate_percentiles(vector, output_file):
    vector = np.nan_to_num(vector)
    percentiles = list(range(10, 100, 1))
    values_percentiles = np.percentile(vector, percentiles)
    with open(output_file, 'w') as f:
        for p, val in zip(percentiles, values_percentiles):
            f.write(f"Percentile {p}: {val}\n")

def calculate_monthly_percentiles(era5_path, year, month):
  """
  Calcula percentis de precipitação ERA5 para um mês específico.

  Args:
      era5_path (str): Caminho para o arquivo netcdf ERA5.
      year (int): Ano.
      month (int): Mês (1-12).

  Returns:
      numpy.array: Dados brutos de precipitação para o mês especificado.
  """
  num_days = calendar.monthrange(year, month)[1]
  start_date = f'{year}-{month:02d}-01'
  end_date = f'{year}-{month:02d}-{num_days}'
  month_dates = generate_date_list(start_date, end_date)

  era_month = load_ERA5_prec_datasets(era5_path, month_dates)
  rawprec_era_month = era_month['tp']
  prec_era_month = rawprec_era_month.values * 1000
  prec_month = prec_era_month.flatten()
  calculate_percentiles(prec_month, f'/home/bianca.fusinato/output/percentile/{month:02d}{year}_percentile.txt')

  return rawprec_era_month

era5_path_2013 = '/home/bianca.fusinato/caracterization_data/era5_2013CARAC.nc'
era5_path_2014_JF = '/home/bianca.fusinato/caracterization_data/era5_JF2014CARAC.nc'
era5_path_2014_MASO = '/home/bianca.fusinato/caracterization_data/era5_MASO2014CARAC.nc'
era5_path_2015 = '/home/bianca.fusinato/caracterization_data/era5_2015CARAC.nc'

# Processing ERA5 data:
rawprec_era_january_2013 = calculate_monthly_percentiles(era5_path_2013, 2013, 1)
rawprec_era_february_2013 = calculate_monthly_percentiles(era5_path_2013, 2013, 2)
rawprec_era_march_2013 = calculate_monthly_percentiles(era5_path_2013, 2013, 3)
rawprec_era_august_2013 = calculate_monthly_percentiles(era5_path_2013, 2013, 8)
rawprec_era_september_2013 = calculate_monthly_percentiles(era5_path_2013, 2013, 9)
rawprec_era_october_2013 = calculate_monthly_percentiles(era5_path_2013, 2013, 10)

rawprec_era_january_2014 = calculate_monthly_percentiles(era5_path_2014_JF, 2014, 1)
rawprec_era_february_2014 = calculate_monthly_percentiles(era5_path_2014_JF, 2014, 2)
rawprec_era_march_2014 = calculate_monthly_percentiles(era5_path_2014_MASO, 2014, 3)
rawprec_era_august_2014 = calculate_monthly_percentiles(era5_path_2014_MASO, 2014, 8)
rawprec_era_september_2014 = calculate_monthly_percentiles(era5_path_2014_MASO, 2014, 9)
rawprec_era_october_2014 = calculate_monthly_percentiles(era5_path_2014_MASO, 2014, 10)

rawprec_era_january_2015 = calculate_monthly_percentiles(era5_path_2015, 2015, 1)
rawprec_era_february_2015 = calculate_monthly_percentiles(era5_path_2015, 2015, 2)
rawprec_era_march_2015 = calculate_monthly_percentiles(era5_path_2015, 2015, 3)
rawprec_era_august_2015 = calculate_monthly_percentiles(era5_path_2015, 2015, 8)
rawprec_era_september_2015 = calculate_monthly_percentiles(era5_path_2015, 2015, 9)
rawprec_era_october_2015 = calculate_monthly_percentiles(era5_path_2015, 2015, 10)







