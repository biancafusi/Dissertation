import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

import numpy as np
import matplotlib

from namelist_for_pathing import *

matplotlib.use("Agg")

'''
VERSION: WITH A BOX AROUND MSLP NOAA DATA!

Developed by Bianca Fusinato.
READ ME:        
            The code logic is described as follows:
            Get all the data at the same time period;
            Save all the data into one dataset;
            Plot the minimum value of MSLP into simple xy graph of each dataset;
            Insert a time legend into the reference data.

Obs.: One could modify the 'Preparing the data' part in other to adequate to one's data
Obs.2: One could modify the logic to get the minimum MSLP values
Obs.3: The default color for the experiment line in the graph is red, but can be changed
'''

############################ PREPARING THE DATA ##########################################
NOAA = xr.open_dataset(NOAA_path)
ERA5 = xr.open_dataset(ERA5_path)
CONTROL = xr.open_dataset(CONTROL_path)
EXPERIMENT = xr.open_dataset(EXPERIMENT_path)

# Rename to get time lat lon
ERA5 = ERA5.rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'msl': 'mslp'})
EXPERIMENT = EXPERIMENT.rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'})
CONTROL = CONTROL.rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'})

# Defining the time according to my reference data:
time = NOAA.time.sel(time=slice(initial_day,final_day))
NOAA_hourly = NOAA.sel(time=time)
MSLP = NOAA_hourly.mslp
lat = NOAA_hourly.lat
lon = NOAA_hourly.lon

# Model data:
if different_day == 'ON':
    time_new = NOAA.time.sel(time=slice(new_day,final_day))
    EXPERIMENT_hourly = EXPERIMENT.sel(time=time_new,lat=slice(latS,latN),lon=slice(lonW,lonE))

    lat_EXPERIMENT = EXPERIMENT_hourly.lat
    lon_EXPERIMENT = EXPERIMENT_hourly.lon
    MSLP_EXPERIMENT = EXPERIMENT_hourly.mslp/100

else:
    EXPERIMENT_hourly = EXPERIMENT.sel(time=time,lat=slice(latS,latN),lon=slice(lonW,lonE))

    lat_EXPERIMENT = EXPERIMENT_hourly.lat
    lon_EXPERIMENT = EXPERIMENT_hourly.lon
    MSLP_EXPERIMENT = EXPERIMENT_hourly.mslp/100

CONTROL_hourly = CONTROL.sel(time=time,lat=slice(latS,latN),lon=slice(lonW,lonE))
lat_CONTROL = CONTROL_hourly.lat
lon_CONTROL = CONTROL_hourly.lon
MSLP_CONTROL = CONTROL_hourly.mslp/100

# # PROCESSING ERA5 DATA:

if convertion_to_180 != 'ON':
    ERA5_hourly = ERA5.sel(time=time, method='nearest')
    ERA5_hourly = ERA5_hourly.sel(lat=slice(latN,latS),lon=slice(lonW,lonE))
    ERA5_hourly = ERA5_hourly.transpose('time', 'lat', 'lon')
    lat_ERA5 = ERA5_hourly.lat[::-1]
    lon_ERA5 = ERA5_hourly.lon
    MSLP_ERA5 = ERA5_hourly.mslp.sel(lat=lat_ERA5) / 100    # to hPa

elif convertion_to_180 == 'ON':
    ERA5_hourly = ERA5.sel(time=time, method='nearest')
    ERA5_hourly = ERA5_hourly.assign_coords(lon=((ERA5.lon + 180) % 360) - 180).sortby('lon')
    ERA5_hourly = ERA5_hourly.sel(lat=slice(latN,latS),lon=slice(lonW,lonE))
    lat_ERA5 = ERA5_hourly.lat[::-1]
    lon_ERA5 = ERA5_hourly.lon
    MSLP_ERA5 = ERA5_hourly.mslp.sel(lat=lat_ERA5) / 100    # to hPa


# One could add more type of data following this structure
datasets = [
    (MSLP, lat, lon, 'o', 'NOAA', 'green'),
    (MSLP_ERA5, lat_ERA5, lon_ERA5, 's', 'ERA5', 'blue'),
    (MSLP_EXPERIMENT,  lat_EXPERIMENT, lon_EXPERIMENT, '^', label_experiment, experiment_color),
    (MSLP_CONTROL, lat_CONTROL, lon_CONTROL, '*', label_control, control_color)
]

#################################### PLOT ##########################################

plt.figure(figsize=(10,8))
proj = ccrs.Mercator()
ax = plt.axes(projection=proj)

dlat, dlon = 2.8, 2.8   # PAY ATTENTION HERE

ax.add_feature(cfeature.LAND,  facecolor='lightgray')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)
ax.add_feature(cfeature.STATES.with_scale('50m'), edgecolor='black', linewidth=0.5)

#lonW, lonE, latS, latN = -106, -70, 13, 37

ax.set_extent([-100, -70, 13, 37], crs=ccrs.PlateCarree()) # One could change this to get the study-area lat/lon region

gl = ax.gridlines(
    crs=ccrs.PlateCarree(), draw_labels=True,
    linewidth=1, color='gray', alpha=0.5, linestyle='--'
)

## Just to get the NOAA lat lon

lat_points_NOAA, lon_points_NOAA = [], []

for t in range(0, len(time), 1): 

    lon_array_sel = datasets[0][2].isel(time=t)
    lat_array_sel = datasets[0][1].isel(time=t)
    
    lon_points_NOAA.append(lon_array_sel.values)
    lat_points_NOAA.append(lat_array_sel.values)


for dataset_MSLP, lat_array, lon_array, marker, label, color in datasets:
    
    lat_points, lon_points, MSLP_values = [], [], []

    for t in range(0, len(time), 1): 

        MSLP_t = dataset_MSLP.isel(time=t)

        if label == 'NOAA':
            lon_array_sel = lon_array.isel(time=t)
            lat_array_sel = lat_array.isel(time=t)
            
            lon_points.append(lon_array_sel.values)
            lat_points.append(lat_array_sel.values)

        else:
            # lat_t, lon_t = np.meshgrid(lat_array, lon_array, indexing='ij')
            
            # Define a região delimitada pelo quadrado
            upper_lat, lower_lat = lat_points_NOAA[t] + dlat, lat_points_NOAA[t] - dlat
            left_lon, right_lon = lon_points_NOAA[t] - dlon, lon_points_NOAA[t] + dlon

            # Seleciona os valores de lat,lon,MSLP dentro da região delimitada

            lat_sliced = lat_array.sel(lat=slice(lower_lat,upper_lat))
            lon_sliced = lon_array.sel(lon=slice(left_lon, right_lon))
            MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(lower_lat, upper_lat))
            
            lat_t, lon_t = np.meshgrid(lat_sliced, lon_sliced, indexing='ij')
            # Verifica se há pontos válidos na região delimitada
            if MSLP_sliced.size > 0 and not np.isnan(MSLP_sliced).all():
                # Encontra o índice do valor mínimo dentro da região delimitada
                min_index = np.nanargmin(MSLP_sliced.values)  # Ignora NaN
                min_value = MSLP_sliced.values.ravel()[min_index]  # Valor mínimo

                # Converte o índice 1D para índices 2D (lat, lon)
                lat_index, lon_index = np.unravel_index(min_index, MSLP_sliced.values.shape)

                # Obtém as coordenadas (lat, lon) correspondentes ao valor mínimo
                lat_sel = lat_t[lat_index, lon_index]
                lon_sel = lon_t[lat_index, lon_index]

                # Adiciona os valores às listas
                MSLP_values.append(min_value)
                lat_points.append(lat_sel)
                lon_points.append(lon_sel)
            else:
                # Se não houver pontos válidos, pula para o próximo timestep
                print(f"No valid points found for {label} at timestep {t}. Skipping...")
                continue  # Pula para o próximo timestep
    
    lat_points = np.array(lat_points)
    lon_points = np.array(lon_points)
    MSLP_values = np.array(MSLP_values)

    ax.plot(
        lon_points, lat_points,
        color=color, linestyle='-', marker=marker, linewidth=1.5, label=label,
        transform=ccrs.PlateCarree()
    )

    for i in range(0, len(lat_points), 1):
        time_label = str(time[i].values)[:13] if len(time) > i else "N/A"  

        if lat_points[i] <= 35 and label == "NOAA" and lat_points[i] >= 8.5:
            ax.text(
                lon_points[i], lat_points[i],
                f"T:{time_label}", fontweight='bold',
                color=color, fontsize=8, transform=ccrs.PlateCarree()
            )

ax.legend(loc='upper right', fontsize=10)
ax.set_adjustable('box')
ax.set_aspect('auto')

ax.set_title(graph_title, fontsize=12)
plt.tight_layout()
plt.savefig(where_save + saving_name, dpi=300, bbox_inches='tight')

