import math
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

from new_namelist_for_errors import *
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

# Importar as bibliotecas de rmse e mae

from new_namelist_for_errors import *
matplotlib.use("Agg")

'''
STATUS: 


LAST CHECKED: MARCH 19 2025
'''

window_size = 3

# Função para aplicar a média móvel
def apply_moving_average(data, window_size):
    # Usando pandas para calcular a média móvel
    return pd.Series(data).rolling(window=window_size, min_periods=1).mean().values



def processing_data(label, data_path):
    
    if label == 'ERA5':

        #abrindo os dados do era5 e deixando padronizados:
        dataset_dry = xr.open_dataset('/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/era5_dry.nc').rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'msl': 'mslp'})
        dataset_dry = (dataset_dry.assign_coords(lon=((dataset_dry.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')

        lat_data = dataset_dry.lat.sel(lat=slice(latN, latS))
        lon_data = dataset_dry.lon.sel(lon=slice(lonW,lonE))

        MSLP_data = dataset_dry.mslp.sel(lat=slice(latN, latS), lon=slice(lonW, lonE)) / 100 # to hPa

        # wind in ERA5:
        dataset_wind_path = '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/era5_wind100m.nc'
        
        dataset_wind = xr.open_dataset(dataset_wind_path).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon'})
        dataset_wind = (dataset_wind).assign_coords(lon=((dataset_wind.lon + 180) % 360) - 180).sortby('lon')
        
        sliced_dataset_wind = dataset_wind.sel(lat=slice(latN, latS), lon=slice(lonW, lonE))
        WSPD_data = calc_wind_gf_era5(sliced_dataset_wind)


    else: # agora os dados vindo do modelo:
        model_data = (xr.open_dataset(data_path).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'})).sel(time=time,lat=slice(latS,latN),lon=slice(lonW,lonE))

        lat_data = model_data.lat
        lon_data = model_data.lon
        MSLP_data = model_data.mslp/100
        WSPD_data = calc_wspd(model_data)
    
    return lat_data, lon_data, MSLP_data, WSPD_data

# Get the NOAA data in order to perform the search around it
NOAA = xr.open_dataset(NOAA_path)
time = NOAA.time.sel(time=slice(initial_day,final_day))
NOAA_hourly = NOAA.sel(time=time)
MSLP = NOAA_hourly.mslp
WSPD = NOAA_hourly.vmax * 1.852  # Passing from knots to km/h. This is already the maximum values!
lat = NOAA_hourly.lat
lon = NOAA_hourly.lon

## Just to get the NOAA lat lon
lat_points_NOAA, lon_points_NOAA = [], []
for t in range(0, len(time), 1): 

    lon_array_sel = lon.isel(time=t)
    lat_array_sel = lat.isel(time=t)
    
    lon_points_NOAA.append(lon_array_sel.values)
    lat_points_NOAA.append(lat_array_sel.values)

process_dataset = []
# First appending the NOAA info for further calculations
process_dataset.append((MSLP, WSPD, lat, lon, 'NOAA', 'green'))
for label, color, data_path in data_information:
    print(f'Processing {label} data ...')
    lat_data, lon_data, MSLP_data, WSPD_data = processing_data(label, data_path)
    process_dataset.append((MSLP_data, WSPD_data, lat_data, lon_data, label, color))

print('Pre-processing finished ...')

if label == 'CP-01':
    dlat, dlon = 10, 10
elif label == 'CP-02T2':
    dlat, dlon = 8, 8
elif label == 'CP-29':
    dlat, dlon = 4, 4
else:
    dlat, dlon = 2.8, 2.8

dataframes = {}
for dataset_MSLP, dataset_WSPD, lat_array, lon_array, label, color in process_dataset:

    lat_points, lon_points, mslp_points, time_steps, wspd_points = [], [], [], [], []

    for t in range(len(time)):
        MSLP_t = dataset_MSLP.isel(time=t)
        WSPD_t = dataset_WSPD.isel(time=t)

        if label == 'NOAA':
            lon_array_sel = lon_array.isel(time=t)
            lat_array_sel = lat_array.isel(time=t)
            
            lon_points.append(lon_array_sel.values)
            lat_points.append(lat_array_sel.values)

            mslp_points.append(MSLP_t.values)
            wspd_points.append(WSPD_t.values)
            time_steps.append(t)

            lat_points_NOAA = lat_points
            lon_points_NOAA = lon_points

        else:
            # Região para busca do mínimo (baseado no NOAA)
            upper_lat, lower_lat = lat_points_NOAA[t] + dlat, lat_points_NOAA[t] - dlat
            left_lon, right_lon = lon_points_NOAA[t] - dlon, lon_points_NOAA[t] + dlon

           
            lon_sliced = lon_array.sel(lon=slice(left_lon, right_lon))
            if label == 'ERA5':
                lat_sliced = lat_array.sel(lat=slice(upper_lat, lower_lat))
                MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(upper_lat,lower_lat))
            else:
                lat_sliced = lat_array.sel(lat=slice(lower_lat,upper_lat))
                MSLP_sliced = MSLP_t.sel(lon=slice(left_lon, right_lon), lat=slice(lower_lat,upper_lat))


            lat_t, lon_t = np.meshgrid(lat_sliced, lon_sliced, indexing='ij')
            
            # Verifica se há pontos válidos na região delimitada
            if MSLP_sliced.size > 0 and not np.isnan(MSLP_sliced).all():
                # Encontra o índice do valor mínimo dentro da região delimitada
                min_index = np.nanargmin(MSLP_sliced.values)  # Ignora NaN
                min_value = MSLP_sliced.values.ravel()[min_index]  # Valor mínimo

                # Converte o índice 1D para índices 2D (lat, lon)
                lat_index, lon_index = np.unravel_index(min_index, MSLP_sliced.values.shape)

                # Obtém as coordenadas (lat, lon) correspondentes ao valor mínimo
                lat_sel = lat_t[lat_index, lon_index]
                lon_sel = lon_t[lat_index, lon_index]

                # Adiciona os valores às listas
                mslp_points.append(min_value)
                lat_points.append(lat_sel)
                lon_points.append(lon_sel)
                time_steps.append(t)
                
                upper_lat_WIND = lat_sel + dlat
                lower_lat_WIND = lat_sel - dlat
                left_lon_WIND = lon_sel - dlon
                right_lon_WIND = lon_sel + dlon
                
                # Select WSPD within the new box
                if label != 'ERA5':
                    WSPD_sliced = WSPD_t.sel(lat=slice(lower_lat_WIND, upper_lat_WIND), lon=slice(left_lon_WIND, right_lon_WIND))
                elif label == 'ERA5':
                    WSPD_sliced = WSPD_t.sel(lat=slice(upper_lat_WIND,lower_lat_WIND), lon=slice(left_lon_WIND, right_lon_WIND))
                
                if WSPD_sliced.size > 0 and not np.isnan(WSPD_sliced).all():
                    # Find the maximum WSPD within the new box
                    max_wspd = np.nanmax(WSPD_sliced.values)
                    wspd_points.append(max_wspd)
                else:
                    # If no valid WSPD points, append NaN
                    print(f"No valid WSPD points found for {label} at timestep {t}. Skipping...")
                    wspd_points.append(np.nan)

            else:
                # Se não houver pontos válidos, pula para o próximo timestep
                print(f"No valid points found for {label} at timestep {t}. Skipping...")
                continue  # Pula para o próximo timestep
            
    # Criar DataFrame
    df = pd.DataFrame({
        'time step': time_steps,
        'mslp': mslp_points,
        'wspd': wspd_points,
        'lat': lat_points,
        'lon': lon_points
    })

    # Here I am saving the dataframes into one thing to further manipulate it and add errors
    dataframes[label] = df

datasets = [] # criado para fazer um loop depois nas trajetorias

# ============== Painel de séries temporais ============ #
# ============== Painel de séries temporais ============ #

# Definir a referência de tempo inicial
time_array = time.values  # Seu vetor de tempo
time_ref = time_array[0]  # Primeiro valor como referência

# Calcular o número de horas após a referência
hours_after = [(t - time_ref) / pd.Timedelta(hours=1) for t in time_array]

# Criar os rótulos formatados
time_labels = [f"{int(h)}" for h in hours_after]

# Criação da figura
fig, axs = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# Títulos
axs[0].set_title("(a) Central Pressure", fontsize=14)
axs[1].set_title("(b) Maximum Wind Speed", fontsize=14)

# Plotagem com suavização
for label, color, _ in data_information:
    if label in dataframes:
        df = dataframes[label]

        # Aplicar média móvel
        mslp_smoothed = apply_moving_average(df['mslp'], window_size)
        wspd_smoothed = apply_moving_average(df['wspd'], window_size)

        # Plotar curvas suavizadas
        if label == 'CP-OFF':
            linestyle = '--'
        elif label == 'CP-ON':
            linestyle = '-.'
        else:
            linestyle = '-'
        axs[0].plot(time_labels, mslp_smoothed, label=label, color=color, linestyle=linestyle)
        axs[1].plot(time_labels, wspd_smoothed, label=label, color=color, linestyle=linestyle)

if 'NOAA' in dataframes:
    df_noaa = dataframes['NOAA']

    mslp_noaa = apply_moving_average(df_noaa['mslp'], window_size)
    wspd_noaa = apply_moving_average(df_noaa['wspd'], window_size)

    axs[0].plot(time_labels, mslp_noaa, label='NOAA', color='darkgreen', linestyle='-')
    axs[1].plot(time_labels, wspd_noaa, label='NOAA', color='darkgreen', linestyle='-')

# Eixos e rótulos
axs[0].set_ylabel("Central Pressure (hPa)", fontsize=16)
axs[1].set_ylabel("Maximum Wind Speed (km/h)", fontsize=16)
axs[1].set_xlabel('Hours after 07-03T12', fontsize=16)

axs[1].tick_params(axis='x', labelsize=16)
axs[1].tick_params(axis='y', labelsize=16)
axs[0].tick_params(axis='y', labelsize=16)

# === Linhas Verticais E e F no gráfico (a) === #
line_positions = {'E': 8, 'F': 19}
for label, xpos in line_positions.items():
    axs[0].plot([xpos, xpos], [950, 1012], color='steelblue', linestyle=':', linewidth=2.0)
    # axs[0].text(xpos, 1013, label, color='steelblue', fontsize=16, ha='center', va='bottom')

# === Linhas Horizontais para a Escala de Saffir-Simpson no gráfico (b) === #
categories = [119, 154, 178, 209, 252]
category_labels = ['Cat 1', 'Cat 2', 'Cat 3', 'Cat 4', 'Cat 5']

for y_val, label in zip(categories, category_labels):
    axs[1].axhline(y=y_val, color='dimgray', linestyle='-', linewidth=1.5)
    axs[1].text(time_labels[-1], y_val, label, color='black', ha='left', va='bottom', fontsize=8)

# Legendas e grades
axs[0].legend(loc='best', fontsize=10)
axs[1].legend(loc='best', fontsize=10)
axs[0].grid(True, linestyle='--', alpha=0.5)
axs[1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("intensity_time_series_panel_FINAL.png", dpi=300)

# ====================== Painel de Erros =============== #

# Cálculo dos erros
mae_rmse_mslp = {}
mae_rmse_wspd = {}

ref_mslp = dataframes['NOAA']['mslp'].values
ref_wspd = dataframes['NOAA']['wspd'].values

for label, _, _ in data_information:
    if label in dataframes and len(dataframes[label]) == len(dataframes['NOAA']):
        pred_mslp = dataframes[label]['mslp'].values
        pred_wspd = dataframes[label]['wspd'].values

        mae_rmse_mslp[label] = {
            'mae': mean_absolute_error(ref_mslp, pred_mslp),
            'rmse': root_mean_squared_error(ref_mslp, pred_mslp)
        }
        mae_rmse_wspd[label] = {
            'mae': mean_absolute_error(ref_wspd, pred_wspd),
            'rmse': root_mean_squared_error(ref_wspd, pred_wspd)
        }

# Ordenando por MAE (MSLP e WSPD separadamente)
sorted_mslp = sorted(mae_rmse_mslp.items(), key=lambda x: x[1]['mae'])
labels_mslp = [item[0] for item in sorted_mslp]
maes_mslp = [item[1]['mae'] for item in sorted_mslp]
rmses_mslp = [item[1]['rmse'] for item in sorted_mslp]

sorted_wspd = sorted(mae_rmse_wspd.items(), key=lambda x: x[1]['mae'])
labels_wspd = [item[0] for item in sorted_wspd]
maes_wspd = [item[1]['mae'] for item in sorted_wspd]
rmses_wspd = [item[1]['rmse'] for item in sorted_wspd]

# Plot
height = 0.35
y1 = np.arange(len(labels_mslp))
y2 = np.arange(len(labels_wspd))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 10))

# ----- (a) MSLP -----
bars1 = ax1.barh(y1 - height / 2, maes_mslp, height, color='black', label='MAE')
bars2 = ax1.barh(y1 + height / 2, rmses_mslp, height, color='grey', hatch='//', edgecolor='dimgray', label='RMSE')

ax1.set_xlabel('Deviation from reference (hPa)', fontsize=16)
ax1.set_yticks(y1)
ax1.set_yticklabels(labels_mslp, fontsize=16)
ax1.invert_yaxis()
ax1.legend(fontsize=16)
ax1.grid(axis='x', linestyle='--', alpha=0.7)
ax1.set_title('(a) Central Pressure Error by Experiment', fontsize=16)
ax1.tick_params(axis='x', labelsize=16)
ax1.tick_params(axis='y', labelsize=16)
ax1.set_xlim(0, max(max(maes_mslp), max(rmses_mslp)) + 2)

# ----- (b) WSPD -----
bars3 = ax2.barh(y2 - height / 2, maes_wspd, height, color='black', label='MAE')
bars4 = ax2.barh(y2 + height / 2, rmses_wspd, height, color='grey', hatch='//', edgecolor='dimgray', label='RMSE')

ax2.set_xlabel('Deviation from reference (km/h)', fontsize=16)
ax2.set_yticks(y2)
ax2.set_yticklabels(labels_wspd, fontsize=16)
ax2.invert_yaxis()
ax2.legend(fontsize=16)
ax2.grid(axis='x', linestyle='--', alpha=0.7)
ax2.set_title('(b) Maximum Wind Speed Error by Experiment', fontsize=16)
ax2.tick_params(axis='x', labelsize=16)
ax2.tick_params(axis='y', labelsize=16)
ax2.set_xlim(0, max(max(maes_wspd), max(rmses_wspd)) + 2)

# Finalizar
plt.tight_layout()
plt.savefig("panel_mae_rmse_mslp_wspd_FINAL.png", dpi=300, bbox_inches='tight')


# ====================== Erro medio Monan ============== #
# Filtrar labels do MONAN
monan_labels = [label for label in mae_rmse_mslp if label.startswith('CP-')]

# Inicializar somatórios
mae_mslp_monan = np.mean([mae_rmse_mslp[label]['mae'] for label in monan_labels])
rmse_mslp_monan = np.mean([mae_rmse_mslp[label]['rmse'] for label in monan_labels])
mae_wspd_monan = np.mean([mae_rmse_wspd[label]['mae'] for label in monan_labels])
rmse_wspd_monan = np.mean([mae_rmse_wspd[label]['rmse'] for label in monan_labels])

# Erros ERA5
mae_mslp_era5 = mae_rmse_mslp['ERA5']['mae']
rmse_mslp_era5 = mae_rmse_mslp['ERA5']['rmse']
mae_wspd_era5 = mae_rmse_wspd['ERA5']['mae']
rmse_wspd_era5 = mae_rmse_wspd['ERA5']['rmse']

# Organização para o gráfico
mae_vals = [mae_mslp_monan, mae_wspd_monan]
rmse_vals = [rmse_mslp_monan, rmse_wspd_monan]
mae_era5 = [mae_mslp_era5, mae_wspd_era5]
rmse_era5 = [rmse_mslp_era5, rmse_wspd_era5]

# Organização para o gráfico
# Categorias no eixo y
categorias = ['Central \n Pressure', 'Maximum \n Wind Speed']
y = np.arange(len(categorias))  # posições
height = 0.2

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

# MONAN
ax.barh(y - height*1.5, mae_vals, height, label='MAE - MONAN', color='black')
ax.barh(y - height*0.5, rmse_vals, height, label='RMSE - MONAN', color='grey', hatch='//', edgecolor='dimgray')

# ERA5
ax.barh(y + height*0.5, mae_era5, height, label='MAE - ERA5', color='lightblue')
ax.barh(y + height*1.5, rmse_era5, height, label='RMSE - ERA5', color='deepskyblue', hatch='\\\\', edgecolor='dimgray')

# Estética
ax.set_yticks(y)
ax.set_yticklabels(categorias, fontsize=14)
ax.set_xlabel('Deviation from reference (km/h and hPa)', fontsize=14)
# ax.set_title('Average MAE and RMSE - MONAN vs ERA5', fontsize=16)
ax.grid(True, axis='x', linestyle='--', alpha=0.5)
ax.legend(fontsize=12, loc='best')
ax.tick_params(axis='x', labelsize=12)
ax.set_xlim(0, max(rmse_vals + rmse_era5) + 2)

# Salvar
plt.tight_layout()
plt.savefig("barplot_mean_error_monan_era5_intensity_FINAL.png", dpi=300, bbox_inches='tight')