import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from percentile_data import rawprec_eraJ, prec_eraF

matplotlib.use('Agg')

def process_GPM_precipitation(dataset_path, time_index, threshold, output_path, save_name):
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"O arquivo {dataset_path} não foi encontrado.")

    ds_GPM = xr.open_dataset(dataset_path, engine='netcdf4')
    #ds_GPM = ds.transpose('time', 'latitude', 'longitude')
   
    if 'precip_media' not in ds_GPM.variables:
        raise ValueError("A variável 'precip_media' não está presente no dataset.")
    
    prec_01 = ds_GPM.precip_media[time_index, :, :]
    prec = prec_01.transpose('lat', 'lon')
    latitudes = prec.lat
    longitudes = prec.lon

    ny, nx = len(latitudes), len(longitudes)
    nova = np.zeros((ny, nx), dtype=int)

    for i in range(ny):
        for j in range(nx):
            valor_prec = prec.values[i][j]
            if valor_prec > threshold:
                nova[i, j] = 1
            else:
                nova[i, j] = 0

    matrix_path = os.path.join(output_path, save_name)
    np.save(matrix_path, nova)
    
    return nova

def process_ERA5_precipitation(dataset, time_index, threshold, output_path,  save_name):
    prec = dataset[time_index,:,:]*1000
    latitudes = dataset.latitude
    longitudes = dataset.longitude

    ny, nx = len(latitudes), len(longitudes)
    nova = np.zeros((ny, nx), dtype=int)

    for i in range(ny):
        for j in range(nx):
            valor_prec = prec.values[i][j]
            if valor_prec > threshold:
                nova[i, j] = 1
            else:
                nova[i, j] = 0

    plt.figure(figsize=(10, 8))
    plt.pcolormesh(longitudes, latitudes, nova, cmap='gray', shading='auto')
    plt.title('Matriz de Precipitação Transformada')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    plot_path = os.path.join(output_path, save_name.replace('.npy', '.png'))
    plt.savefig(plot_path)
    plt.close()

    matrix_path = os.path.join(output_path, save_name)
    np.save(matrix_path, nova)
    
    return nova

def process_BRAMS_precipitation(dataset_path, time_index, threshold, output_path,  save_name):
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"O arquivo {dataset_path} não foi encontrado.")
    
    ds = xr.open_dataset(dataset_path, engine='netcdf4')
    if 'totprec' not in ds.variables:
        raise ValueError("A variável 'totprec' não está presente no dataset.")

    prec = ds.totprec[time_index, :, :]

    latitudes = prec.lat
    longitudes = prec.lon

    ny, nx = len(latitudes), len(longitudes)
    nova = np.zeros((ny, nx), dtype=int)

    for i in range(ny):
        for j in range(nx):
            valor_prec = prec.values[i][j]
            if valor_prec > threshold:
                nova[i, j] = 1
            else:
                nova[i, j] = 0

    plt.figure(figsize=(10, 8))
    plt.pcolormesh(longitudes, latitudes, nova, cmap='gray', shading='auto')
    plt.title('Matriz de Precipitação Transformada')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    plot_path = os.path.join(output_path, save_name.replace('.npy', '.png'))
    plt.savefig(plot_path)
    plt.close()

    matrix_path = os.path.join(output_path, save_name)
    np.save(matrix_path, nova)
    
    return nova

threshold = 1.979

#output_directory_GPM = '/home/bianca/Documents/master_code/dataout/bin_matrix_GPM_resolution/gpm/'
output_directory_ERA5 = '/home/bianca.fusinato/output/binary_matrix/era5J/'

january = [
    range(0,744)
]
february = [
    range(0,673)
]

for indices in january:
    for time_index in indices:
        #save_name_GPM = f'cnv_GPM_{time_index}.npy'
        save_name_ERA5 = f'cnv_ERA5_{time_index}.npy'
        
        #matriz_resultado_GPM = process_GPM_precipitation(dataset_path_GPM, time_index, threshold, output_directory_GPM, save_name_GPM)
        matriz_resultado_ERA5 = process_ERA5_precipitation(rawprec_eraJ, time_index, threshold, output_directory_ERA5, save_name_ERA5)
        
        print(f'The matrices and plots for time_index {time_index} have been saved')


