import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xskillscore as xs
import matplotlib
from netCDF4 import Dataset    


from new_namelist_for_errors import *
matplotlib.use("Agg")

'''
Cria as files em formato .nc dos acumulados de chuva
'''

def creating_nc_files(label, lat_data, lon_data, rainfall):
    
    # criando um novo arquivo:
    ncfile = Dataset(f'{label}.nc',mode='w',format='NETCDF4_CLASSIC') 

    # dando um título para o arquivo:
    ncfile.title=f'Rainfall accumulated {label} data'

    # dando as dimensões para o arquivo (obrigatorio):    
    ncfile.createDimension('lat', len(lat_data))     # latitude axis
    ncfile.createDimension('lon', len(lon_data))    # longitude axis

    # criando as dimensões variáveis do arquivo:
    # espacial
    lat = ncfile.createVariable('lat', np.float32, ('lat',))
    lat.units = 'degrees_north'
    lat.long_name = 'latitude'
    lon = ncfile.createVariable('lon', np.float32, ('lon',))
    lon.units = 'degrees_east'
    lon.long_name = 'longitude'

    # criando a variável chuva:
    rainfall_acc = ncfile.createVariable('rainfall',np.float64,('lat','lon'))
    rainfall_acc.units = 'mm' # degrees Kelvin
    rainfall_acc.standard_name = 'rainfall_accumulated' # this is a CF standard name

    # colocando a chuva, latitudes e longitudes dentro do novo arquivo:
    rainfall_acc[:,:] = rainfall
    lat[:] = lat_data
    lon[:] = lon_data
    
    ncfile.close(); print('Dataset is closed!')


for label, color, input_file_data in data_information:
    print(f'Processing {label} data...')
    
    if label == 'ERA5':

        dataset = xr.open_dataset(input_file_data).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'tp': 'rainfall'})
        time = dataset.time.sel(time=slice(initial_day,final_day))
        time_steps =  np.arange(0, len(time), 1)
        dataset_moist = (dataset.assign_coords(lon=((dataset.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')
        
        lat_data = dataset_moist.lat.sel(lat=slice(latS,latN))
        lon_data = dataset_moist.lon.sel(lon=slice(lonW, lonE))

        rainfall = (dataset_moist.rainfall.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)) * 1000).sum(dim='time')
        
        creating_nc_files(label, lat_data, lon_data, rainfall)
        
    elif label == 'GSMap':

        dataset_moist = xr.open_dataset(input_file_data).rename({'latitude': 'lat', 'longitude': 'lon', 'precip': 'rainfall'}).transpose('time', 'lat', 'lon').sel(time=time, method='nearest')
        lat_data = dataset_moist.lat.sel(lat=slice(latS,latN))
        lon_data = dataset_moist.lon.sel(lon=slice(lonW, lonE))
        
        rainfall = ((dataset_moist.rainfall).sel(lat=slice(latS,latN), lon=slice(lonW, lonE))).sum(dim='time')

        creating_nc_files(label, lat_data, lon_data, rainfall)
    
    elif label == 'GPM-IMERG':

        dataset_moist = xr.open_dataset(input_file_data).rename({'latitude': 'lat', 'longitude': 'lon', 'precipitation': 'rainfall'}).transpose('time', 'lat', 'lon').sel(time=time, method='nearest')

        lat_data = dataset_moist.lat.sel(lat=slice(latS,latN))
        lon_data = dataset_moist.lon.sel(lon=slice(lonW, lonE))
        
        rainfall = (dataset_moist.rainfall.sel(lat=slice(latS,latN), lon=slice(lonW, lonE))).sum(dim='time')

        creating_nc_files(label, lat_data, lon_data, rainfall)
    
    else:
        
        dataset_moist = xr.open_dataset(input_file_data).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'}).sel(time=final_day, lat=slice(latS, latN), lon=slice(lonW, lonE))
        
        lat_data = dataset_moist.lat
        lon_data = dataset_moist.lon

        rainfall = dataset_moist.rainnc + dataset_moist.rainc

        creating_nc_files(label, lat_data, lon_data, rainfall)

