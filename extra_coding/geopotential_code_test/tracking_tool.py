import math
import xarray as xr
import numpy as np
import pandas as pd
import os

from namelist_for_maps import *

def tracking_tool(label, input_file_data):

    # Separacao dos dados de referencia, nesse caso os dados da NOAA
    NOAA = xr.open_dataset(NOAA_path)
    time_NOAA = NOAA.time.sel(time=slice(initial_day,final_day))
    NOAA_hourly = NOAA.sel(time=time_NOAA)
    lat_NOAA = NOAA_hourly.lat
    lon_NOAA = NOAA_hourly.lon
  
    # Guardar trilha do NOAA
    lat_points_NOAA, lon_points_NOAA, mslp_points_NOAA = [], [], []
    for t in range(0, len(time_NOAA), 1):
        lon_array_sel = lon_NOAA.isel(time=t)
        lat_array_sel = lat_NOAA.isel(time=t)
        lon_points_NOAA.append(lon_array_sel.values)
        lat_points_NOAA.append(lat_array_sel.values)

    print(f'Processing {label} data ...')
    
    if label == 'ERA5':
        # abrindo dados do ERA5
        dataset_dry = xr.open_dataset('/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/era5_dry.nc').rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'msl': 'mslp'})
        dataset_dry = (dataset_dry.assign_coords(lon=((dataset_dry.lon + 180) % 360) - 180).sortby('lon')).sel(time=time_NOAA, method='nearest')

        lat_data = dataset_dry.lat.sel(lat=slice(latN,latS))
        lon_data = dataset_dry.lon.sel(lon=slice(lonW, lonE))
        MSLP_data = dataset_dry.mslp.sel(lat=slice(latN,latS), lon=slice(lonW, lonE)) / 100  # to hPa

    else:
        model_data = (xr.open_dataset(input_file_data).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'})).sel(time=time_NOAA, lat=slice(latS, latN), lon=slice(lonW, lonE))
        lat_data = model_data.lat
        lon_data = model_data.lon
        MSLP_data = model_data.mslp / 100

    # Encontrar trilha do ciclone para esse dataset
    lat_points, lon_points, mslp_points, time_steps = [], [], [], []

    if label == 'CP-01':
        dlat, dlon = 10, 10
    elif label == 'CP-02T2':
        dlat, dlon = 8, 8
    elif label == 'CP-29':
        dlat, dlon = 4, 4
    else:
        dlat, dlon = 2.8, 2.8
    
    for t in range(len(time_NOAA)):
        MSLP_t = MSLP_data.isel(time=t)
        # Região de busca
        upper_lat, lower_lat = lat_points_NOAA[t] + dlat, lat_points_NOAA[t] - dlat
        left_lon, right_lon = lon_points_NOAA[t] - dlon, lon_points_NOAA[t] + dlon
        
        # Seleciona região
        lon_sliced = lon_data.sel(lon=slice(left_lon, right_lon))
        if label == 'ERA5':
            lat_sliced = lat_data.sel(lat=slice(upper_lat,lower_lat))
            MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(upper_lat, lower_lat))

        else:
            lat_sliced = lat_data.sel(lat=slice(lower_lat, upper_lat))
            MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(lower_lat, upper_lat))

        # Encontrar mínimo
        if MSLP_sliced.size > 0 and not np.isnan(MSLP_sliced).all():
            min_index = np.nanargmin(MSLP_sliced.values)
            lat_index, lon_index = np.unravel_index(min_index, MSLP_sliced.values.shape)
            lat_sel = lat_sliced.values[lat_index]
            lon_sel = lon_sliced.values[lon_index]
            lat_points.append(lat_sel)
            lon_points.append(lon_sel)
            # mslp_points.append(MSLP_sliced.values.ravel()[min_index])
            time_steps.append(t * 6) #aqui vezes 6 para ele salvar essa informação de 6h

    return(lat_points, lon_points, time_steps)



