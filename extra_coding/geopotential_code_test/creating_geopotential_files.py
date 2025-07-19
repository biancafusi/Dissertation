import xarray as xr
import numpy as np
from netCDF4 import Dataset   

from namelist_for_maps import *

from tracking_tool import *

ref_time = np.datetime64(initial_day)

# def creating_nc_files(label, lat_data, lon_data, geopotential_500, geopotential_700, tracking):
    
#     # criando um novo arquivo:
#     ncfile = Dataset(where_to_save + f'{label}_GEO+TRACKING_hourly.nc',mode='w',format='NETCDF4_CLASSIC') 

#     # dando um título para o arquivo:
#     ncfile.title=f'Cloud Top Temperature hourly {label} data'

#     # dando as dimensões para o arquivo (obrigatorio):   
#     ncfile.createDimension('time', len(geopotential_500.time)) 
#     ncfile.createDimension('lat', len(lat_data))     # latitude axis
#     ncfile.createDimension('lon', len(lon_data))    # longitude axis

#     # criando as dimensões variáveis do arquivo:
#     time = ncfile.createVariable('time', np.float64, ('time',))
#     time.units = 'hours since 2024-07-03T12'
#     time.long_name = 'time'

#     lat = ncfile.createVariable('lat', np.float32, ('lat',))
#     lat.units = 'degrees_north'
#     lat.long_name = 'latitude'
#     lon = ncfile.createVariable('lon', np.float32, ('lon',))
#     lon.units = 'degrees_east'
#     lon.long_name = 'longitude'

#     # criando as variaveis:
#     geopotential_500_hourly = ncfile.createVariable('geoph500',np.float64,('time','lat','lon'))
#     geopotential_500_hourly.units = 'm'
#     geopotential_500_hourly.standard_name = 'geopotential_height_500hpa'

#     geopotential_700_hourly = ncfile.createVariable('geoph700',np.float64,('time','lat','lon'))
#     geopotential_700_hourly.units = 'm'
#     geopotential_700_hourly.standard_name = 'geopotential_height_700hpa'
    
#     tracking_hourly = ncfile.createVariable('tracking',np.float64,('time','lat','lon'))
#     tracking_hourly.long_name = 'cyclone_tracking_mask'
#     tracking_hourly.units = '1'  # ou dimensionless

#     # colocando as variaveis, latitudes e longitudes dentro do novo arquivo:
#     geopotential_500_hourly[:,:,:] = geopotential_500
#     geopotential_700_hourly[:,:,:] = geopotential_700
#     tracking_hourly[:,:,:] = tracking
#     lat[:] = lat_data
#     lon[:] = lon_data
#     # diferença em horas
#     time_hours = (geopotential_500.time.values - ref_time) / np.timedelta64(1, 'h')
#     time[:] = time_hours

#     ncfile.close(); print('Dataset is closed!')
def creating_nc_files(label, lat_data, lon_data, geopotential_500, geopotential_700, track_lat, track_lon, track_times):
    from netCDF4 import Dataset
    import numpy as np

    ncfile = Dataset(where_to_save + f'{label}_GEO+TRACKING_hourly.nc', mode='w', format='NETCDF4_CLASSIC') 
    ncfile.title = f'Geopotential and Cyclone Track - {label}'

    # === Dimensões ===
    ncfile.createDimension('time', len(geopotential_500.time)) 
    ncfile.createDimension('lat', len(lat_data))     
    ncfile.createDimension('lon', len(lon_data))    
    ncfile.createDimension('time_track', len(track_times))  # <- trilha separada!

    # === Variáveis de coordenadas ===
    time = ncfile.createVariable('time', np.float64, ('time',))
    time.units = 'hours since 2024-07-03T12'
    time.long_name = 'time'

    lat = ncfile.createVariable('lat', np.float32, ('lat',))
    lat.units = 'degrees_north'
    lat.long_name = 'latitude'

    lon = ncfile.createVariable('lon', np.float32, ('lon',))
    lon.units = 'degrees_east'
    lon.long_name = 'longitude'

    # === Coordenadas da trilha ===
    time_track = ncfile.createVariable('time_track', np.float64, ('time_track',))
    time_track.units = 'hours since 2024-07-03T12'
    time_track.long_name = 'tracking time'

    lat_track = ncfile.createVariable('lat_track', np.float32, ('time_track',))
    lat_track.units = 'degrees_north'
    lat_track.long_name = 'cyclone_center_latitude'

    lon_track = ncfile.createVariable('lon_track', np.float32, ('time_track',))
    lon_track.units = 'degrees_east'
    lon_track.long_name = 'cyclone_center_longitude'

    # === Campos principais ===
    geopotential_500_hourly = ncfile.createVariable('geoph500', np.float64, ('time','lat','lon'))
    geopotential_500_hourly.units = 'm'
    geopotential_500_hourly.standard_name = 'geopotential_height_500hpa'

    geopotential_700_hourly = ncfile.createVariable('geoph700', np.float64, ('time','lat','lon'))
    geopotential_700_hourly.units = 'm'
    geopotential_700_hourly.standard_name = 'geopotential_height_700hpa'

    # === Preenchendo os dados ===
    geopotential_500_hourly[:, :, :] = geopotential_500
    geopotential_700_hourly[:, :, :] = geopotential_700

    lat[:] = lat_data
    lon[:] = lon_data
    time[:] = (geopotential_500.time.values - ref_time) / np.timedelta64(1, 'h')

    # Preenchendo trilha
    lat_track[:] = track_lat
    lon_track[:] = track_lon
    # Garante que estamos lidando com tempo absoluto real
    track_times_datetime = np.array([ref_time + np.timedelta64(t, 'h') for t in track_times], dtype='datetime64[h]')

    # Converte de volta para horas desde o ref_time (NetCDF-style)
    time_track[:] = (track_times_datetime - ref_time) / np.timedelta64(1, 'h')

    ncfile.close()
    print(f'NetCDF for {label} created and closed.')


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
    
    else:
        
        dataset = xr.open_dataset(input_file_data).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'}).sel(time=slice(initial_day, final_day), 
                                                                                                                               lat=slice(latS, latN), lon=slice(lonW, lonE))

        lat_data = np.round(dataset.lat.values, 1)
        lon_data = np.round(dataset.lon.values, 1)

        geopotential_500 = dataset.geoph_500hPa
        geopotential_700 = dataset.geoph_700hPa

        tracking_lat, tracking_lon, time_steps = tracking_tool(label, input_file_data)
        creating_nc_files(label, lat_data, lon_data, geopotential_500, geopotential_700, tracking_lat, tracking_lon, time_steps)

