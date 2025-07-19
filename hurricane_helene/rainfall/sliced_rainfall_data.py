import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from netCDF4 import Dataset,date2num,num2date    
import datetime as dt

matplotlib.use("Agg")

from namelist_for_helene import *

'''
Faz um .nc file de um recorte da chuva horária.
'''

# referência do tempo inicial
ref_time = np.datetime64(initial_day)

def creating_nc_files(label, lat_data, lon_data, rainfall):
    
    # criando um novo arquivo:
    # ncfile = Dataset(f'/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/helene_rainfall_statistics/hourly_native_rainfall/{label}_hourly.nc',mode='w',format='NETCDF4_CLASSIC') 
    ncfile = Dataset(f'/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/helene_rainfall_statistics/helene_rainfall_sliced/{label}_hourly.nc',mode='w',format='NETCDF4_CLASSIC') 

    # dando um título para o arquivo:
    ncfile.title=f'Rainfall hourly {label} data'

    # dando as dimensões para o arquivo (obrigatorio):   
    ncfile.createDimension('time', len(rainfall.time)) 
    ncfile.createDimension('lat', len(lat_data))     # latitude axis
    ncfile.createDimension('lon', len(lon_data))    # longitude axis

    # criando as dimensões variáveis do arquivo:
    time = ncfile.createVariable('time', np.float64, ('time',))
    time.units = 'hours since 2024-09-25T00'
    time.long_name = 'time'

    lat = ncfile.createVariable('lat', np.float32, ('lat',))
    lat.units = 'degrees_north'
    lat.long_name = 'latitude'
    lon = ncfile.createVariable('lon', np.float32, ('lon',))
    lon.units = 'degrees_east'
    lon.long_name = 'longitude'

    # criando a variável chuva:
    rainfall_hourly = ncfile.createVariable('rainfall',np.float64,('time','lat','lon'))
    rainfall_hourly.units = 'mm/h' # degrees Kelvin
    rainfall_hourly.standard_name = 'rainfall_hourly'# this is a CF standard name

    # colocando a chuva, latitudes e longitudes dentro do novo arquivo:
    rainfall_hourly[:,:,:] = rainfall
    lat[:] = lat_data
    lon[:] = lon_data
    # diferença em horas
    time_hours = (rainfall.time.values - ref_time) / np.timedelta64(1, 'h')
    time[:] = time_hours

    ncfile.close(); print('Dataset is closed!')


# Configuration for MONAN resolution (EXCEPT cp-15km)

for label, input_file_data in data_information:
    print(f'Processing {label} data...')
    
    if label == 'ERA5':
        dataset_moist = xr.open_dataset(input_file_data).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'tp': 'rainfall'})
        time = dataset_moist.time.sel(time=slice(initial_day,final_day))
        
        lat_data = np.round(dataset_moist.lat.sel(lat=slice(latS,latN)).values, 1)
        lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)

        rainfall = (dataset_moist.rainfall.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)) * 1000)

        creating_nc_files(label, lat_data, lon_data, rainfall)
        
        
    elif label == 'GSMaP':

        dataset_moist = xr.open_dataset(input_file_data).rename({'latitude': 'lat', 'longitude': 'lon', 'precip': 'rainfall'}).transpose('time', 'lat', 'lon').sel(time=slice(initial_day, final_day))

        lat_data = np.round(dataset_moist.lat.sel(lat=slice(latS,latN)).values, 1) 
        lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)

        rainfall = ((dataset_moist.rainfall).sel(lat=slice(latS,latN), lon=slice(lonW, lonE)))

        creating_nc_files(label, lat_data, lon_data, rainfall)
    
    elif label == 'GPM-IMERG':

        dataset_moist = xr.open_dataset(input_file_data).rename({'latitude': 'lat', 'longitude': 'lon', 'precipitation': 'rainfall'}).transpose('time', 'lat', 'lon').sel(time=slice(initial_day, final_day))
        lat_data = np.round(dataset_moist.lat.sel(lat=slice(latS,latN)).values, 1)
        lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)

        rainfall = (dataset_moist.rainfall.sel(lat=slice(latS,latN), lon=slice(lonW, lonE))).transpose('time', 'lat', 'lon')

        creating_nc_files(label, lat_data, lon_data, rainfall)
    

    else:
        
        dataset_moist = xr.open_dataset(input_file_data).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'}).sel(time=slice(initial_day, final_day), 
                                                                                                                             lat=slice(latS, latN), lon=slice(lonW, lonE))
        
        lat_data = np.round(dataset_moist.lat.values, 1)
        lon_data = np.round(dataset_moist.lon.values, 1)

        rainfall = dataset_moist.rainnc + dataset_moist.rainc

        creating_nc_files(label, lat_data, lon_data, rainfall)
