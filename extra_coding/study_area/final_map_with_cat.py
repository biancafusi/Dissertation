import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy as np
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import xarray as xr
import pandas as pd

# Set the lat/lon box:
lonW = -92
lonE = -69
latS = 17
latN = 40

# # Coordinates for some locations
# locations = {
#     "Houston, Texas": (29.7604, -95.3698),
#     "Matagorda, Texas": (28.696944, -95.966667),
#     "Yucatán Peninsula": (20.5, -89.0),
#     "Grenada": (12.1165, -61.679),
#     "St. Vincent": (13.2528, -61.1971),
#     "Baton Rouge, Louisiana": (30.4515, -91.1871),
# }
# markers = {
#     "Houston, Texas": 'o',
#     "Matagorda, Texas": 'p',
#     "Yucatán Peninsula": 's',
#     "Grenada": '^',
#     "St. Vincent": 'D',
#     "Baton Rouge, Louisiana": '*',
# }

# Configuração do mapa
stamen_terrain = cimgt.GoogleTiles(style='satellite')
fig, ax = plt.subplots(
    figsize=(9, 7),
    subplot_kw={"projection": stamen_terrain.crs}
)

# Map lat/lon extension 
ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree())

# Add background image:
ax.add_image(stamen_terrain, 8)

# # Add the locations with a red marker
# for name, (lat, lon) in locations.items():
#     ax.plot(lon, lat, markers[name], color='red', markersize=4, transform=ccrs.PlateCarree(), label=name)

# axis labels
ax.set_yticks(np.arange(latS , latN, 5), crs=ccrs.PlateCarree())
ax.set_xticks(np.linspace(lonW,lonE,9,dtype=int), crs=ccrs.PlateCarree())
   
lon_formatter = LongitudeFormatter(number_format='.0f',  
                                   degree_symbol='',
                                   dateline_direction_label=True)

lat_formatter = LatitudeFormatter(number_format='.0f',
                                  degree_symbol='')

ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)


# Creation of the boxes

# boxes = [
#     {'lonW': -99, 'lonE': -94, 'latS': 27, 'latN': 30, 'label': 'F'},
#     {'lonW': -86, 'lonE': -90, 'latS': 17, 'latN': 23, 'label': 'E'},
#     {'lonW': -70, 'lonE': -62, 'latS': 10, 'latN': 20, 'label': 'D'}
# ]

# for box in boxes:
    
#     lonW,lonE,latS,latN = box['lonW'], box['lonE'], box['latS'], box['latN']
#     width = lonE-lonW
#     height = latN-latS

#     rect = patches.Rectangle(
#         (lonW, latS),
#         width,
#         height,
#         linewidth = 1.5,
#         facecolor='none',
#         edgecolor = 'white',
#         linestyle = '--',
#         transform=ccrs.PlateCarree()
#     )
#     ax.add_patch(rect)

#     ax.text(
#         lonW + width / 2,
#         latN+ 0.5,
#         box['label'],
#         color = 'white',
#         fontweight = 'bold',
#         ha = 'center', va='center',
#         transform=ccrs.PlateCarree()
#     )
# # Adiciona legendas
# ax.legend(loc="upper right", fontsize=9, title="Location")
# Add the trajectory
NOAA_path = '/home/bianca/Documentos/masters/data/Helene.nc'
NOAA = xr.open_dataset(NOAA_path)

initial_time = '2024-09-24'
final_time = '2024-09-28'

time = NOAA.time.sel(time=slice(initial_time,final_time))
NOAA_hourly = NOAA.sel(time=time)
MSLP = NOAA_hourly.mslp
lat = NOAA_hourly.lat
lon = NOAA_hourly.lon
vmax = NOAA_hourly.vmax * 1.852  # Convertendo para km/h

# Intervalo de tempo para o marcador 'o'
start_marker_time = pd.to_datetime('2024-09-24T00:00:00')
end_marker_time = pd.to_datetime('2024-09-28T00:00:00')

lat_points, lon_points = [], []

for t in range(len(time)):
    current_time = pd.to_datetime(str(time[t].values))

    lon_val = lon.isel(time=t).values
    lat_val = lat.isel(time=t).values

    # Armazena os pontos para possível uso adicional
    lon_points.append(lon_val)
    lat_points.append(lat_val)

    # Decide o marcador com base no intervalo de tempo
    if start_marker_time <= current_time <= end_marker_time:
        marker_style = 'o'
        marker_color = 'gray'
    else:
        marker_style = 'x'
        marker_color = 'red'

    ax.plot(
        lon_val, lat_val,
        color='black',
        marker=marker_style,
        markerfacecolor=marker_color if marker_style == 'o' else 'none',
        markeredgecolor=marker_color,
        markersize=6,
        linewidth=1.2,
        transform=ccrs.PlateCarree(),
    )
ax.set_yticks(np.arange(latS, latN + 1, 3), crs=ccrs.PlateCarree())

# Opcional: plotar a linha de trajetória contínua
ax.plot(
    lon_points, lat_points,
    color='black',
    linestyle='-',
    linewidth=1.2,
    transform=ccrs.PlateCarree(),
    label='Trajectory',
    zorder=1  # Desenha atrás dos marcadores
)

# Coordenadas de Perry, Florida
perry_lat = 30.1170
perry_lon = -83.5818

# Adiciona uma estrela vermelha em Perry, Florida
ax.plot(
    perry_lon, perry_lat,
    marker='*',
    color='red',
    markersize=10,
    transform=ccrs.PlateCarree(),
    label='Perry, Florida'
)

# Opcional: adicionar o nome no mapa
ax.text(
    perry_lon + 0.3, perry_lat + 0.3,
    "Perry, FL",
    color='white',
    fontsize=9,
    fontweight='bold',
    transform=ccrs.PlateCarree()
)
# Adiciona os pontos reais no loop, sem etiquetas
# for t in range(0, len(time), 1):
#     vmax_value = vmax.isel(time=t).values
#     lon_point = lon.isel(time=t).values
#     lat_point = lat.isel(time=t).values

#     if vmax_value >= 252:  # Category 5
#         ax.plot(lon_point, lat_point, 'o', color='purple', markersize=6, transform=ccrs.PlateCarree())
#     elif 119 <= vmax_value <= 153:  # Category 1
#         ax.plot(lon_point, lat_point, 'o', color='yellow', markersize=6, transform=ccrs.PlateCarree())

# Cria marcadores fictícios para a legenda
cat1_proxy = plt.Line2D([], [], color='yellow', marker='o', linestyle='None', markersize=6, label='CAT1')
cat2_proxy = plt.Line2D([], [], color='orange', marker='o', linestyle='None', markersize=6, label='CAT2')
cat3_proxy = plt.Line2D([], [], color='red', marker='o', linestyle='None', markersize=6, label='CAT3')
cat4_proxy = plt.Line2D([], [], color='pink', marker='o', linestyle='None', markersize=6, label='CAT4')
cat5_proxy = plt.Line2D([], [], color='purple', marker='o', linestyle='None', markersize=6, label='CAT5')

# Loop principal para plotar os pontos com base na categoria
for t in range(0, len(time), 1):
    vmax_value = vmax.isel(time=t).values
    lon_point = lon.isel(time=t).values
    lat_point = lat.isel(time=t).values
    time_label = pd.to_datetime(str(time[t].values)).strftime('%Y-%m-%d %H UTC')

    if vmax_value >= 252:  # Categoria 5
        ax.plot(lon_point, lat_point, 'o', color='purple', markersize=6, transform=ccrs.PlateCarree())
        ax.text(lon_point, lat_point, time_label, fontsize=8, color='purple', fontweight='bold', transform=ccrs.PlateCarree())

    elif 209 <= vmax_value <= 251:  # Categoria 4
        ax.plot(lon_point, lat_point, 'o', color='pink', markersize=6, transform=ccrs.PlateCarree())
        ax.text(lon_point, lat_point, time_label, fontsize=8, color='pink', fontweight='bold', transform=ccrs.PlateCarree())

    elif 178 <= vmax_value <= 208:  # Categoria 3
        ax.plot(lon_point, lat_point, 'o', color='red', markersize=6, transform=ccrs.PlateCarree())
        ax.text(lon_point, lat_point, time_label, fontsize=8, color='red', fontweight='bold', transform=ccrs.PlateCarree())

    elif 154 <= vmax_value <= 177:  # Categoria 2
        ax.plot(lon_point, lat_point, 'o', color='orange', markersize=6, transform=ccrs.PlateCarree())
        ax.text(lon_point, lat_point, time_label, fontsize=8, color='orange', fontweight='bold', transform=ccrs.PlateCarree())

    elif 119 <= vmax_value <= 153:  # Categoria 1
        ax.plot(lon_point, lat_point, 'o', color='yellow', markersize=6, transform=ccrs.PlateCarree())
        ax.text(lon_point, lat_point, time_label, fontsize=8, color='yellow', fontweight='bold', transform=ccrs.PlateCarree())


legend = ax.legend(
    handles=[
        cat1_proxy,
        cat2_proxy,
        cat3_proxy,
        cat4_proxy,
        ax.get_legend_handles_labels()[0][0]  # Inclui a trajetória real, se estiver plotada com label
    ],
    loc='upper right',
    fontsize=9,
    title="Hurricane Categories",
    title_fontsize=10,
    frameon=True,
    facecolor='white',
    edgecolor='black',
    framealpha=0.7,
    handlelength=1,
    handletextpad=0.5
)

# Adiciona a legenda ao mapa
ax.add_artist(legend)
# Títulos e rótulos
# ax.set_title("Beryl Trajectory with the hurricane's wind categories", fontsize=16)

# Mostra o mapa
plt.savefig('HELENE_map_with_cat_path.png', dpi=300, bbox_inches="tight")