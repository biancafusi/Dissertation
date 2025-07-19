import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib
import numpy as np
from matplotlib import cm
from matplotlib.colors import BoundaryNorm, TwoSlopeNorm, ListedColormap
from matplotlib.ticker import LogLocator, FuncFormatter, MaxNLocator, LinearLocator

matplotlib.use("Agg")

# Caminhos
folder_of_data = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/ctt_datasets/'
# preciso colocar as files .nc da chuva na resolução nativa desses dados.

where_save_figure = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/ctt_figures/'

# Dias escolhidos
days_selected = {
    'day_01': '2024-07-04T00',
    'day_03': '2024-07-05T16',
    'day_05': '2024-07-07T10'
}

# Experimentos selecionados
data_to_be_plotted = ['CP-ON', 'CP-OFF', 'CP-1H', 'CP-3H', 'CP-D025', 'CP-D050',
     'CPSS-ON', 'CP-15km', 'CP-60km', 'CP-GFS', 'CP-29', 'CP-02T12', 'CP-1HD050']

# Letras para os subplots
letters = ['(a)', '(b)', '(c)']

# Extents para cada coluna
extents = [
    [-89, -69, 10, 30],    # (a) Day 01
    [-100, -80, 12.5, 32.5], # (b) Day 03
    [-105, -85, 17.5, 37.5]  # (c) Day 05
]
global_min = float('inf')
global_max = float('-inf')

for label in data_to_be_plotted:
    for initial_day in days_selected.values():
        ds = xr.open_dataset(folder_of_data + f'{label}_hourly.nc').sel(time=initial_day)
        variable = ds['ctt']
        lonW, lonE, latS, latN = extents[list(days_selected.values()).index(initial_day)]
        variable_cropped = variable.sel(lon=slice(lonW, lonE), lat=slice(latS, latN))
        
        min_val = float(variable_cropped.min())
        max_val = float(variable_cropped.max())
        
        global_min = min(global_min, min_val)
        global_max = max(global_max, max_val)

# Arredondar para múltiplos de 10
vmin = int(np.floor(global_min / 10) * 10)
vmax = int(np.ceil(global_max / 10) * 10)
ticks = np.arange(vmin, vmax + 10, 10)


for label in data_to_be_plotted:
    print(f'Processing {label}')
    
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(14, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    
    for col_idx, (day_name, initial_day) in enumerate(days_selected.items()):
        # Abrir dataset e selecionar o tempo
        ds = xr.open_dataset(folder_of_data + f'{label}_hourly.nc').sel(time=initial_day)
        
        # Selecionar variável de chuva
        variable = ds['ctt']
        
        # Extensão geográfica para esse subplot
        lonW, lonE, latS, latN = extents[col_idx]
        
        # Recorte espacial padrão
        varible_cropped = variable.sel(lon=slice(lonW, lonE), lat=slice(latS, latN))
        
        # Estatísticas
        min_variable = varible_cropped.min().values
        # mean_variable = varible_cropped.mean().values
        
        # Subplot
        ax = axes[col_idx]
        
        # Colormap e normalização
        im = ax.pcolormesh(variable['lon'], variable['lat'], variable,
                   transform=ccrs.PlateCarree(),
                   cmap='jet', vmin=vmin, vmax=vmax)
        
        # Estética
        ax.coastlines()
        ax.set_extent(extents[col_idx], crs=ccrs.PlateCarree())
        ax.set_title(f'{letters[col_idx]} {initial_day} UTC', fontsize=12)

        
        ax.text(0.05, 0.95, f'Min: {min_variable:.2f} °C',
                transform=ax.transAxes, fontsize=9, color='black', ha='left', va='top',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.5'))
        
        # Grid
        # Gridlines e labels
        gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
                          linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {'size': 8}
        gl.ylabel_style = {'size': 8}

    # Layout e colorbar
    plt.tight_layout(rect=[0, 1, 0, 0])

    cbar_ax = fig.add_axes([0.92, 0.2, 0.02, 0.6])
    cbar = fig.colorbar(im, cax=cbar_ax, ticks=ticks)
    cbar.set_label('Cloud Top Temperature (°C)', fontsize=12)
    cbar.ax.tick_params(labelsize=10)
    
    # Salvar figura
    fig_name = f'{where_save_figure}{label}_ctt_panel.png'
    plt.savefig(fig_name, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved panel for {label}")


# ============================= PLOT COM TODOS ============================ #

# Experimentos selecionados para o painel
experiments_to_plot = ['GPM-MERGIR', 'CP-OFF', 'CP-ON', 'CP-D050', 'CP-3H']

# -----------------------------
# 2. Criar a figura
# -----------------------------
fig, axes = plt.subplots(nrows=5, ncols=3, figsize=(8, 10),
                         subplot_kw={'projection': ccrs.PlateCarree()})

# -----------------------------
# 3. Loop pelos experimentos e dias
# -----------------------------
for row_idx, experiment_file in enumerate(experiments_to_plot):
    for col_idx, (day_name, initial_day) in enumerate(days_selected.items()):
        print(f'processing {experiment_file} - {initial_day}')
        
        ds = xr.open_dataset(folder_of_data + f'{experiment_file}_hourly.nc').sel(time=initial_day)
        ctt = ds['ctt']

        lonW, lonE, latS, latN = extents[col_idx]
        ctt_cropped = ctt.sel(lon=slice(lonW, lonE), lat=slice(latS, latN))

        min_ctt = ctt_cropped.min().values

        ax = axes[row_idx, col_idx]

        im = ax.pcolormesh(ctt['lon'], ctt['lat'], ctt,
                           transform=ccrs.PlateCarree(),
                           cmap='jet', vmin=vmin, vmax=vmax)

        ax.coastlines()
        ax.set_extent(extents[col_idx], crs=ccrs.PlateCarree())

        if row_idx == 0:
            ax.set_title(f'{letters[col_idx]} {initial_day} UTC', fontsize=12)

        if col_idx == 0:
            ax.text(-0.35, 0.5, experiment_file, va='center', ha='right', rotation=90,
                    transform=ax.transAxes, fontsize=14, fontweight='bold')

        ax.text(0.05, 0.95, f'Min: {min_ctt:.2f} °C',
                transform=ax.transAxes, fontsize=9, color='black', ha='left', va='top',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.5'))

        gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
                          linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {'size': 8}
        gl.ylabel_style = {'size': 8}

# -----------------------------
# 4. Layout e Colorbar
# -----------------------------
plt.tight_layout(rect=[0, 1, 0, 0])

cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax, ticks=ticks)
cbar.set_label('Cloud Top Temperature (°C)', fontsize=14)
cbar.ax.tick_params(labelsize=12)

# -----------------------------
# 5. Salvar figura
# -----------------------------
plt.savefig(where_save_figure + 'painel_ctt_selected_experiments_FINAL.png', dpi=300, bbox_inches='tight')
plt.close()

print("Painel CTT salvo com sucesso.")

# # ======================================== Plot anterior porem com o bias ========================= #
# # -----------------------------
# # Experimentos CP (previsões)
# # -----------------------------
# experiments_to_plot = ['CP-OFF', 'CP-ON', 'CP-D050', 'CP-3H']
# reference_exp = 'GPM-MERGIR'

# # Defina os limites do bias para a colormap (ajuste conforme seus dados)
# bias_limit = 20  # por exemplo, -20 a 20 °C
# cmap = plt.cm.RdBu_r
# norm = TwoSlopeNorm(vmin=-bias_limit, vcenter=0, vmax=bias_limit)
# ticks = np.arange(-bias_limit, bias_limit + 5, 5)

# # -----------------------------
# # Criar a figura
# # -----------------------------
# fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(8, 10),
#                          subplot_kw={'projection': ccrs.PlateCarree()})

# # -----------------------------
# # Loop pelos experimentos e dias
# # -----------------------------
# for row_idx, experiment_file in enumerate(experiments_to_plot):
#     for col_idx, (day_name, initial_day) in enumerate(days_selected.items()):
#         print(f'Processing BIAS {experiment_file} - {initial_day}')
        
#         # Abrir previsão e referência
#         ds_ref = xr.open_dataset(folder_of_data + f'{reference_exp}_hourly.nc').sel(time=initial_day)
#         ds_exp = xr.open_dataset(folder_of_data + f'{experiment_file}_hourly.nc').sel(time=initial_day)
        
#         ctt_ref = ds_ref['ctt']
#         ctt_exp = ds_exp['ctt']
        
#         # Recorte espacial
#         lonW, lonE, latS, latN = extents[col_idx]
#         ctt_ref_cropped = ctt_ref.sel(lon=slice(lonW, lonE), lat=slice(latS, latN))
#         ctt_exp_cropped = ctt_exp.sel(lon=slice(lonW, lonE), lat=slice(latS, latN))
        
#         # Cálculo do BIAS
#         bias = ctt_exp_cropped - ctt_ref_cropped
#         mean_bias = bias.mean().values
        
#         # Plot
#         ax = axes[row_idx, col_idx]
#         im = ax.pcolormesh(ctt_exp_cropped['lon'], ctt_exp_cropped['lat'], bias,
#                            transform=ccrs.PlateCarree(), cmap=cmap, norm=norm)

#         ax.coastlines()
#         ax.set_extent(extents[col_idx], crs=ccrs.PlateCarree())

#         if row_idx == 0:
#             ax.set_title(f'{letters[col_idx]} {initial_day} UTC', fontsize=12)

#         if col_idx == 0:
#             ax.text(-0.35, 0.5, experiment_file, va='center', ha='right', rotation=90,
#                     transform=ax.transAxes, fontsize=14, fontweight='bold')

#         ax.text(0.05, 0.95, f'Mean Bias: {mean_bias:.2f} °C',
#                 transform=ax.transAxes, fontsize=9, color='black', ha='left', va='top',
#                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.5'))

#         gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
#                           linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
#         gl.top_labels = False
#         gl.right_labels = False
#         gl.xlabel_style = {'size': 8}
#         gl.ylabel_style = {'size': 8}

# # -----------------------------
# # Colorbar
# # -----------------------------
# plt.tight_layout(rect=[0, 1, 0, 0])
# cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
# cbar = fig.colorbar(im, cax=cbar_ax, ticks=ticks)
# cbar.set_label('CTT Bias (°C)', fontsize=14)
# cbar.ax.tick_params(labelsize=12)

# # -----------------------------
# # Salvar figura
# # -----------------------------
# plt.savefig(where_save_figure + 'painel_ctt_bias_selected_experiments.png', dpi=300, bbox_inches='tight')
# plt.close()

# print("Painel de BIAS CTT salvo com sucesso.")


# ============================= PLOT COM TODOS - RESOLUÇÃO NATIVA ============================ #

# Experimentos selecionados para o painel
experiments_to_plot = ['GPM-MERGIR', 'CP-30km', 'CP-15km', 'CP-60km']

# -----------------------------
# 2. Criar a figura
# -----------------------------
fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(8, 10),
                         subplot_kw={'projection': ccrs.PlateCarree()})

# -----------------------------
# 3. Loop pelos experimentos e dias
# -----------------------------
print('\n')
print('now plotting the resolution experiments')
for row_idx, experiment_file in enumerate(experiments_to_plot):
    for col_idx, (day_name, initial_day) in enumerate(days_selected.items()):
        print(f'processing {experiment_file} - {initial_day}')
        
        ds = xr.open_dataset('/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/ctt_native_resolution/' 
                             + f'{experiment_file}_hourly.nc').sel(time=initial_day)
        ctt = ds['ctt']

        lonW, lonE, latS, latN = extents[col_idx]
        ctt_cropped = ctt.sel(lon=slice(lonW, lonE), lat=slice(latS, latN))
        print(ctt_cropped)

        min_ctt = ctt_cropped.min().values

        ax = axes[row_idx, col_idx]

        im = ax.pcolormesh(ctt['lon'], ctt['lat'], ctt,
                           transform=ccrs.PlateCarree(),
                           cmap='jet', vmin=vmin, vmax=vmax)

        ax.coastlines()
        ax.set_extent(extents[col_idx], crs=ccrs.PlateCarree())

        if row_idx == 0:
            ax.set_title(f'{letters[col_idx]} {initial_day} UTC', fontsize=12)

        if col_idx == 0:
            ax.text(-0.35, 0.5, experiment_file, va='center', ha='right', rotation=90,
                    transform=ax.transAxes, fontsize=14, fontweight='bold')

        ax.text(0.05, 0.95, f'Min: {min_ctt:.2f} °C',
                transform=ax.transAxes, fontsize=9, color='black', ha='left', va='top',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.5'))

        gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
                          linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {'size': 8}
        gl.ylabel_style = {'size': 8}

# -----------------------------
# 4. Layout e Colorbar
# -----------------------------
plt.tight_layout(rect=[0, 1, 0, 0])

cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax, ticks=ticks)
cbar.set_label('Cloud Top Temperature (°C)', fontsize=14)
cbar.ax.tick_params(labelsize=12)

# -----------------------------
# 5. Salvar figura
# -----------------------------
plt.savefig(where_save_figure + 'painel_ctt_native_resolution_FINAL.png', dpi=300, bbox_inches='tight')
plt.close()

print("Painel CTT salvo com sucesso.")