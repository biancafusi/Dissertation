import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib
import numpy as np
from matplotlib import cm
from matplotlib.colors import BoundaryNorm, TwoSlopeNorm, ListedColormap
from matplotlib.ticker import LogLocator, FuncFormatter, MaxNLocator, LinearLocator

matplotlib.use("Agg")

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
folder_of_data = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/native_resolution/'
# preciso colocar as files .nc da chuva na resolução nativa desses dados.


where_save_figure = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/paineis_chuva_instantanea_and_bias/'

# Dias escolhidos
days_selected = {
    'day_01': '2024-07-04T00',
    'day_03': '2024-07-05T16',
    'day_05': '2024-07-07T10'
}

# Experimentos selecionados
data_to_be_plotted = ['GPM-IMERG', 'GSMaP', 'ERA5', 'CP-30km', 'CP-15km', 'CP-60km']

# Letras para os subplots
letters = ['(a)', '(b)', '(c)']

# Extents para cada coluna
extents = [
    [-89, -69, 10, 30],    # (a) Day 01
    [-100, -80, 12.5, 32.5], # (b) Day 03
    [-105, -85, 17.5, 37.5]  # (c) Day 05
]

# Definir os níveis de cores
color_levels = [0.5, 1, 1.5, 2, 2.5, 3, 5, 6, 8, 10, 12, 16, 18, 22, 30]

# Criar painel: 6 linhas (experimentos) x 3 colunas (dias)
fig, axes = plt.subplots(nrows=6, ncols=3, figsize=(10, 20), subplot_kw={'projection': ccrs.PlateCarree()})

# Loop pelos experimentos e dias
for row_idx, experiment_file in enumerate(data_to_be_plotted):
    for col_idx, (day_name, initial_day) in enumerate(days_selected.items()):
        # Abrir o arquivo correto
        print(f'processing {experiment_file}')
        ds = xr.open_dataset(folder_of_data + f'{experiment_file}_native_hourly.nc').sel(time=initial_day)

        # Selecionar a variável de chuva
        rainfall = ds['rainfall']

        # Descobrir o extent para este subplot
        lonW, lonE, latS, latN = extents[col_idx]

        # Cortar área
        if experiment_file in ['ERA5', 'GSMaP']:
            rainfall_cropped = rainfall.sel(lat=slice(latN, latS), lon=slice(lonW, lonE))
        elif experiment_file == 'GPM-IMERG':
            rainfall_cropped = rainfall.sel(lat=slice(latS, latN), lon=slice(lonW, lonE))
        else:
            rainfall_cropped = rainfall.sel(lon=slice(lonW, lonE), lat=slice(latS, latN))

        # Máximo e média
        max_rainfall = rainfall_cropped.max().values
        mean_rainfall = rainfall_cropped.mean().values

        # Selecionar o subplot correto
        ax = axes[row_idx, col_idx]

        # Aqui criamos a colormap e os níveis
        cmap, levels = modified_jet_with_white()

        # Norm deve usar "ncolors = len(levels) - 1"
        norm = BoundaryNorm(levels, ncolors=cmap.N)

        # Agora sim seu pcolormesh:
        im = ax.pcolormesh(rainfall['lon'], rainfall['lat'], rainfall,
                        transform=ccrs.PlateCarree(),
                        cmap=cmap,
                        norm=norm)
        # Adicionar linhas de costa
        ax.coastlines()

        # Aplicar recorte para acompanhar o furacão
        ax.set_extent(extents[col_idx], crs=ccrs.PlateCarree())

        # Títulos apenas na primeira linha
        if row_idx == 0:
            date = initial_day + ' UTC'
            ax.set_title(f'{letters[col_idx]} {date}', fontsize=14)

        # Nome do experimento na primeira coluna de cada linha
        if col_idx == 0:
            ax.text(-0.25, 0.5, experiment_file, va='center', ha='right', rotation=90,
                    transform=ax.transAxes, fontsize=14, fontweight='bold')

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

# Ajustar espaço da figura
plt.tight_layout(rect=[0, 1, 0, 0])

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
plt.savefig(where_save_figure + 'painel_resolution_rainfall_FINAL.png', dpi=300, bbox_inches='tight')
plt.close()

print("Panel saved")