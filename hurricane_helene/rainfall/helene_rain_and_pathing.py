import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as mcolors
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib

from shapely.geometry import Point


matplotlib.use("Agg")

from namelist_for_helene_pathing import *

'''
Este codigo serve para plotar o caminho registrado pelo algoritmo
de localizaçao da pressao central juntamente com o acumulado de chuva do dia
'''

# Separacao dos dados de referencia, nesse caso os dados da NOAA
NOAA = xr.open_dataset(NOAA_path)
time = NOAA.time.sel(time=slice(initial_day,final_day))
NOAA_hourly = NOAA.sel(time=time)
MSLP = NOAA_hourly.mslp
lat = NOAA_hourly.lat
lon = NOAA_hourly.lon

## Just to get the NOAA lat lon
lat_points_NOAA, lon_points_NOAA = [], []
for t in range(0, len(time), 1): 

    lon_array_sel = lon.isel(time=t)
    lat_array_sel = lat.isel(time=t)
    
    lon_points_NOAA.append(lon_array_sel.values)
    lat_points_NOAA.append(lat_array_sel.values)

datasets = [] # criado para fazer um loop depois nas trajetorias

datasets.append((MSLP, lat, lon, 'NOAA', 'black'))

# for label, color, input_file_data in data_information:

#     print(f'Processing {label} data ...')
    
#     if label == 'ERA5':
#         # abrindo dados do ERA5
#         dataset_prec = xr.open_dataset(input_file_data).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon'})
#         dataset_dry = xr.open_dataset('/mnt/beegfs/bianca.fusinato/monan/comparison/helene/era5/x1.655362.era5_helene_dry_native.nc').rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'msl': 'mslp'})

#         dataset_prec = (dataset_prec.assign_coords(lon=((dataset_prec.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')
#         dataset_dry = (dataset_dry.assign_coords(lon=((dataset_dry.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')

#         lat_data = dataset_prec.lat.sel(lat=slice(latS,latN))
#         lon_data = dataset_prec.lon.sel(lon=slice(lonW, lonE))

#         slice_prec = dataset_prec.tp.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)) * 1000 * 24
#         prec_acc = slice_prec.sum(dim='time') / num_days

#         MSLP_data = dataset_dry.mslp.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)) / 100  # to hPa

#     else:
#         model_data = (xr.open_dataset(input_file_data).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'})).sel(time=time, lat=slice(latS, latN), lon=slice(lonW, lonE))

#         lat_data = model_data.lat
#         lon_data = model_data.lon
#         prec_acc = (model_data.rainc.sel(time=final_day) + model_data.rainnc.sel(time=final_day)) / num_days
#         MSLP_data = model_data.mslp / 100

#     datasets.append((MSLP_data, lat_data, lon_data, label, color))
#     # --------------------- PLOTAGEM ------------------------
#     plt.figure(figsize=(12, 10))
#     proj = ccrs.Mercator()
#     ax = plt.axes(projection=proj)

#     ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree())

#     # Mapa features
#     ax.add_feature(cfeature.LAND, facecolor='lightgray')
#     ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
#     ax.add_feature(cfeature.COASTLINE)
#     ax.add_feature(cfeature.BORDERS, linestyle=':')
#     ax.add_feature(cfeature.STATES.with_scale('50m'), edgecolor='black', linewidth=0.5)

#     # Gridlines
#     gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
#     gl.top_labels = False
#     gl.right_labels = False
#     gl.xlabel_style = {'size': 10}
#     gl.ylabel_style = {'size': 10}

#     # --------------------- PRECIP PLOT ------------------------
#     levels = np.arange(0, 50, 5)
#     cmap = plt.cm.Blues

#     prec_plot = ax.contourf(
#         lon_data, lat_data, prec_acc,
#         levels=levels, cmap=cmap, extend='both',
#         transform=ccrs.PlateCarree()
#     )

#     cbar = plt.colorbar(prec_plot, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
#     cbar.set_label('Acumulado de Precipitação (mm/day)')

# dlat, dlon = 10, 10

# # Criar um dicionário para armazenar DataFrames para cada dataset
# dataframes = {}

# for dataset_MSLP, lat_array, lon_array, marker, label, color in datasets:

#     lat_points, lon_points, mslp_points, time_steps = [], [], [], []

#     for t in range(len(time)):
#         MSLP_t = dataset_MSLP.isel(time=t)

#         if label == 'NOAA':
#             lon_array_sel = lon_array.isel(time=t)
#             lat_array_sel = lat_array.isel(time=t)
            
#             lon_points.append(lon_array_sel.values)
#             lat_points.append(lat_array_sel.values)

#             mslp_points.append(MSLP_t.values)
#             time_steps.append(t)

#         else:
#             # Região para busca do mínimo (baseado no NOAA)
#             upper_lat, lower_lat = lat_points_NOAA[t] + dlat, lat_points_NOAA[t] - dlat
#             left_lon, right_lon = lon_points_NOAA[t] - dlon, lon_points_NOAA[t] + dlon

           
#             lon_sliced = lon_array.sel(lon=slice(left_lon, right_lon))
#             if label == 'ERA5':
#                 lat_sliced = lat_array.sel(lat=slice(upper_lat, lower_lat))
#                 MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(upper_lat,lower_lat))
#             else:
#                 lat_sliced = lat_array.sel(lat=slice(lower_lat,upper_lat))
#                 MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(lower_lat,upper_lat))


#             lat_t, lon_t = np.meshgrid(lat_sliced, lon_sliced, indexing='ij')
            
#             # Verifica se há pontos válidos na região delimitada
#             if MSLP_sliced.size > 0 and not np.isnan(MSLP_sliced).all():
#                 # Encontra o índice do valor mínimo dentro da região delimitada
#                 min_index = np.nanargmin(MSLP_sliced.values)  # Ignora NaN
#                 min_value = MSLP_sliced.values.ravel()[min_index]  # Valor mínimo

#                 # Converte o índice 1D para índices 2D (lat, lon)
#                 lat_index, lon_index = np.unravel_index(min_index, MSLP_sliced.values.shape)

#                 # Obtém as coordenadas (lat, lon) correspondentes ao valor mínimo
#                 lat_sel = lat_t[lat_index, lon_index]
#                 lon_sel = lon_t[lat_index, lon_index]

#                 # Adiciona os valores às listas
#                 mslp_points.append(min_value)
#                 lat_points.append(lat_sel)
#                 lon_points.append(lon_sel)
#                 time_steps.append(t)
#             else:
#                 # Se não houver pontos válidos, pula para o próximo timestep
#                 print(f"No valid points found for {label} at timestep {t}. Skipping...")
#                 continue  # Pula para o próximo timestep
            

#     # Plotar caminho
#     ax.plot(
#         lon_points, lat_points, color=color, linestyle='-',
#         marker=marker, linewidth=1.5, label=label,
#         transform=ccrs.PlateCarree()
#     )

# =============================== ESTOU TESTANDO ISSO: =========================================== #

# Separacao dos dados que irei plotar:

for label, color, input_file_data in data_information:
    
    if label == 'ERA5':

        dataset_prec = xr.open_dataset(input_file_data).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon'})
        dataset_dry = xr.open_dataset('/mnt/beegfs/bianca.fusinato/monan/comparison/helene/era5/x1.655362.era5_helene_dry_native.nc').rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'msl': 'mslp'})

        dataset_prec = (dataset_prec.assign_coords(lon=((dataset_prec.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')
        dataset_dry = (dataset_dry.assign_coords(lon=((dataset_dry.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')

        lat_data = dataset_prec.lat.sel(lat=slice(latS,latN))
        lon_data = dataset_prec.lon.sel(lon=slice(lonW, lonE))

        slice_prec = dataset_prec.tp.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)) * 1000 * 24
        prec_acc = slice_prec.sum(dim='time') / num_days

        MSLP_data = dataset_dry.mslp.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)) / 100  # to hPa

    else:    
        model_data = (xr.open_dataset(input_file_data).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'})).sel(time=time, lat=slice(latS, latN), lon=slice(lonW, lonE))

        lat_data = model_data.lat
        lon_data = model_data.lon
        prec_acc = (model_data.rainc.sel(time=final_day) + model_data.rainnc.sel(time=final_day)) / num_days
        MSLP_data = model_data.mslp / 100

    datasets.append((MSLP_data, lat_data, lon_data, label, color))

    # --------------------- PLOTAGEM ------------------------

    plt.figure(figsize=(12, 10))
    proj = ccrs.Mercator()
    ax = plt.axes(projection=proj)

    ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree())

    # Features do mapa
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.STATES.with_scale('50m'), edgecolor='black', linewidth=0.5)

    # Gridlines
    gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 10}
    gl.ylabel_style = {'size': 10}

    # --------------------- PLOT PRECIPITAÇÃO ------------------------
    # Escolher níveis e cores
    levels = np.arange(0, 50, 5)  # Ajuste conforme necessário
    cmap = plt.cm.Blues

    prec_plot = ax.contourf(
        lon_data, lat_data, prec_acc,
        levels=levels, cmap=cmap, extend='both',
        transform=ccrs.PlateCarree()
    )

    cbar = plt.colorbar(prec_plot, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar.set_label('Acumulado de Precipitação (mm/day)')

# --------------------- PLOT CAMINHOS PRESSÃO ------------------------

datasets = [
    (MSLP, lat, lon, 'o', 'NOAA', 'green'),
    (MSLP_data, lat_data, lon_data, 's', label, 'black'),
]

dlat, dlon = 10, 10

# Criar um dicionário para armazenar DataFrames para cada dataset
dataframes = {}

for dataset_MSLP, lat_array, lon_array, marker, label, color in datasets:

    lat_points, lon_points, mslp_points, time_steps = [], [], [], []

    for t in range(len(time)):
        MSLP_t = dataset_MSLP.isel(time=t)

        if label == 'NOAA':
            lon_array_sel = lon_array.isel(time=t)
            lat_array_sel = lat_array.isel(time=t)
            
            lon_points.append(lon_array_sel.values)
            lat_points.append(lat_array_sel.values)

            mslp_points.append(MSLP_t.values)
            time_steps.append(t)

        else:
            # Região para busca do mínimo (baseado no NOAA)
            upper_lat, lower_lat = lat_points_NOAA[t] + dlat, lat_points_NOAA[t] - dlat
            left_lon, right_lon = lon_points_NOAA[t] - dlon, lon_points_NOAA[t] + dlon

           
            lon_sliced = lon_array.sel(lon=slice(left_lon, right_lon))
            if label == 'ERA5':
                lat_sliced = lat_array.sel(lat=slice(upper_lat, lower_lat))
                MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(upper_lat,lower_lat))
            else:
                lat_sliced = lat_array.sel(lat=slice(lower_lat,upper_lat))
                MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(lower_lat,upper_lat))


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
                mslp_points.append(min_value)
                lat_points.append(lat_sel)
                lon_points.append(lon_sel)
                time_steps.append(t)
            else:
                # Se não houver pontos válidos, pula para o próximo timestep
                print(f"No valid points found for {label} at timestep {t}. Skipping...")
                continue  # Pula para o próximo timestep
            

    # Plotar caminho
    ax.plot(
        lon_points, lat_points, color=color, linestyle='-',
        marker=marker, linewidth=1.5, label=label,
        transform=ccrs.PlateCarree()
    )
    # print(len(time_steps))
    # print(len(mslp_points))
    # print(len(lat_points))
    # print(len(lon_points))
    # Criar DataFrame
    df = pd.DataFrame({
        'time step': time_steps,
        'mslp': mslp_points,
        'lat': lat_points,
        'lon': lon_points
    })

    dataframes[label] = df

# --------------------- FINAL ------------------------

plt.legend(loc='lower left')
plt.title(f'Caminho do mínimo de pressão e acumulado de chuva ({initial_day} a {final_day})')
plt.savefig(f'/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/accumulated/helene_rain_and_pathing/track_and_precip_{label}.png', dpi=300, bbox_inches='tight')
plt.close()

print("Plot salvo com sucesso!")

# # --------------------- SALVAR EXCEL ------------------------

# excel_name = f'track_data_{label_data}.xlsx'
# with pd.ExcelWriter(excel_name) as writer:
#     for label, df in dataframes.items():
#         df.to_excel(writer, sheet_name=label, index=False)

# print(f"Tabela salva com sucesso em {excel_name}!")

# # --------------------- PLOTAGEM ------------------------

# plt.figure(figsize=(12, 10))
# proj = ccrs.Mercator()
# ax = plt.axes(projection=proj)

# ax.set_extent([-100, -70, 13, 37], crs=ccrs.PlateCarree())

# # Features do mapa
# ax.add_feature(cfeature.LAND, facecolor='lightgray')
# ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
# ax.add_feature(cfeature.COASTLINE)
# ax.add_feature(cfeature.BORDERS, linestyle=':')
# # ax.add_feature(cfeature.LAKES, alpha=0.5)
# # ax.add_feature(cfeature.RIVERS)
# ax.add_feature(cfeature.STATES.with_scale('50m'), edgecolor='black', linewidth=0.5)

# # Gridlines
# gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
# gl.top_labels = False
# gl.right_labels = False
# gl.xlabel_style = {'size': 10}
# gl.ylabel_style = {'size': 10}

# # --------------------- PLOT PRECIPITAÇÃO ------------------------
# # Escolher níveis e cores
# levels = np.arange(0, 50, 5)  # Ajuste conforme necessário
# cmap = plt.cm.Blues

# prec_plot = ax.contourf(
#     lon_ERA5, lat_ERA5, prec_acc,
#     levels=levels, cmap=cmap, extend='both',
#     transform=ccrs.PlateCarree()
# )

# cbar = plt.colorbar(prec_plot, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
# cbar.set_label('Acumulado de Precipitação (mm/day)')

# # --------------------- PLOT CAMINHOS PRESSÃO ------------------------
# datasets = [
#     (MSLP, lat, lon, 'o', 'NOAA', 'green'),
#     (MSLP_ERA5, lat_ERA5, lon_ERA5, 's', 'ERA5', 'black'),
# ]

# dlat, dlon = 2.8, 2.8

# for dataset_MSLP, lat_array, lon_array, marker, label, color in datasets:

#     lat_points, lon_points = [], []

#     for t in range(len(time)):
#         MSLP_t = dataset_MSLP.isel(time=t)

#         if label == 'ERA5':
#             # Região para busca do mínimo
#             upper_lat, lower_lat = lat_points_NOAA[t] + dlat, lat_points_NOAA[t] - dlat
#             left_lon, right_lon = lon_points_NOAA[t] - dlon, lon_points_NOAA[t] + dlon

#             lat_sliced = lat_array.sel(lat=slice(upper_lat, lower_lat))
#             lon_sliced = lon_array.sel(lon=slice(left_lon, right_lon))
#             MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(upper_lat,lower_lat))

#             if MSLP_sliced.size > 0 and not np.isnan(MSLP_sliced).all():
#                 min_index = np.nanargmin(MSLP_sliced.values)
#                 lat_idx, lon_idx = np.unravel_index(min_index, MSLP_sliced.shape)

#                 lat_sel = lat_sliced.values[lat_idx]
#                 lon_sel = lon_sliced.values[lon_idx]

#                 lat_points.append(lat_sel)
#                 lon_points.append(lon_sel)
#             else:
#                 continue

#     # Plotar caminho
#     ax.plot(
#         lon_points, lat_points, color=color, linestyle='-',
#         marker=marker, linewidth=1.5, label=label,
#         transform=ccrs.PlateCarree()
#     )

# # --------------------- FINAL ------------------------

# plt.legend(loc='lower left')
# plt.title(f'Caminho do mínimo de pressão e acumulado de chuva ({initial_day} a {final_day})')
# plt.savefig(f'track_and_precip_{label_data}.png', dpi=300, bbox_inches='tight')
# plt.close()

# print("Plot salvo com sucesso!")

