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

from namelist_for_helene import *

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
# Guardar trilha do NOAA
lat_points_NOAA, lon_points_NOAA, mslp_points_NOAA = [], [], []
for t in range(0, len(time), 1):
    lon_array_sel = lon.isel(time=t)
    lat_array_sel = lat.isel(time=t)
    lon_points_NOAA.append(lon_array_sel.values)
    lat_points_NOAA.append(lat_array_sel.values)
    mslp_points_NOAA.append(MSLP.isel(time=t).values)

print(lat_points_NOAA)

datasets = [] # criado para fazer um loop depois nas trajetorias

datasets.append({
    'label': 'NOAA',
    'prec_acc': None,  # Não tem precipitação
    'lat': lat,
    'lon': lon,
    'mslp_trail_lat': lat_points_NOAA,
    'mslp_trail_lon': lon_points_NOAA,
    'color': 'darkgreen',
    'marker': 'o'
})

# ========== OUTROS DATASETS ==========
for label, color, input_file_data in data_information:
    print('oi')
    print(f'Processing {label} data ...')
    
    if label == 'ERA5':
        # abrindo dados do ERA5
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

    # Encontrar trilha do ciclone para esse dataset
    lat_points, lon_points, mslp_points = [], [], []

    dlat, dlon = 2.0, 2.0
    
    for t in range(len(time)):
        MSLP_t = MSLP_data.isel(time=t)
        # Região de busca
        upper_lat, lower_lat = lat_points_NOAA[t] + dlat, lat_points_NOAA[t] - dlat
        left_lon, right_lon = lon_points_NOAA[t] - dlon, lon_points_NOAA[t] + dlon
        
        # Seleciona região
        lon_sliced = lon_data.sel(lon=slice(left_lon, right_lon))
        if label == 'ERA5':
            lat_sliced = lat_data.sel(lat=slice(lower_lat,upper_lat))
            MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(lower_lat,upper_lat))
            print(MSLP_sliced)

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
            mslp_points.append(MSLP_sliced.values.ravel()[min_index])
    
    datasets.append({
        'label': label,
        'prec_acc': prec_acc,
        'lat': lat_data,
        'lon': lon_data,
        'mslp_trail_lat': lat_points,
        'mslp_trail_lon': lon_points,
        'color': color,
        'marker': '^'
    })

# ========== PLOT 1 =================================================================== #
# Plot all tracks (datasets + NOAA) without precipitation

plt.figure(figsize=(9, 7))
proj = ccrs.Mercator()
ax = plt.axes(projection=proj)
# lonW, lonE, latS, latN = -92, -69, 17, 49
ax.set_extent([-91, -70, 17, 40], crs=ccrs.PlateCarree())
# ax.set_yticks(np.arange(latS , latN, 3), crs=ccrs.PlateCarree())

# Add map features
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.STATES.with_scale('50m'), edgecolor='black', linewidth=0.5)
gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
gl.top_labels = False
gl.right_labels = False

# Plot all tracks except NOAA
for d in datasets:
    if d['label'] == 'NOAA':
        continue
    ax.plot(
        d['mslp_trail_lon'], d['mslp_trail_lat'],
        color=d['color'], marker=d['marker'], label=d['label'],
        transform=ccrs.PlateCarree()
    )
# Plot NOAA track
ax.plot(
    lon_points_NOAA, lat_points_NOAA,
    color='darkgreen', marker='o', label='NOAA',
    transform=ccrs.PlateCarree()
)

plt.legend()
# plt.title("Tracks of all datasets + NOAA")
plt.savefig("/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/accumulated/helene_results/Helene_Tracks_FINAL.png", dpi=300, bbox_inches='tight', pad_inches=0)
plt.close()
exit()

# =============================== PLOT 2 =================================================

# # Define experiment groups (update labels as needed)
# groups = {
#     "Parameterization Effects": ['NOAA', 'CP-ON', 'CP-OFF', 'CPSS-ON', 'ERA5'],
#     "Lifetime Effects": ['NOAA', 'CP-ON', 'CP-1H', 'CP-3H', 'CP-6H'],
#     "Mass-Flux Height Effects": ['NOAA', 'CP-ON', 'CP-D025', 'CP-D050'],
#     "Resolution Effects": ['NOAA', 'CP-ON', 'CP-15km', 'CP-60km'],
#     "Initial Condition Effects": ['NOAA', 'CP-ON', 'CP-GFS', 'CPSS-02', 'CP-29', 'CP-01', 'CP-02T12'],
#     "Best Configuration": ['NOAA', 'CP-ON', 'CP-1HD050', 'CP-1HD05015km']
# }

# # Loop through each group and create a plot with the datasets in the group + NOAA track
# for group_name, exp_list in groups.items():
    
#     plt.figure(figsize=(10,8))
#     proj = ccrs.Mercator()
#     ax = plt.axes(projection=proj)
#     ax.set_extent([-100, -70, 13, 37], crs=ccrs.PlateCarree())

#     # Add map features
#     ax.add_feature(cfeature.LAND, facecolor='lightgray')
#     ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
#     ax.add_feature(cfeature.COASTLINE)
#     ax.add_feature(cfeature.BORDERS, linestyle=':')
#     ax.add_feature(cfeature.STATES.with_scale('50m'), edgecolor='black', linewidth=0.5)
#     gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
#     gl.top_labels = False
#     gl.right_labels = False

#     # Criar um conjunto para armazenar rótulos da legenda e evitar duplicação
#     legend_labels = set()

#     # Plot datasets que estão no grupo
#     for d in datasets:
#         if d['label'] in exp_list:
#             ax.plot(
#                 d['mslp_trail_lon'], d['mslp_trail_lat'],
#                 color=d['color'], marker=d['marker'],
#                 label=d['label'] if d['label'] not in legend_labels else "_nolegend_",  # Evita duplicação
#                 transform=ccrs.PlateCarree()
#             )
#             legend_labels.add(d['label'])  # Adiciona o rótulo ao conjunto

#     # Plot NOAA track apenas uma vez
#     if "NOAA" in exp_list and "NOAA" not in legend_labels:
#         ax.plot(
#             lon_points_NOAA, lat_points_NOAA,
#             color='darkgreen', marker='o', label='NOAA',
#             transform=ccrs.PlateCarree()
#         )
#         legend_labels.add("NOAA")

#     plt.legend()
#     plt.title(f"Tracks: {group_name}")
#     plt.savefig('/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/accumulated/Grups_pathing_updated/'+f"{group_name.replace(' ', '_')}_tracks.png", dpi=300, bbox_inches='tight', pad_inches=0)
#     plt.close()

# # ========================================================================================= #

# # ========== PLOT 3 ======================================================================= #

# # For each dataset, plot the dataset track + NOAA track (without precipitation)

# for dataset in datasets:
#     label = dataset['label']
#     lat_data = dataset['lat']
#     lon_data = dataset['lon']
#     prec_acc = dataset['prec_acc']

#     # Skip NOAA dataset here
#     if dataset['label'] == 'NOAA':
#         continue

#     plt.figure(figsize=(12, 10))
#     proj = ccrs.Mercator()
#     ax = plt.axes(projection=proj)
#     ax.set_extent([-100, -70, 13, 37], crs=ccrs.PlateCarree())

#     # Add map features
#     ax.add_feature(cfeature.LAND, facecolor='lightgray')
#     ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
#     ax.add_feature(cfeature.COASTLINE)
#     ax.add_feature(cfeature.BORDERS, linestyle=':')
#     ax.add_feature(cfeature.STATES.with_scale('50m'), edgecolor='black', linewidth=0.5)
#     gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
#     gl.top_labels = False
#     gl.right_labels = False

#     # Plot precipitation (if available)
#     if prec_acc is not None:
#         levels = np.arange(0, 50, 5)
#         cmap = plt.cm.Blues
#         prec_plot = ax.contourf(
#             lon_data, lat_data, prec_acc,
#             levels=levels, cmap=cmap, extend='both',
#             transform=ccrs.PlateCarree()
#         )
#         cbar = plt.colorbar(prec_plot, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
#         cbar.set_label("Accumulated Precipitation (mm/day)")

#     # Plot current dataset track
#     ax.plot(
#         dataset['mslp_trail_lon'], dataset['mslp_trail_lat'],
#         color=dataset['color'], marker=dataset['marker'], label=label,
#         transform=ccrs.PlateCarree()
#     )

#     # Plot NOAA track
#     ax.plot(
#         lon_points_NOAA, lat_points_NOAA,
#         color='darkgreen', marker='o', label='NOAA',
#         transform=ccrs.PlateCarree()
#     )

#     plt.legend()
#     plt.title(f"Track of {label} + NOAA")
#     plt.savefig(f"{label}_track_NOAA.png", dpi=300, bbox_inches='tight', pad_inches=0)
#     plt.close()

# # # ========== PLOTAGEM TODOS==========

# for dataset in datasets:
#     label = dataset['label']
#     prec_acc = dataset['prec_acc']
#     lat_data = dataset['lat']
#     lon_data = dataset['lon']

#     plt.figure(figsize=(12, 10))
#     proj = ccrs.Mercator()
#     ax = plt.axes(projection=proj)
#     ax.set_extent([-100, -70, 13, 37], crs=ccrs.PlateCarree())

#     # Features
#     ax.add_feature(cfeature.LAND, facecolor='lightgray')
#     ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
#     ax.add_feature(cfeature.COASTLINE)
#     ax.add_feature(cfeature.BORDERS, linestyle=':')
#     ax.add_feature(cfeature.STATES.with_scale('50m'), edgecolor='black', linewidth=0.5)
#     gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
#     gl.top_labels = False
#     gl.right_labels = False

#     # Plot PRECIP (só se tiver)
#     if prec_acc is not None:
#         levels = np.arange(0, 50, 5)
#         cmap = plt.cm.Blues
#         prec_plot = ax.contourf(
#             lon_data, lat_data, prec_acc,
#             levels=levels, cmap=cmap, extend='both',
#             transform=ccrs.PlateCarree()
#         )
#         cbar = plt.colorbar(prec_plot, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
#         cbar.set_label('Acumulado de Precipitação (mm/day)')

#     # Plot TRILHAS de TODOS os datasets
#     for d in datasets:
#         ax.plot(
#             d['mslp_trail_lon'], d['mslp_trail_lat'],
#             color=d['color'], marker=d['marker'], label=d['label'],
#             transform=ccrs.PlateCarree()
#         )

#     plt.legend()
#     plt.title(f"Precipitação acumulada e trilhas - {label}")
#     plt.savefig(f"/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/accumulated/Grups_pathing_updated/com_chuva/{label}_precip_trilhas.png")
#     plt.close()
