import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy as np
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

lonW = -106
lonE = -50
latS = 5
latN = 41

# Coordenadas das localidades
locations = {
    "Houston, Texas": (29.7604, -95.3698),
    "Matagorda, Texas": (28.696944, -95.966667),
    "Yucatán Peninsula": (20.5, -89.0),
    "Grenada": (12.1165, -61.679),
    "St. Vincent": (13.2528, -61.1971),
    "Baton Rouge, Louisiana": (30.4515, -91.1871),
}
markers = {
    "Houston, Texas": 'o',
    "Matagorda, Texas": 'p',
    "Yucatán Peninsula": 's',
    "Grenada": '^',
    "St. Vincent": 'D',
    "Baton Rouge, Louisiana": '*',
}

# Configuração do mapa
stamen_terrain = cimgt.GoogleTiles(style='satellite')
fig, ax = plt.subplots(
    figsize=(9, 7),
    subplot_kw={"projection": stamen_terrain.crs}
)

# Extensão do mapa
ax.set_extent([-106, -50, 15, 40], crs=ccrs.PlateCarree())

# Adiciona imagem de fundo (mapa de terreno)
ax.add_image(stamen_terrain, 8)

# Adiciona as localidades como bolinhas vermelhas
for name, (lat, lon) in locations.items():
    ax.plot(lon, lat, markers[name], color='red', markersize=8, transform=ccrs.PlateCarree(), label=name)

# Configura rótulos dos eixos
ax.set_yticks(np.arange(latS , latN, 5), crs=ccrs.PlateCarree())
ax.set_xticks(np.linspace(lonW,lonE,9,dtype=int), crs=ccrs.PlateCarree())
   
lon_formatter = LongitudeFormatter(number_format='.1f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
lat_formatter = LatitudeFormatter(number_format='.1f',
                                      degree_symbol='')

ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)

boxes = [
    {'lonW': -100, 'lonE': -90, 'latS': 25, 'latN': 35, 'label': 'B'},
    # {'lonW': -66, 'lonE': -56, 'latS': 8, 'latN': 18, 'label': 'A'}
    {'lonW': -92, 'lonE': -82, 'latS': 17.5, 'latN': 22.5, 'label': 'A'}
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


# Adiciona legendas
ax.legend(loc="upper right", fontsize=9, title="Location")

# Títulos e rótulos
# ax.set_title("Special Locations for Beryl Analysis", fontsize=16)

# Mostra o mapa
plt.savefig('big_study_area.png', dpi=300, bbox_inches="tight")


