import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib
import cartopy.feature as cfeature

import numpy as np
from matplotlib import cm
from matplotlib.colors import BoundaryNorm, TwoSlopeNorm, ListedColormap
from matplotlib.ticker import LogLocator, FuncFormatter, MaxNLocator, LinearLocator

matplotlib.use("Agg")

'''
Plota para cada dia uma figura da chuva
'''

def modified_jet_with_white():
    # Seus níveis
    levels = [0.5, 1, 1.5, 2, 2.5, 3, 5, 6, 8, 10, 12, 16, 18, 22, 30]
    
    # Mapa jet original
    jet = cm.get_cmap('jet', 256)
    
    # Definimos quantas cores: 1 (branco) + restante dos níveis
    n_colors = len(levels)
    
    # 0.5 será branco
    white = np.array([1, 1, 1, 1])
    
    # Gerar cores do jet para os outros níveis (sem contar o primeiro)
    # Vamos espalhar as cores do jet uniformemente nos níveis restantes
    jet_colors = jet(np.linspace(0, 1, n_colors - 1))
    
    # Junta branco + jet_colors
    colors = np.vstack([white, jet_colors])
    
    # Cria nova colormap
    new_cmap = ListedColormap(colors)
    
    return new_cmap, levels

# Caminhos
folder_of_data = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/helene_rainfall_statistics/helene_rainfall_sliced/'
where_save_figure = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/helene_rainfall_statistics/helene_snapshots/'

# Experimentos selecionados
data_to_be_plotted = 'GSMaP'

# Definir os níveis de cores
color_levels = [0.5, 1, 1.5, 2, 2.5, 3, 5, 6, 8, 10, 12, 16, 18,22, 30]

projection=ccrs.PlateCarree(central_longitude=180.0, globe=None)

fig = plt.figure(figsize=(10, 15))
ax  = plt.axes(projection=projection)

ds = xr.open_dataset(folder_of_data + f'{data_to_be_plotted}_hourly.nc')
time = ds.time

print(time)
print('\n')
print(time[45])
print(time[60])
print(time[73])
exit()

# Selecionar a variável de chuva
rainfall = ds['rainfall']

# Descobrir o extent para este subplot
lonW, lonE, latS, latN = -92, -69, 17, 48

# Cortar o rainfall apenas para a área do extent
rainfall_cropped = rainfall.sel(lon=slice(lonW, lonE), lat=slice(latS, latN))

for t in range(len(time)):

    rainfall_selected = rainfall.isel(time=t)

    max_rainfall = rainfall_selected.max().values
    mean_rainfall = rainfall_selected.mean().values

    time_title = rainfall_selected.time.values


    # Aqui criamos a colormap e os níveis
    cmap, levels = modified_jet_with_white()

    # Norm deve usar "ncolors = len(levels) - 1"
    norm = BoundaryNorm(levels, ncolors=cmap.N)

    # Agora sim seu pcolormesh:
    im = ax.pcolormesh(rainfall_selected['lon'], rainfall_selected['lat'], rainfall_selected,
                    transform=ccrs.PlateCarree(),
                    cmap=cmap,
                    norm=norm)
    
    # Adicionar linhas de costa
    ax.add_feature(cfeature.COASTLINE, alpha=0.4, linewidth=0.4, edgecolor='black')
    ax.add_feature(cfeature.BORDERS, alpha=0.4, linewidth=0.4)
    ax.add_feature(cfeature.LAND, alpha=0.4, linewidth=0.4)
    ax.add_feature(cfeature.STATES, alpha=0.4, linewidth=0.2)
    ax.add_feature(cfeature.OCEAN, alpha=0.4, linewidth=0.3)
    ax.stock_img()

    # Aplicar recorte para acompanhar o furacão
    ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree())

    # Adicionar valores máximos e médios
    ax.text(0.05, 0.95, f'Max: {max_rainfall:.2f} mm/h\nMean: {mean_rainfall:.2f} mm/h',
            transform=ax.transAxes, fontsize=10, color='black', ha='left', va='top',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.5'))

    # Gridlines e labels
    gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
                        linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 8}
    gl.ylabel_style = {'size': 8}

    # Adicionar colorbar
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    cbar = fig.colorbar(im, cax=cbar_ax)

    # Configurar ticks da colorbar
    cbar.set_ticks(color_levels)
    cbar.ax.tick_params(labelsize=12)

    # Melhorar aparência geral
    cbar.set_label('Rainfall (mm/h)', fontsize=14)
    cbar.ax.tick_params(labelsize=12)

    # Salvar a figura
    plt.title(f'GSMaP at:' +np.datetime_as_string(time[t],unit='h'))
    plt.savefig(where_save_figure + f'helene_panels{t}.png', dpi=300, bbox_inches='tight')

    print("Salvo com sucesso!")

