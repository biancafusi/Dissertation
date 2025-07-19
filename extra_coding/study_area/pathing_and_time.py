import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Carrega os dados
helene = xr.open_dataset('/home/bianca/Documentos/masters/IBTrACS/tropycal/Helene.nc')
beryl = xr.open_dataset('/home/bianca/Documentos/masters/IBTrACS/tropycal/Beryl.nc')

# Função para plotar uma figura individual para um furacão
def plot_individual_hurricane(data, name, color):
    lats = data.lat.values
    lons = data.lon.values
    times = data.time.dt.strftime('%m-%d %H:%M').values

    fig = plt.figure(figsize=(10, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Ajuste da área do mapa
    buffer = 5  # margem para os limites
    ax.set_extent([lons.min() - buffer, lons.max() + buffer,
                   lats.min() - buffer, lats.max() + buffer])

    # Recursos geográficos
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.gridlines(draw_labels=True)

    # Plotar trajetória
    ax.plot(lons, lats, marker='o', color=color, label=name, transform=ccrs.PlateCarree())

    # Anotar o tempo em cada ponto
    for lon, lat, t in zip(lons, lats, times):
        ax.text(lon + 0.2, lat + 0.2, t, fontsize=6, transform=ccrs.PlateCarree())

    plt.title(f'Tracking do Furacão {name}')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'teste_pathing_time_{name}.png')

# Gerar figuras individuais
plot_individual_hurricane(helene, 'Helene', 'red')
plot_individual_hurricane(beryl, 'Beryl', 'blue')
