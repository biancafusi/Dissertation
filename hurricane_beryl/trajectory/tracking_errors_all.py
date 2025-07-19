import math
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import string  # for subplot labels like (a), (b), etc.
import os
from new_namelist_for_errors import *
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from geopy.distance import geodesic
import matplotlib.ticker as ticker



matplotlib.use("Agg")

'''
STATUS: NEED A REVIEW: NOT PROPERLY GETTING THE TIME!


LAST CHECKED: MARCH 19 2025
'''
window_size = 3

# Função para aplicar a média móvel
def apply_moving_average(data, window_size):
    # Usando pandas para calcular a média móvel
    return pd.Series(data).rolling(window=window_size, min_periods=1).mean().values

# def haversine(coord1, coord2):
#     '''
#         Calculate distance using the Haversine Formula

#         coord1: lon,lat
#         coord2: lon,lat
#     '''
    
#     lon1, lat1 = coord1
#     lon2, lat2 = coord2

#     R = 6371000
#     phi_1 = math.radians(lat1)
#     phi_2 = math.radians(lat2)

#     delta_phi = math.radians(lat2 - lat1)
#     delta_lambda = math.radians(lon2 - lon1)

#     a = math.sin(delta_phi / 2.0)**2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0)**2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

#     meters = R * c
#     km = meters / 1000.0

#     return round(km, 3)

def track_error(coord_bt, coord_sim):
    '''
        Calcula o erro de trilha entre o centro do ciclone tropical (CT) 
        no best track (bt) e o simulado (sim), em quilômetros.

        As coordenadas devem ser fornecidas em graus:
        coord_bt: (lon, lat) do CT no best track
        coord_sim: (lon, lat) do CT simulado
    '''

    lambda_0, phi_0 = coord_bt
    lambda_s, phi_s = coord_sim

    # Converte para radianos apenas nas funções trigonométricas
    cos_inv_arg = (
        math.sin(math.radians(phi_0)) * math.sin(math.radians(phi_s)) +
        math.cos(math.radians(phi_0)) * math.cos(math.radians(phi_s)) *
        math.cos(math.radians(lambda_0 - lambda_s))
    )

    # Garante que o argumento do arccos esteja no intervalo [-1, 1]
    # cos_inv_arg = min(1.0, max(-1.0, cos_inv_arg))

    distance_km = 111.11 * math.degrees(math.acos(cos_inv_arg))  # resultado também em graus

    return round(distance_km, 3)

def calculating_errors_inside_df(df_reference, df_model, label, color):

    # Fazendo merge pelo time step
    df_merged = pd.merge(df_reference, df_model, on='time step', suffixes=('_NOAA', '_MODEL'))
    df_merged[['lat_NOAA', 'lon_NOAA', 'lat_MODEL', 'lon_MODEL']] = df_merged[['lat_NOAA', 'lon_NOAA', 'lat_MODEL', 'lon_MODEL']].astype(float)

    # Calcula o erro conforme a funcao que defini
    df_merged['erro'] = df_merged.apply(
        lambda row: track_error(  #MUDAR AQ DPS
            (row['lon_NOAA'], row['lat_NOAA']),
            (row['lon_MODEL'], row['lat_MODEL'])
        ),
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
        dataset_dry = xr.open_dataset('/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/era5_dry.nc').rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'msl': 'mslp'})
        dataset_dry = (dataset_dry.assign_coords(lon=((dataset_dry.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')

        lat_data = dataset_dry.lat.sel(lat=slice(latN,latS))
        lon_data = dataset_dry.lon.sel(lon=slice(lonW, lonE))
        MSLP_data = dataset_dry.mslp.sel(lat=slice(latN,latS), lon=slice(lonW, lonE)) / 100  # to hPa

        dataset_wind = xr.open_dataset(input_file_data).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon'})
        dataset_wind = (dataset_wind.assign_coords(lon=((dataset_wind.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')

    else:
        model_data = (xr.open_dataset(input_file_data).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'})).sel(time=time, lat=slice(latS, latN), lon=slice(lonW, lonE))
        lat_data = model_data.lat
        lon_data = model_data.lon
        MSLP_data = model_data.mslp / 100

    # Encontrar trilha do ciclone para esse dataset
    lat_points, lon_points, mslp_points, time_steps = [], [], [], []

    if label == 'CP-01':
        dlat, dlon = 10, 10
    elif label == 'CP-02T2':
        dlat, dlon = 8, 8
    elif label == 'CP-29':
        dlat, dlon = 4, 4
    else:
        dlat, dlon = 2.8, 2.8
    
    for t in range(len(time)):
        MSLP_t = MSLP_data.isel(time=t)
        # Região de busca
        upper_lat, lower_lat = lat_points_NOAA[t] + dlat, lat_points_NOAA[t] - dlat
        left_lon, right_lon = lon_points_NOAA[t] - dlon, lon_points_NOAA[t] + dlon
        
        # Seleciona região
        lon_sliced = lon_data.sel(lon=slice(left_lon, right_lon))
        if label == 'ERA5':
            lat_sliced = lat_data.sel(lat=slice(upper_lat,lower_lat))
            MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(upper_lat, lower_lat))

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

    # Salvar imediatamente
    # excel_name = saving_excel_folder+f'track_data_{label}.xlsx'
    # df.to_excel(excel_name, index=False)
    # print(f"Tabela salva com sucesso em {excel_name}!")

# ############################## CALCULATING ERRORS AND SAVING INTO ANOTHER TABLE ################
df_reference = dataframes['NOAA']

errors_dict = {}

for label in dataframes.keys():
    if label == 'NOAA':
        continue

    df_model = dataframes[label]
    color = next((d['color'] for d in datasets if d['label'] == label), 'black')  # Pega a cor do dataset

    time_step, erro, _ = calculating_errors_inside_df(df_reference, df_model, label, color)

    errors_dict[label] = {
        'time': time_step,
        'erro': erro,
        'color': color
    }

# # ################################### PLOTTING ERRORS BY GROUP ###################################

groups = {
    "Parameterization Effects": ['NOAA', 'CP-ON', 'CP-OFF', 'ERA5'],
    "Lifetime Effects": ['NOAA', 'CP-ON', 'CP-1H', 'CP-3H', 'CP-6H', 'ERA5'],
    "Mass-Flux Height Effects": ['NOAA', 'CP-ON', 'CP-D025', 'CP-D050', 'ERA5'],
    "Resolution Effects": ['NOAA', 'CP-ON', 'CP-15km', 'CP-60km', 'ERA5'],
    "Initial Condition Effects": ['NOAA', 'CP-ON', 'CP-GFS', 'CP-29', 'CP-01', 'CP-02T12', 'ERA5'],
    "Best Configuration": ['NOAA', 'CP-ON', 'CP-1HD050', 'CP-1HD05015km','CP-D050', 'CP-1H', 'ERA5']
}

# groups = {
#     "Parameterization Effects": ['NOAA', 'CP-ON', 'CP-OFF', 'CPSS-ON', 'ERA5'],
#     "Lifetime Effects": ['NOAA', 'CP-ON', 'CP-1H', 'CP-3H', 'ERA5'],
#     "Mass-Flux Height Effects": ['NOAA', 'CP-ON', 'CP-D025', 'CP-D050', 'ERA5'],
#     "Resolution Effects": ['NOAA', 'CP-ON', 'CP-15km', 'CP-60km', 'ERA5'],
#     "Initial Condition Effects": ['NOAA', 'CP-ON', 'CP-GFS', 'CP-29', 'CP-02T12', 'ERA5'],
#     "Best Configuration": ['NOAA', 'CP-ON', 'CP-1HD050', 'ERA5']
# }

panel_groups = [
    ("All Experiments", list(errors_dict.keys())),  # (a)
    ("Cold Pool Lifetime", groups["Lifetime Effects"]),  # (b)
    ("Initial Condition Day", groups["Initial Condition Effects"]),  # (c)
    ("Best Configuration Test", groups["Best Configuration"])  # (d)
]

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

# ==================================================PLOT 1 ========================================#
# ===================================== This creates a panel =====================================#
fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True, sharey=True)
axes = axes.flatten()

for idx, (group_name, dataset_labels) in enumerate(panel_groups):
    ax = axes[idx]

    for label in dataset_labels:
        if label in errors_dict:
            erro_suavizado = errors_dict[label]['erro']
            color = errors_dict[label]['color']

            linestyle = '--' if label == 'CP-OFF' else '-.' if label == 'CP-ON' else '-'

            ax.plot(
                time_labels, erro_suavizado,
                color=color, linestyle=linestyle, linewidth=2 if label in ['CP-OFF', 'CP-ON'] else 1.5,
                label=label
            )

    ax.set_title(f"({string.ascii_lowercase[idx]}) {group_name}", loc='left', fontsize=13)
    ax.grid(True)
    if idx in [2, 3]:  # bottom row
        ax.set_xlabel('Hours after 07-03T12', fontsize=11)
    if idx in [0, 2]:  # left column
        ax.set_ylabel('Error (km)', fontsize=11)

    ax.tick_params(axis='x', rotation=45)

    if idx == 0:
        ax.legend(fontsize=9, loc='upper left')

plt.tight_layout()
panel_path = os.path.join(where_to_save, 'panel_2x2_error_comparison.png')
plt.savefig(panel_path, dpi=300, bbox_inches='tight')
plt.close()

# # ===================================================PLOT 2=======================================#
# # Criar os gráficos
# for group_name, dataset_labels in groups.items():
#     plt.figure(figsize=(12, 6))

#     for label in dataset_labels:
#         if label in errors_dict:  # Verifica se o dataset existe nos erros calculados
#             erro_suavizado = errors_dict[label]['erro']  # Agora já está suavizado
#             color = errors_dict[label]['color']

#             plt.plot(
#                 time_labels, erro_suavizado,  # Plot usando o erro suavizado
#                 color=color, linestyle='-', linewidth=1.8, label=label
#             )

#     plt.xticks(ticks=range(len(time_labels)), labels=time_labels, rotation=45)
#     plt.xlabel('Hours after 07-03T12')
#     plt.ylabel('Error (km)')
#     plt.title(f'Errors - {group_name}', fontsize=14)
#     plt.grid()
#     plt.legend()
#     plt.tight_layout()

#     # Salvar cada gráfico
#     saving_name = f"errors_{group_name.replace(' ', '_')}.png"
#     plt.savefig(saving_name, dpi=300, bbox_inches='tight')
#     plt.close()  # Fecha a figura para evitar sobreposição

# # ======================================== PLOT 2 ===========================================

# # # #  Criar um único gráfico com todos os grupos 
plt.figure(figsize=(12, 6))

for label in errors_dict.keys():
    erro_suavizado = errors_dict[label]['erro']
    color = errors_dict[label]['color']

    # Destaque para CP-OFF e CP-ON com linestyle diferente
    if label == 'CP-OFF':
        linestyle = '--'  # por exemplo, tracejado
    elif label == 'CP-ON':
        linestyle = '-.'  # por exemplo, ponto-tracejado
    else:
        linestyle = '-'   # padrão

    plt.plot(
        time_labels, erro_suavizado,
        color=color, linestyle=linestyle, linewidth=2.2 if label in ['CP-OFF', 'CP-ON'] else 1.8,
        label=label
    )

plt.xticks(ticks=range(len(time_labels)), labels=time_labels, rotation=45)
plt.xlabel('Hours after 07-03T12')
plt.ylabel('Error (km)')
plt.grid()
plt.legend()
plt.tight_layout()

# Salvar o gráfico único
plt.savefig("errors_all_groups_filtered.png", dpi=300, bbox_inches='tight')
plt.close()

# ============================= PLOT 3 ====================================================== # #
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

ax.set_xticks(np.arange(0, max_val + 20, 20))
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)


plt.tight_layout()
plt.savefig("barplot_mae_rmse_horizontal_custom.png", dpi=300)


## ========================= PANEL PLOT 2+ 3 ========================== #
# # Definindo labels ordenados por MAE
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

ax1.set_xticks(ticks=range(len(time_labels)))
ax1.set_xticklabels(time_labels, rotation=45, fontsize=16)
ax1.set_xlabel('Hours after 07-03T12', fontsize=16)
ax1.set_ylabel('Error (km)', fontsize=16)
ax1.grid(True)
ax1.legend(fontsize=14)
ax1.tick_params(axis='x', labelsize=16)
ax1.tick_params(axis='y', labelsize=16)
ax1.set_title('(a) Distance error over time', fontsize=16)

# # ===================== (b) Plot 2 - MAE e RMSE =====================

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

# # ===================== Salvar o painel =====================
plt.tight_layout()
plt.savefig("panel_errors_mae_rmse_FINAL.png", dpi=300, bbox_inches='tight')