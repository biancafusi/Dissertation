import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy as np
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import xarray as xr

# Set the lat/lon box:
lonW = -106
lonE = -50
latS = 9
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

boxes = [
    {'lonW': -99, 'lonE': -94, 'latS': 27, 'latN': 30, 'label': 'F'},
    {'lonW': -86, 'lonE': -90, 'latS': 17, 'latN': 23, 'label': 'E'},
    {'lonW': -70, 'lonE': -62, 'latS': 10, 'latN': 20, 'label': 'D'}
]

for box in boxes:
    
    lonW,lonE,latS,latN = box['lonW'], box['lonE'], box['latS'], box['latN']
    width = lonE-lonW
    height = latN-latS

    rect = patches.Rectangle(
        (lonW, latS),
        width,
        height,
        linewidth = 1.5,
        facecolor='none',
        edgecolor = 'white',
        linestyle = '--',
        transform=ccrs.PlateCarree()
    )
    ax.add_patch(rect)

    ax.text(
        lonW + width / 2,
        latN+ 0.5,
        box['label'],
        color = 'white',
        fontweight = 'bold',
        ha = 'center', va='center',
        transform=ccrs.PlateCarree()
    )
# # Adiciona legendas
# ax.legend(loc="upper right", fontsize=9, title="Location")
# Add the trajectory
NOAA_path = '/home/bianca/Documentos/masters/data/beryl.nc'
NOAA = xr.open_dataset(NOAA_path)

initial_time = '2024-07-01'
final_time = '2024-07-11'

time = NOAA.time.sel(time=slice(initial_time,final_time))
NOAA_hourly = NOAA.sel(time=time)
MSLP = NOAA_hourly.mslp
lat = NOAA_hourly.lat
lon = NOAA_hourly.lon
vmax = NOAA_hourly.vmax * 1.852  # Convertendo para km/h

lat_points, lon_points = [], []
for t in range(0, len(time), 1): 

    lon_array_sel = lon.isel(time=t)
    lat_array_sel = lat.isel(time=t)
    
    lon_points.append(lon_array_sel.values)
    lat_points.append(lat_array_sel.values)

lat_points = np.array(lat_points)
lon_points = np.array(lon_points)

# Plot the trajectory
ax.plot(
    lon_points, lat_points,
    color='black',  # Cor da linha
    linestyle='-',  # Estilo da linha
    marker='o',     # Formato do marcador
    markerfacecolor='gray',  # Cor do marcador
    markeredgecolor='gray',  # Cor da borda do marcador
    markersize=6,   # Tamanho do marcador
    linewidth=1.2,  # Espessura da linha
    transform=ccrs.PlateCarree(),
    label='Trajectory'  # Adiciona uma etiqueta para a trajetória
)

# Plot markers for categories 1 and 5
# Cria marcadores fictícios para a legenda
cat5_proxy = plt.Line2D([], [], color='purple', marker='o', linestyle='None', markersize=6, label='CAT5')
cat1_proxy = plt.Line2D([], [], color='yellow', marker='o', linestyle='None', markersize=6, label='CAT1')

# Adiciona os pontos reais no loop, sem etiquetas
# for t in range(0, len(time), 1):
#     vmax_value = vmax.isel(time=t).values
#     lon_point = lon.isel(time=t).values
#     lat_point = lat.isel(time=t).values

#     if vmax_value >= 252:  # Category 5
#         ax.plot(lon_point, lat_point, 'o', color='purple', markersize=6, transform=ccrs.PlateCarree())
#     elif 119 <= vmax_value <= 153:  # Category 1
#         ax.plot(lon_point, lat_point, 'o', color='yellow', markersize=6, transform=ccrs.PlateCarree())

for t in range(0, len(time), 1):
    vmax_value = vmax.isel(time=t).values
    lon_point = lon.isel(time=t).values
    lat_point = lat.isel(time=t).values
    time_label = str(time[t].values)[:13]  # Formata o tempo conforme desejado

    if vmax_value >= 252:  # Categoria 5
        ax.plot(lon_point, lat_point, 'o', color='purple', markersize=6, transform=ccrs.PlateCarree())
        ax.text(lon_point, lat_point, time_label, fontsize=8, color='purple',fontweight='bold', transform=ccrs.PlateCarree())

    elif 119 <= vmax_value <= 153:  # Categoria 1
        ax.plot(lon_point, lat_point, 'o', color='yellow', markersize=6, transform=ccrs.PlateCarree())
        ax.text(lon_point, lat_point, time_label, fontsize=8, color='yellow',fontweight='bold', transform=ccrs.PlateCarree())    
    

legend = ax.legend(
    handles=[cat5_proxy, cat1_proxy, ax.get_legend_handles_labels()[0][0]],  # Inclui os marcadores fictícios e a trajetória
    loc='upper right',  # Posiciona a legenda no canto superior direito
    fontsize=9,
    title="Hurricane Categories",
    title_fontsize=10,
    frameon=True,  # Habilita a moldura da legenda
    facecolor='white',  # Cor de fundo da legenda
    edgecolor='black',  # Cor da borda da legenda
    framealpha=0.7,  # Transparência do fundo (0 = transparente, 1 = opaco)
    handlelength=1,  # Define o comprimento do manipulador (linha/marcador)
    handletextpad=0.5  # Define o espaçamento entre o manipulador e o texto
)

# Adiciona a legenda ao mapa
ax.add_artist(legend)
# Títulos e rótulos
ax.set_title("Beryl Trajectory with the hurricane's wind categories", fontsize=16)

# Mostra o mapa
plt.savefig('map_with_cat_path.png', dpi=300, bbox_inches="tight")