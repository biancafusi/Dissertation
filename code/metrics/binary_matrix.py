import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from percentile_data import *
'''
Made by: Bianca Fusinato
Get the percentiles and datasets to create binaty matrix
'''
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
    exit()
    
    return nova

def create_binary_matrix_and_plot(raw_data, threshold, output_dir, time_indices):
  """
  Creates binary matrices and plots based on a given threshold and saves them to a specified directory.

  Args:
    raw_data: The raw precipitation data.
    threshold: The threshold value.
    output_dir: The output directory.
    time_indices: A list of time indices.
  """
  for time_index in time_indices:
    process_ERA5_precipitation(raw_data, time_index, threshold, output_dir, f"cnv_ERA5_{time_index}.npy")
    print(f"The binary matrix and plot for time_index {time_index} have been saved to {output_dir}")

threshold_dict = {
    "january": 1.979,
    "february": 2.094,
    "march":2.1798,
    "august":0.306,
    "september":0.280,
    "october":0.8366
}

output_dir_dict = {
    "january2013": "/home/bianca.fusinato/output/binary_matrix/january2013/",
    "january2014": "/home/bianca.fusinato/output/binary_matrix/january2014/",
    "january2015": "/home/bianca.fusinato/output/binary_matrix/january2015/",
    "february2013":'/home/bianca.fusinato/output/binary_matrix/february2013',
    "february2014":'/home/bianca.fusinato/output/binary_matrix/february2014',
    "february2015":'/home/bianca.fusinato/output/binary_matrix/february2015',
    "march2013": "/home/bianca.fusinato/output/binary_matrix/march2013/",
    "march2014": "/home/bianca.fusinato/output/binary_matrix/march2014/",
    "march2015": "/home/bianca.fusinato/output/binary_matrix/march2015/",
    "august2013": "/home/bianca.fusinato/output/binary_matrix/august2013/",
    "august2014": "/home/bianca.fusinato/output/binary_matrix/august2014/",
    "august2015": "/home/bianca.fusinato/output/binary_matrix/august2015/",
    "september2013": "/home/bianca.fusinato/output/binary_matrix/september2013/",
    "september2014": "/home/bianca.fusinato/output/binary_matrix/september2014/",
    "september2015": "/home/bianca.fusinato/output/binary_matrix/september2015/",
    "october2013": "/home/bianca.fusinato/output/binary_matrix/october2013/",
    "october2014": "/home/bianca.fusinato/output/binary_matrix/october2014/",
    "october2015": "/home/bianca.fusinato/output/binary_matrix/october2015/"
    
}

time_indices_dict = {
    "january": range(0, 744),
    "february": range(0, 672),
    "march": range(0, 744),
    "august": range(0, 744),
    "september": range(0, 720),
    "october": range(0, 744),
}

# Processing ERA5 data:
create_binary_matrix_and_plot(rawprec_era_january_2013, threshold_dict["january"], output_dir_dict["january2013"], time_indices_dict["january"])
create_binary_matrix_and_plot(rawprec_era_january_2014, threshold_dict["january"], output_dir_dict["january2014"], time_indices_dict["january"])
create_binary_matrix_and_plot(rawprec_era_january_2015, threshold_dict["january"], output_dir_dict["january2015"], time_indices_dict["january"])

create_binary_matrix_and_plot(rawprec_era_february_2013, threshold_dict["february"], output_dir_dict["february2013"], time_indices_dict["february"])
create_binary_matrix_and_plot(rawprec_era_february_2014, threshold_dict["february"], output_dir_dict["february2014"], time_indices_dict["february"])
create_binary_matrix_and_plot(rawprec_era_february_2015, threshold_dict["february"], output_dir_dict["february2015"], time_indices_dict["february"])

create_binary_matrix_and_plot(rawprec_era_march_2013, threshold_dict["march"], output_dir_dict["march2013"], time_indices_dict["march"])
create_binary_matrix_and_plot(rawprec_era_march_2014, threshold_dict["march"], output_dir_dict["march2014"], time_indices_dict["march"])
create_binary_matrix_and_plot(rawprec_era_march_2015, threshold_dict["march"], output_dir_dict["march2015"], time_indices_dict["march"])

create_binary_matrix_and_plot(rawprec_era_august_2013, threshold_dict["august"], output_dir_dict["august2013"], time_indices_dict["august"])
create_binary_matrix_and_plot(rawprec_era_august_2014, threshold_dict["august"], output_dir_dict["august2014"], time_indices_dict["august"])
create_binary_matrix_and_plot(rawprec_era_august_2015, threshold_dict["august"], output_dir_dict["august2015"], time_indices_dict["august"])

create_binary_matrix_and_plot(rawprec_era_september_2013, threshold_dict["september"], output_dir_dict["september2013"], time_indices_dict["september"])
create_binary_matrix_and_plot(rawprec_era_september_2014, threshold_dict["september"], output_dir_dict["september2014"], time_indices_dict["september"])
create_binary_matrix_and_plot(rawprec_era_september_2015, threshold_dict["september"], output_dir_dict["september2015"], time_indices_dict["september"])

create_binary_matrix_and_plot(rawprec_era_october_2013, threshold_dict["october"], output_dir_dict["october2013"], time_indices_dict["october"])
create_binary_matrix_and_plot(rawprec_era_october_2014, threshold_dict["october"], output_dir_dict["october2014"], time_indices_dict["october"])
create_binary_matrix_and_plot(rawprec_era_october_2015, threshold_dict["october"], output_dir_dict["october2015"], time_indices_dict["october"])