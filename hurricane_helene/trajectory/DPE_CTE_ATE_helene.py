import math
import xarray as xr
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import geopy

from namelist_helene_for_errors import *


from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from geopy.distance import geodesic, great_circle
import matplotlib.ticker as ticker

matplotlib.use("Agg")

'''
Objective: Creates 3 figures: a panel with distance error + mae, rmse;

STATUS: 

PRECISO MODIFICAR AQUI PARA O HELENE

LAST CHECKED: MARCH 19 2025
'''
window_size = 3

# Função para aplicar a média móvel
def apply_moving_average(data, window_size):
    # Usando pandas para calcular a média móvel
    return pd.Series(data).rolling(window=window_size, min_periods=1).mean().values

def calculating_errors_inside_df(df_reference, df_model, label, color):

    # This function calculated DPE inside my daframe

    # Fazendo merge pelo time step
    df_merged = pd.merge(df_reference, df_model, on='time step', suffixes=('_NOAA', '_MODEL'))
    df_merged[['lat_NOAA', 'lon_NOAA', 'lat_MODEL', 'lon_MODEL']] = df_merged[['lat_NOAA', 'lon_NOAA', 'lat_MODEL', 'lon_MODEL']].astype(float)

    # Calcula o erro conforme a funcao que defini
    df_merged['erro'] = df_merged.apply(
        lambda row: great_circle(  #MUDAR AQ DPS
            (row['lat_NOAA'], row['lon_NOAA']),
            (row['lat_MODEL'], row['lon_MODEL'])
        ).km,
        axis=1
    )
    
    # Salva isso em uma tabela do excel
    excel_name = saving_excel_folder+f'track_data_{label}_with_error.xlsx'
    with pd.ExcelWriter(excel_name) as writer:
        df_merged.to_excel(writer, sheet_name='hole_field', index=False)
        # df_oceano.to_excel(writer, sheet_name='Oceano', index=False)
        # df_continente.to_excel(writer, sheet_name='Continente', index=False)
    print(f"Tabelas com erro salvas com sucesso em {excel_name}!")

    return df_merged['time step'], df_merged['erro'], color


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

dataframes = {}

# adding NOAA data:
df_NOAA = pd.DataFrame({
    'time step': np.arange(0, len(time), 1),
    'mslp': mslp_points_NOAA,
    'lat': lat_points_NOAA,
    'lon': lon_points_NOAA,
    'color': 'darkgreen'
})

dataframes['NOAA'] = df_NOAA

# ========== OUTROS DATASETS ==========
for label, color, input_file_data in data_information:
    print(f'Processing {label} data ...')
    
    if label == 'ERA5':
        # abrindo dados do ERA5
        dataset_dry = xr.open_dataset('/mnt/beegfs/bianca.fusinato/monan/comparison/helene/era5/x1.655362.era5_helene_dry_native.nc').rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'msl': 'mslp'})
        
        dataset_dry = (dataset_dry.assign_coords(lon=((dataset_dry.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')

        lat_data = dataset_dry.lat.sel(lat=slice(latS,latN))
        lon_data = dataset_dry.lon.sel(lon=slice(lonW, lonE))
        MSLP_data = dataset_dry.mslp.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)) / 100  # to hPa

        dataset_wind = xr.open_dataset(input_file_data).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon'})
        dataset_wind = (dataset_wind.assign_coords(lon=((dataset_wind.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')

    else:
        model_data = (xr.open_dataset(input_file_data).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'})).sel(time=time, lat=slice(latS, latN), lon=slice(lonW, lonE))
        lat_data = model_data.lat
        lon_data = model_data.lon
        MSLP_data = model_data.mslp / 100

    # Encontrar trilha do ciclone para esse dataset
    lat_points, lon_points, mslp_points, time_steps = [], [], [], []

    dlat, dlon = 10, 10
    
    for t in range(len(time)):
        MSLP_t = MSLP_data.isel(time=t)
        # Região de busca
        upper_lat, lower_lat = lat_points_NOAA[t] + dlat, lat_points_NOAA[t] - dlat
        left_lon, right_lon = lon_points_NOAA[t] - dlon, lon_points_NOAA[t] + dlon
        
        # Seleciona região
        lon_sliced = lon_data.sel(lon=slice(left_lon, right_lon))
        if label == 'ERA5':

            # Preciso verificar se isso aqui está certo
            lat_sliced = lat_data.sel(lat=slice(lower_lat,upper_lat))
            MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(lower_lat,upper_lat))


        else:
            lat_sliced = lat_data.sel(lat=slice(lower_lat, upper_lat))
            lon_sliced = lon_data.sel(lon=slice(left_lon, right_lon))
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
            time_steps.append(t)
    
    datasets.append({
        'label': label,
        'lat': lat_data,
        'lon': lon_data,
        'mslp_trail_lat': lat_points,
        'mslp_trail_lon': lon_points,
        'color': color,
        'marker': '^'
    })

    # Criar DataFrame
    df = pd.DataFrame({
        'time step': time_steps,
        'mslp': mslp_points,
        'lat': lat_points,
        'lon': lon_points,
        'color': color
    })

    # Here I am saving the dataframes into one thing to further manipulate it and add errors
    dataframes[label] = df

# ############################## CALCULATING ERRORS AND SAVING INTO ANOTHER TABLE ################
df_reference = dataframes['NOAA']

errors_dict = {}

for label in dataframes.keys():
    if label == 'NOAA':
        continue

    df_model = dataframes[label]
    color = next((d['color'] for d in datasets if d['label'] == label), 'black')  # Pega a cor do dataset

    # COMPUTING DPE:
    time_step, erro, _ = calculating_errors_inside_df(df_reference, df_model, label, color)

    errors_dict[label] = {
        'time': time_step,
        'erro': erro,
        'color': color
    }


# Definir a referência de tempo inicial
time_array = time.values  # Seu vetor de tempo
time_ref = time_array[0]  # Primeiro valor como referência

# Calcular o número de horas após a referência
hours_after = [(t - time_ref) / pd.Timedelta(hours=1) for t in time_array]

# Criar os rótulos formatados
time_labels = [f"{int(h)}" for h in hours_after]

### Smoothing the lines:
# Aplicar a média móvel a todos os erros antes de plotar
for label in errors_dict.keys():
    errors_dict[label]['erro'] = apply_moving_average(errors_dict[label]['erro'], window_size)

# ============================= MAE AND RMSE ===========================================

mae_rmse_dict = {}

df_reference = dataframes['NOAA']

for label, df_model in dataframes.items():
    if label == 'NOAA':
        continue

    # Get smoothed error
    error = errors_dict[label]['erro']
    
    # Assuming 'errors_dict[label]['erro']' is already the difference between model and NOAA
    # But if not, you might want to recompute the error as: error = np.abs(df_model - df_reference)

    mae = mean_absolute_error(np.zeros_like(error), error)  # MAE with respect to zero (true error)
    rmse = root_mean_squared_error(np.zeros_like(error), error)

    mae_rmse_dict[label] = {
        'mae': mae,
        'rmse': rmse,
        'color': errors_dict[label]['color']
    }

labels = list(mae_rmse_dict.keys())
maes = [mae_rmse_dict[l]['mae'] for l in labels]
rmses = [mae_rmse_dict[l]['rmse'] for l in labels]
colors = [mae_rmse_dict[l]['color'] for l in labels]

# Sort by MAE
sorted_items = sorted(mae_rmse_dict.items(), key=lambda x: x[1]['mae'])
labels = [item[0] for item in sorted_items]
maes = [item[1]['mae'] for item in sorted_items]
rmses = [item[1]['rmse'] for item in sorted_items]

y = np.arange(len(labels))  # Y positions
height = 0.35

# ========================= MAE and RMSE Graph ============================= #

fig, ax = plt.subplots(figsize=(12, 10))

# Plot MAE in black
bars1 = ax.barh(
    y - height / 2, maes, height,
    label='MAE', color='black'
)

# Plot RMSE in grey with hatch
bars2 = ax.barh(
    y + height / 2, rmses, height,
    label='RMSE', color='grey', hatch='//', edgecolor='dimgray'
)

# Add labels and style
ax.set_xlabel('Distance from the reference (km)', fontsize=16)
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=14)
ax.invert_yaxis()  # Top = best
ax.legend(fontsize=16)
ax.grid(axis='x', linestyle='--', alpha=0.7)

max_val = max(max(maes), max(rmses))

ax.set_xticks(np.arange(0, max_val, 20))
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)

plt.tight_layout()
plt.savefig(where_to_save+"ONLY_mae_rmse_horizontal_custom.png", dpi=300)


## ========================= PANEL PLOT 2+ 3 ========================== #
# Definindo labels ordenados por MAE
sorted_items = sorted(mae_rmse_dict.items(), key=lambda x: x[1]['mae'])
labels = [item[0] for item in sorted_items]
maes = [item[1]['mae'] for item in sorted_items]
rmses = [item[1]['rmse'] for item in sorted_items]

y = np.arange(len(labels))  # Y positions
height = 0.35

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 10))  # Painel lado a lado

# # ===================== (a) Plot 1 - Curvas de erro suavizado =====================

for label in errors_dict.keys():
    erro_suavizado = errors_dict[label]['erro']
    color = errors_dict[label]['color']

    if label == 'CP-OFF':
        linestyle = '--'
    elif label == 'CP-ON':
        linestyle = '-.'
    else:
        linestyle = '-'

    ax1.plot(
        time_labels, erro_suavizado,
        color=color, linestyle=linestyle,
        linewidth=2.2 if label in ['CP-OFF', 'CP-ON'] else 1.8,
        label=label
    )

# === Linhas verticais E e F === #
line_positions = {'Landfall': 9}
y_start = 0
y_end = 150

for label, xpos in line_positions.items():
    ax1.plot([xpos, xpos], [y_start, y_end], color='steelblue', linestyle=':', linewidth=2.0)
    ax1.text(xpos, ax1.get_ylim()[1]*0.956, label, color='steelblue', fontsize=16,
             ha='center', va='bottom')

ax1.set_xticks(ticks=range(len(time_labels)))
ax1.set_xticklabels(time_labels, rotation=45, fontsize=16)
ax1.set_xlabel(ax_label, fontsize=16)
ax1.set_ylabel('Error (km)', fontsize=16)
ax1.grid(True)
ax1.legend(fontsize=14)
ax1.tick_params(axis='x', labelsize=16)
ax1.tick_params(axis='y', labelsize=16)
ax1.set_title('(a) Distance error over time', fontsize=16)

# ===================== (b) Plot 2 - MAE e RMSE =====================

bars1 = ax2.barh(y - height / 2, maes, height, label='MAE', color='black')
bars2 = ax2.barh(y + height / 2, rmses, height, label='RMSE', color='grey', hatch='//', edgecolor='dimgray')

ax2.set_xlabel('Distance from the reference (km)', fontsize=16)
ax2.set_yticks(y)
ax2.set_yticklabels(labels, fontsize=16)
ax2.invert_yaxis()
ax2.legend(fontsize=16)
ax2.grid(axis='x', linestyle='--', alpha=0.7)

max_val = max(max(maes), max(rmses))
ax2.set_xticks(np.arange(0, max_val + 20, 20))
ax2.tick_params(axis='x', labelsize=16)
ax2.tick_params(axis='y', labelsize=16)
ax2.set_title('(b) MAE and RMSE by experiment', fontsize=16)

# ===================== Salvar o painel =====================
plt.tight_layout()
plt.savefig(where_to_save+"PANEL_DPE_mae_rmse_FINAL.png", dpi=300, bbox_inches='tight')


# ===================================== MEDIA MONAN ============================================ #
# monan_maes = []
# monan_rmses = []
# # Coleta os valores de MAE/RMSE dos modelos MONAN (prefixo CP-)
# for label, df_model in dataframes.items():
#     if not label.startswith("CP-"):
#         continue

#     error = errors_dict[label]['erro']
#     mae = mean_absolute_error(np.zeros_like(error), error)
#     rmse = root_mean_squared_error(np.zeros_like(error), error)

#     monan_maes.append(mae)
#     monan_rmses.append(rmse)

# # Média dos modelos MONAN
# monan_mae_mean = np.mean(monan_maes)
# monan_rmse_mean = np.mean(monan_rmses)

# # ERA5
# era5_error = errors_dict['ERA5']['erro']
# era5_mae = mean_absolute_error(np.zeros_like(era5_error), era5_error)
# era5_rmse = root_mean_squared_error(np.zeros_like(era5_error), era5_error)

# # Preparando para plotagem
# labels = ['MONAN', 'ERA5']
# maes = [monan_mae_mean, era5_mae]
# rmses = [monan_rmse_mean, era5_rmse]
# y = np.arange(len(labels))
# height = 0.25

# fig, ax = plt.subplots(figsize=(12, 6))

# # MAE - preto
# ax.barh(
#     y - height / 2, maes, height,
#     label='MAE', color='black'
# )

# # RMSE - cinza com hachura
# ax.barh(
#     y + height / 2, rmses, height,
#     label='RMSE', color='grey', hatch='//', edgecolor='dimgray'
# )

# # Estilo e rótulos
# ax.set_xlabel('Distance from the reference (km)', fontsize=16)
# ax.set_yticks(y)
# ax.set_yticklabels(labels, fontsize=16)
# ax.invert_yaxis()
# ax.legend(fontsize=16)
# ax.grid(axis='x', linestyle='--', alpha=0.7)

# max_val = max(max(maes), max(rmses))
# ax.set_xticks(np.arange(0, max_val + 10, 10))
# ax.tick_params(axis='x', labelsize=14)
# ax.tick_params(axis='y', labelsize=14)

# plt.tight_layout()
# plt.savefig("/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/statistical_metrics/helene_results/barplot_monan_vs_era5_mae_rmse_FINAL.png", dpi=300)


# ============================== Computing and plotting CTE and ATE ============================ #
def bearing(coord_start, coord_end):
    lat_start, lon_start = coord_start
    lat_end, lon_end = coord_end

    lat_start = math.radians(lat_start)
    lat_end = math.radians(lat_end)
    longitude_difference = math.radians(lon_end - lon_start)

    arg_1 = math.sin(longitude_difference) * math.cos(lat_end)
    arg_2 = math.cos(lat_start) * math.sin(lat_end) - math.sin(lat_start) * math.cos(lat_end) * math.cos(longitude_difference)
    bearing_rad = math.atan2(arg_1, arg_2)

    # Converte para graus e normaliza para 0–360°
    bearing_deg = (math.degrees(bearing_rad) + 360) % 360

    return bearing_deg
# =================== CORES POR LABEL ======================

label_colors = {
    'ERA5': 'blue',
    'CP-ON': 'red',
    'CP-OFF': 'black',
    'CP-15km': 'magenta',
    'CP-25': 'darkorange',
    'CP-1HD050': 'cyan'
}

# Constante de raio da Terra em km (usada para consistência)
EARTH_RADIUS = geopy.distance.EARTH_RADIUS  # 6371.0 km

# Armazena os erros para cada modelo
errors_by_model = {}

for label, df_model in dataframes.items():
    if label == 'NOAA':
        continue

    cte_list, ate_list, time_list = [], [], []

    for t in range(len(time_labels) - 1):
        coord_ref_present = (df_reference.iloc[t]['lat'], df_reference.iloc[t]['lon'])
        coord_ref_next = (df_reference.iloc[t+1]['lat'], df_reference.iloc[t+1]['lon'])
        coord_model = (df_model.iloc[t]['lat'], df_model.iloc[t]['lon'])

        distance_start_third = great_circle(coord_ref_present, coord_model).km / EARTH_RADIUS
        bearing_start_third = math.radians(bearing(coord_ref_present, coord_model))
        bearing_start_end = math.radians(bearing(coord_ref_present, coord_ref_next))

        cte = math.asin(math.sin(distance_start_third) * math.sin(bearing_start_third - bearing_start_end)) * EARTH_RADIUS
        cte_angular = cte / EARTH_RADIUS
        ate = math.acos(math.cos(distance_start_third) / math.cos(cte_angular)) * EARTH_RADIUS

        cte_list.append(cte)
        ate_list.append(ate)
        time_list.append(df_reference.iloc[t]['time step'])

    cte_smoothed = apply_moving_average(cte_list, window_size)
    ate_smoothed = apply_moving_average(ate_list, window_size)

    df_errors = pd.DataFrame({
        'time step': time_list,
        'CTE (km)': cte_smoothed,
        'ATE (km)': ate_smoothed
    })

    errors_by_model[label] = df_errors

# =================== PLOTAGEM ATUALIZADA ======================
fig, axes = plt.subplots(2, 1, figsize=(16, 10), sharex=True)

# Subplot (a) — Cross-Track Error
axes[0].set_title("(a) Cross-Track Error over time", fontsize=16)
axes[0].set_ylabel("Cross-Track Error (km)", fontsize=16)

# Subplot (b) — Along-Track Error
axes[1].set_title("(b) Along-Track Error over time", fontsize=16)
axes[1].set_ylabel("Along-Track Error (km)", fontsize=16)
axes[1].set_xlabel(ax_label, fontsize=16)

for label, df in errors_by_model.items():
    color = label_colors.get(label, 'gray')
    linestyle = '--' if label == 'CP-OFF' else '-.' if label == 'CP-ON' else '-'

    # Plot for Cross-Track and Along-Track Errors
    axes[0].plot(time_labels[:-1], df['CTE (km)'], label=label, color=color, linestyle=linestyle)
    axes[1].plot(time_labels[:-1], df['ATE (km)'], label=label, color=color, linestyle=linestyle)

print(time_labels[9])
# === Linhas verticais — subplot (a) CTE === #
line_positions = {'Landfall': 9}

for label, xpos in line_positions.items():
    axes[0].plot([xpos, xpos], [-110, 50], color='steelblue', linestyle=':', linewidth=2.0)
    axes[0].set_ylim(-110, 76)
    axes[0].text(xpos, 55, label, color='steelblue', fontsize=16,
                 ha='center', va='bottom')

# === Linhas verticais — subplot (b) ATE (sem labels, até o fim do eixo Y) === #
for xpos in line_positions.values():
    y_min, y_max = 0, 150
    axes[1].plot([xpos, xpos], [y_min, y_max], color='steelblue', linestyle=':', linewidth=2.0)

# Grid and legends
axes[0].grid(True, linestyle='--', alpha=0.5)
axes[1].grid(True, linestyle='--', alpha=0.5)

axes[0].legend(loc='lower left', fontsize=10)
axes[1].legend(loc='upper left', fontsize=10)

# Tick label font sizes
axes[0].tick_params(axis='both', labelsize=16)
axes[1].tick_params(axis='both', labelsize=16)

plt.tight_layout()
plt.savefig(where_to_save+'Cross_Track_Along_Track_Errors_FINAL.png', dpi=300, bbox_inches='tight')