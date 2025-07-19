import xarray as xr
import numpy as np
import pandas as pd
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

# where_to_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/ctt_datasets/'
where_to_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/ctt_native_resolution/'

# data_information = [
#     # ('ERA5', '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/x1.655362.era5_moist.nc'), #OK
#     ('GPM-MERGIR', '/mnt/beegfs/bianca.fusinato/monan/comparison/MERGIR/merg_2024070703_0703_x1.655362.nc' ), # trocar aqui pro mergir
#     ('CP-ON', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
#     ('CP-OFF', run_folder+'beryl_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
#     ('CP-1H', run_folder+'beryl_cporg1_gustf1_sub3d0_TCP1H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
#     ('CP-3H', run_folder+'beryl_cporg1_gustf1_sub3d0_TCP3H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
#     ('CP-D025', run_folder+'beryl_cporg1_gustf1_sub3d0_DOW025_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
#     ('CP-D050', run_folder+'beryl_cporg1_gustf1_sub3d0_DOW050_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
#     ('CPSS-ON', run_folder+'beryl_cporg1_gustf2_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
#     ('CP-15km', '/mnt/beegfs/bianca.fusinato/monan/comparison/beryl_15km/15km_all_diag_dc.2024-07-03_00.00.00.nc_x1.655362.nc'), #OK
#     ('CP-60km', '/mnt/beegfs/bianca.fusinato/monan/comparison/beryl_60km/60km_all_diag_dc.2024-07-03_00.00.00.nc_x1.655362.nc'), #OK
#     ('CP-GFS', '/mnt/beegfs/bianca.fusinato/monan/model/GFS_run/beryl_cporg1_gustf1_sub3d0_GFdef_GFS_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
#     ('CP-29', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024062900/diag/all_diag_dc.2024-06-29_00.00.00.nc'), #OK
#     ('CP-02T12', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070212/diag/all_diag_dc.2024-07-02_12.00.00.nc'),
#     ('CP-1HD050', run_folder+'beryl_cporg1_gustf1_sub3d0_LT1HD050_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc') #OK
# ]

# RESOLUÇÃO NATIVA:
data_information = [
    # ('ERA5', '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/x1.655362.era5_moist.nc'), #OK
    # ('GPM-MERGIR', '/mnt/beegfs/bianca.fusinato/monan/comparison/MERGIR/merg_2024070703_0703_4km-pixel.nc4' ), # trocar aqui pro mergir
    # ('CP-ON', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
    # ('CP-15km', '/mnt/beegfs/bianca.fusinato/monan/model/beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.2621442/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
    ('CP-60km', '/mnt/beegfs/bianca.fusinato/monan/model/beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.163842/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc')
    ]

# where_to_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/native_resolution/'

# # dados na resolução nativa.
# data_information = [
#     ('ERA5', '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/era5_moist.nc'), #OK
#     ('GSMap', '/mnt/beegfs/bianca.fusinato/monan/comparison/JAXA/JAXA_NATIVE_R.nc'), #OK
#     ('GPM-IMERG', '/mnt/beegfs/bianca.fusinato/monan/comparison/GPM/3B-HHR.MS.MRG.3IMERG.2024_01Z2906_24Z0909_1hour.nc4' ), #OK
#     ('CP-ON', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
#     ('CP-15km', '/mnt/beegfs/bianca.fusinato/monan/model/beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.2621442/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
#     ('CP-60km', '/mnt/beegfs/bianca.fusinato/monan/model/beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.163842/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'), #OK
# ]

# referência do tempo inicial
ref_time = np.datetime64(initial_day)

def creating_nc_files(label, lat_data, lon_data, variable_want_to_save):
    
    # criando um novo arquivo:
    ncfile = Dataset(where_to_save + f'{label}_hourly.nc',mode='w',format='NETCDF4_CLASSIC') 

    # dando um título para o arquivo:
    ncfile.title=f'Cloud Top Temperature hourly {label} data'

    # dando as dimensões para o arquivo (obrigatorio):   
    ncfile.createDimension('time', len(variable_want_to_save.time)) 
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
    variable_hourly = ncfile.createVariable('ctt',np.float64,('time','lat','lon'))
    variable_hourly.units = '°C'
    variable_hourly.standard_name = 'cloud_top_temperature'# this is a CF standard name

    # colocando a chuva, latitudes e longitudes dentro do novo arquivo:
    variable_hourly[:,:,:] = variable_want_to_save
    lat[:] = lat_data
    lon[:] = lon_data
    # diferença em horas
    time_hours = (variable_want_to_save.time.values - ref_time) / np.timedelta64(1, 'h')
    time[:] = time_hours

    ncfile.close(); print('Dataset is closed!')


for label, input_file_data in data_information:
    print(f'Processing {label} data...')
    
    if label == 'ERA5':
        print('preciso baixar esse dado!')
        # dataset = xr.open_dataset(input_file_data).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon'})
        # print(dataset)
        # exit()
        # time = dataset.time.sel(time=slice(initial_day,final_day))
        # time_steps =  np.arange(0, len(time), 1)
        # dataset_moist = (dataset.assign_coords(lon=((dataset.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')
        
        # lat_data = np.round(dataset_moist.lat.sel(lat=slice(latN,latS)).values, 1)
        # lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)

        # rainfall = (dataset_moist.rainfall.sel(lat=slice(latN,latS), lon=slice(lonW, lonE)) * 1000)
        # print(rainfall)
        
        # creating_nc_files(label, lat_data, lon_data, rainfall)
    
    elif label == 'GPM-MERGIR':

        dataset_moist = xr.open_dataset(input_file_data).rename({'Tb': 'ctt'}).sel(time=slice(initial_day, final_day))

        lat_data = np.round(dataset_moist.lat.sel(lat=slice(latS,latN)).values, 1)
        lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)
        
        variable = (dataset_moist.ctt.sel(lat=slice(latS,latN), lon=slice(lonW, lonE))) - 273.15 # transformando para celsius

        creating_nc_files(label, lat_data, lon_data, variable)
    
    else:
        
        dataset_moist = xr.open_dataset(input_file_data).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'}).sel(time=slice(initial_day, final_day), 
                                                                                                                               lat=slice(latS, latN), lon=slice(lonW, lonE))

        lat_data = np.round(dataset_moist.lat.values, 1)
        lon_data = np.round(dataset_moist.lon.values, 1)

        variable = dataset_moist.ctt

        creating_nc_files(label, lat_data, lon_data, variable)
