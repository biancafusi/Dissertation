import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xskillscore as xs
import matplotlib
from netCDF4 import Dataset    
import cartopy.crs as ccrs
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cartopy.feature as cfeature

matplotlib.use("Agg")


folder_of_data = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/helene_rainfall_statistics/helene_rainfall_sliced/'
where_save_figure = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/helene_rainfall_statistics/helene_correlation_per_day/'
# # ========= Plotagem do mapa de correlação em cada dia ====================== #

# # 1) Criar as listas com os tempos que serão initial_day e final_day nos slices futuros
# days = {
#     'day_01': ['2024-07-03T00', '2024-07-04T00'],
#     'day_02': ['2024-07-04T00', '2024-07-05T00'],
#     'day_03': ['2024-07-05T00', '2024-07-06T00'],
#     'day_04': ['2024-07-06T00', '2024-07-07T00'],
#     'day_05': ['2024-07-07T00', '2024-07-08T00'],
#     'day_06': ['2024-07-08T00', '2024-07-09T00'], 
# }

# # print(days['day_01'][0]) # assim é como acessar o dicionário

# # 2) loop com o cálculo do pearson correlation:
# experiments = data_information = ['ERA5','GSMap', 'CP-ON', 'CP-OFF', 'CP-1H', 'CP-3H', 'CP-D025', 'CP-D050',
#     'CPSS-ON', 'CP-15km', 'CP-60km', 'CP-GFS', 'CP-29', 'CP-02T12', 'CP-1HD050']

# # Loop para cada experimento
# # Loop para cada experimento
# for experiment_file in experiments:
#     # Criar uma figura com subplots para os 5 dias
#     fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 6), subplot_kw={'projection': ccrs.PlateCarree()})

#     for i, (day_name, (initial_day, final_day)) in enumerate(days.items()):
#         observation = xr.open_dataset(folder_of_data + 'GPM-IMERG_hourly.nc').sel(time=slice(initial_day, final_day))
#         forecast = xr.open_dataset(folder_of_data + f'{experiment_file}_hourly.nc').sel(time=slice(initial_day, final_day))

#         r = xs.pearson_r(observation, forecast, dim='time')  # correlação no tempo
#         r = r['rainfall']

#         # Plotar cada dia em uma posição diferente no painel
#         # Calcular as coordenadas de linha e coluna
#         row = i // 3  # Linha (divisão inteira)
#         col = i % 3   # Coluna (resto da divisão)

#         # Plotar cada dia em uma posição diferente no painel
#         ax = axes[row, col]  # Selecionar o subgráfico correto
#         im = ax.pcolormesh(r['lon'], r['lat'], r, 
#                            transform=ccrs.PlateCarree(), 
#                            cmap='RdBu_r', vmin=-1, vmax=1)

#         ax.coastlines()
#         ax.set_title(f'{day_name} - {initial_day} to {final_day}')

#         # Adicionar gridlines e labels
#         gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
#                           linewidth=0.5, color='gray', alpha=0.7, linestyle='--')
#         gl.top_labels = False  # Remove label superior
#         gl.right_labels = False  # Remove label da direita
#         gl.xlabel_style = {'size': 10}
#         gl.ylabel_style = {'size': 10}
#         gl.xformatter = ccrs.cartopy.mpl.ticker.LongitudeFormatter()
#         gl.yformatter = ccrs.cartopy.mpl.ticker.LatitudeFormatter()

#     # Adicionar a barra de cores

#     cbar = fig.colorbar(im, ax=axes, orientation='vertical',fraction=0.025, pad=0.04)
#     cbar.set_label('Pearson Correlation')

#     # Salvar a figura
#     plt.suptitle(f'Correlation of: {experiment_file}', fontsize=16)
#     plt.tight_layout(rect=[0, 1, 1, 0.96])  # Ajustar para o título não sobrepor o gráfico
#     plt.savefig(where_save_figure + f'correlation_{experiment_file}_all_days.png', dpi=300, bbox_inches='tight')
#     plt.close()


# =================== PAINEL GIGANTE =========================================== #
# Dias escolhidos
days_selected = {
    'day_01': ['2024-09-25T00', '2024-09-26T00'],
    'day_02': ['2024-09-26T00', '2024-09-27T00'],
    'day_03': ['2024-09-27T00', '2024-09-28T00'],
}


# Experimentos selecionados
experiments_selected = ['ERA5', 'CP-OFF', 'CP-ON', 'CP-1HD050', 'CP-25']

# Letras para os subplots
letters = ['(a)', '(b)', '(c)']

# Criar painel: 5 linhas (experimentos) x 3 colunas (dias)
fig, axes = plt.subplots(nrows=5, ncols=3, figsize=(10, 17), subplot_kw={'projection': ccrs.PlateCarree()})

# Loop pelos experimentos e dias
for row_idx, experiment_file in enumerate(experiments_selected):
    for col_idx, (day_name, (initial_day, final_day)) in enumerate(days_selected.items()):
        # Abrir os dados de observação e previsão
        observation = xr.open_dataset(folder_of_data + 'GPM-IMERG_hourly.nc').sel(time=slice(initial_day, final_day))
        forecast = xr.open_dataset(folder_of_data + f'{experiment_file}_hourly.nc').sel(time=slice(initial_day, final_day))

        # Calcular a correlação de Pearson no tempo
        r = xs.pearson_r(observation, forecast, dim='time')
        r = r['rainfall']

        # Selecionar o subplot correto
        ax = axes[row_idx, col_idx]
        im = ax.pcolormesh(r['lon'], r['lat'], r, 
                           transform=ccrs.PlateCarree(), 
                           cmap='RdBu_r', vmin=-1, vmax=1)

        # Adicionar linhas de costa e título
        #ax.coastlines()
        ax.add_feature(cfeature.COASTLINE, alpha=0.4, linewidth=0.4, edgecolor='black')
        ax.add_feature(cfeature.BORDERS, alpha=0.4, linewidth=0.4)
        ax.add_feature(cfeature.LAND, alpha=0.4, linewidth=0.4)
        ax.add_feature(cfeature.STATES, alpha=0.4, linewidth=0.2)
        ax.add_feature(cfeature.OCEAN, alpha=0.4, linewidth=0.3)
    
        
        # Títulos apenas na primeira linha (superior)
        if row_idx == 0:
            date = initial_day[:10]
            ax.set_title(f'{letters[col_idx]} Day {day_name[-2:]} - {date}', fontsize=14)

        # Label do experimento à esquerda
        if col_idx == 0:
            ax.text(-0.28, 0.5, experiment_file, va='center', ha='right', rotation=90,
                    transform=ax.transAxes, fontsize=14, fontweight='bold')

        # Gridlines com labels apenas nas bordas
        gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
                          linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False

        # se eu quiser legenda dos eixos só nas bordas
        # if col_idx != 0:
        #     gl.left_labels = False
        # if row_idx != 4:
        #     gl.bottom_labels = False

# Ajustar o espaço da figura para comportar os eixos
plt.tight_layout(rect=[1, 1, 0, 0])

# Adicionar uma única barra de cores
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label('Pearson Correlation Coefficient', fontsize=14)
cbar.ax.tick_params(labelsize=14)  # <-- Esta linha aqui ajusta o tamanho dos números


# Salvar a figura
plt.savefig(where_save_figure + 'painel_correlation_selected_experiments_days_nomeado.png', dpi=300, bbox_inches='tight')
plt.close()

print("Painel salvo com sucesso!")