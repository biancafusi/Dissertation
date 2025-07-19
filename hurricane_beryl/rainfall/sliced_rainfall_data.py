import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from netCDF4 import Dataset,date2num,num2date    
import datetime as dt

matplotlib.use("Agg")

# DEFINIÇÃO DOS EXPERIMENTOS

lonW, lonE, latS, latN = -106, -50, 10, 40

# initial_day = '2024-07-01T00'
initial_day = '2024-07-03T12'
final_day = '2024-07-09T00'

run_folder = '/mnt/beegfs/bianca.fusinato/monan/model/'

# where_to_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/rainfall_sliced_data/'

data_information = [
    ('ERA5', '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/x1.655362.era5_moist.nc'), #OK
    ('GSMaP', '/mnt/beegfs/bianca.fusinato/monan/comparison/JAXA/x1.655362.JAXA.nc'), #OK
    ('GPM-IMERG', '/mnt/beegfs/bianca.fusinato/monan/comparison/GPM/x1.655362.3B-HHR.MS.MRG.3IMERG.2024_01Z2906_24Z0909_1hour.nc' ), #OK
    ('CP-ON', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
    ('CP-OFF', run_folder+'beryl_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
    ('CP-1H', run_folder+'beryl_cporg1_gustf1_sub3d0_TCP1H_ERA5_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
    ('CP-3H', run_folder+'beryl_cporg1_gustf1_sub3d0_TCP3H_ERA5_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
    ('CP-D025', run_folder+'beryl_cporg1_gustf1_sub3d0_DOW025_ERA5_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
    ('CP-D050', run_folder+'beryl_cporg1_gustf1_sub3d0_DOW050_ERA5_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
    ('CPSS-ON', run_folder+'beryl_cporg1_gustf2_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
    ('CP-15km', '/mnt/beegfs/bianca.fusinato/monan/model/beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.2621442/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
    ('CP-60km', '/mnt/beegfs/bianca.fusinato/monan/model/beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.163842/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
    ('CP-GFS', '/mnt/beegfs/bianca.fusinato/monan/model/GFS_run/beryl_cporg1_gustf1_sub3d0_GFdef_GFS_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
    ('CP-29', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024062900/diag/only_precip_diag_dc.2024-06-29_00.00.00.nc'), #OK
    ('CP-02T12', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070212/diag/only_precip_diag_dc.2024-07-02_12.00.00.nc'),
    ('CP-1HD050', run_folder+'beryl_cporg1_gustf1_sub3d0_LT1HD050_ERA5_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc') #OK
]

where_to_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/sliced_rainfall_for_pdfs_cdfs/'

# dados na resolução nativa.
# where_to_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/native_resolution/'
# data_information = [
#     ('ERA5', '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/era5_moist.nc'), #OK
#     ('GSMap', '/mnt/beegfs/bianca.fusinato/monan/comparison/JAXA/JAXA_NATIVE_R.nc'), #OK
#     ('GPM-IMERG', '/mnt/beegfs/bianca.fusinato/monan/comparison/GPM/3B-HHR.MS.MRG.3IMERG.2024_01Z2906_24Z0909_1hour.nc4' ), #OK
#     ('CP-ON', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
#     ('CP-15km', '/mnt/beegfs/bianca.fusinato/monan/model/beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.2621442/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
#     ('CP-60km', '/mnt/beegfs/bianca.fusinato/monan/model/beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.163842/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'), #OK
# ]

# referência do tempo inicial
ref_time = np.datetime64(initial_day)

def creating_nc_files(label, lat_data, lon_data, rainfall):
    
    # criando um novo arquivo:
    ncfile = Dataset(where_to_save + f'{label}_hourly.nc',mode='w',format='NETCDF4_CLASSIC') 

    # dando um título para o arquivo:
    ncfile.title=f'Rainfall hourly {label} data'

    # dando as dimensões para o arquivo (obrigatorio):   
    ncfile.createDimension('time', len(rainfall.time)) 
    ncfile.createDimension('lat', len(lat_data))     # latitude axis
    ncfile.createDimension('lon', len(lon_data))    # longitude axis

    # criando as dimensões variáveis do arquivo:
    time = ncfile.createVariable('time', np.float64, ('time',))
    time.units = 'hours since 2024-07-03T12'
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


# TODOS RESOLUCAO MONAN MENOS 60km E 15km
for label, input_file_data in data_information:
    print(f'Processing {label} data...')
    
    if label == 'ERA5':

        dataset = xr.open_dataset(input_file_data).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'tp': 'rainfall'})
        time = dataset.time.sel(time=slice(initial_day,final_day))
        time_steps =  np.arange(0, len(time), 1)
        dataset_moist = (dataset.assign_coords(lon=((dataset.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')
        
        lat_data = np.round(dataset_moist.lat.sel(lat=slice(latS,latN)).values, 1)
        lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)

        rainfall = (dataset_moist.rainfall.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)) * 1000)
        print(rainfall)

        creating_nc_files(label, lat_data, lon_data, rainfall)

    elif label == 'GSMaP':
      
        dataset_moist = xr.open_dataset(input_file_data).rename({'latitude': 'lat', 'longitude': 'lon', 'precip': 'rainfall'}).transpose('time', 'lat', 'lon').sel(time=slice(initial_day,final_day))

        lat_data = np.round(dataset_moist.lat.sel(lat=slice(latS,latN)).values, 1) 
        lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)

        rainfall = ((dataset_moist.rainfall).sel(lat=slice(latS,latN), lon=slice(lonW, lonE)))
        print(rainfall)

        creating_nc_files(label, lat_data, lon_data, rainfall)
    
    elif label == 'GPM-IMERG':

        dataset_moist = xr.open_dataset(input_file_data).rename({'latitude': 'lat', 'longitude': 'lon', 'precipitation': 'rainfall'}).transpose('time', 'lat', 'lon').sel(time=slice(initial_day,final_day))

        lat_data = np.round(dataset_moist.lat.sel(lat=slice(latS,latN)).values, 1)
        lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)

        rainfall = (dataset_moist.rainfall.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)))
        print(rainfall)
        creating_nc_files(label, lat_data, lon_data, rainfall)
       
    else:
        
        dataset_moist = xr.open_dataset(input_file_data).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'}).sel(time=slice(initial_day, final_day), 
                                                                                                                             lat=slice(latS, latN), lon=slice(lonW, lonE))
        
        lat_data = np.round(dataset_moist.lat.values, 1)
        lon_data = np.round(dataset_moist.lon.values, 1)

        rainfall = dataset_moist.rainnc + dataset_moist.rainc

        print(rainfall)


        creating_nc_files(label, lat_data, lon_data, rainfall)

# for label, input_file_data in data_information:
#     print(f'Processing {label} data...')
    
#     if label == 'ERA5':

#         dataset = xr.open_dataset(input_file_data).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'tp': 'rainfall'})
#         time = dataset.time.sel(time=slice(initial_day,final_day))
#         time_steps =  np.arange(0, len(time), 1)
#         dataset_moist = (dataset.assign_coords(lon=((dataset.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')
        
#         lat_data = np.round(dataset_moist.lat.sel(lat=slice(latN,latS)).values, 1)
#         lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)

#         rainfall = (dataset_moist.rainfall.sel(lat=slice(latN,latS), lon=slice(lonW, lonE)) * 1000)
#         print(rainfall)
        
#         creating_nc_files(label, lat_data, lon_data, rainfall)
        
#     elif label == 'GSMap':

#         # FIZ UMA MODIFICAÇÃO PRA NATIVA RESOLUÇÂO: tirei latitude e longitude do rename, coloquei o assing

#         dataset_moist = xr.open_dataset(input_file_data).rename({'precip': 'rainfall'}).sel(time=time, method='nearest')
#         dataset_moist = dataset_moist.assign_coords(lon=((dataset_moist.lon + 180) % 360) - 180).sortby('lon')
    

#         lat_data = np.round(dataset_moist.lat.sel(lat=slice(latN,latS)).values, 1)
#         # lat_data = np.round(dataset_moist.lat.sel(lat=slice(latS,latN)).values, 1) # mudei
#         lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)
        
#         rainfall = ((dataset_moist.rainfall).sel(lat=slice(latN,latS), lon=slice(lonW, lonE))) # mudei

#         creating_nc_files(label, lat_data, lon_data, rainfall)
    
#     elif label == 'GPM-IMERG':

#         # FIZ UMA MODIFICAÇÃO PRA NATIVA RESOLUÇÂO: tirei latitude e longitude do rename

#         dataset_moist = xr.open_dataset(input_file_data).rename({'precipitation': 'rainfall'}).transpose('time', 'lat', 'lon').sel(time=time, method='nearest')

#         lat_data = np.round(dataset_moist.lat.sel(lat=slice(latS,latN)).values, 1)
#         lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)
        
#         rainfall = (dataset_moist.rainfall.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)))

#         creating_nc_files(label, lat_data, lon_data, rainfall)
    
#     else:
        
#         dataset_moist = xr.open_dataset(input_file_data).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'}).sel(time=slice(initial_day, final_day), 
#                                                                                                                              lat=slice(latS, latN), lon=slice(lonW, lonE))
        
#         lat_data = np.round(dataset_moist.lat.values, 1)
#         lon_data = np.round(dataset_moist.lon.values, 1)

#         rainfall = dataset_moist.rainnc + dataset_moist.rainc

#         creating_nc_files(label, lat_data, lon_data, rainfall)
