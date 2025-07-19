import xarray as xr
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import math
import matplotlib.pyplot as plt



from namelist_for_pathing_error import *

'''
Last update: march 17 2025

Este codigo calcula os pontos de pressao central do furacao
Beryl e as distancias entre o ponto de pressao central de acordo
com os dados da NOAA e de acordo com o Modelo/ERA5
'''

def haversine(coord1, coord2):
    '''
    Calculate distance using the Haversine Formula

    coord1: lon,lat
    coord2: lon,lat
    '''
    
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    R = 6371000
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c
    km = meters / 1000.0

    return round(km, 3)
# dado as coordenadas lat/lon da NOOA, como x1,y1 
# dado as coordenadas lat/lon do Modelo ou Era5, como x2,y2
# definir a distancia entre as coordenadas
# a distancia pode ser encontrada fazendo
# erro = distancia = sqrt((x1-x2)**2+(y1-y2)**2)

# coisas que preciso implementar:
# 1) pegar esses dados lat/lon, do jeito que ja esta implementado
# 2) criar um dataframe com esses dados
# 3) separar em um dataframe geral, um dataframe sobre o oceano e dataframe sobre o continente,
# para isso devo separar as regioes de acordo com os dados da noaa, por exemplo de tal em tal lat e lon, 
# se situa sobre o oceano
# 4) fazer o calculo dos erros utilizando as colunas do dataframe

# resolvendo 1)

NOAA = xr.open_dataset(NOAA_path)
time = NOAA.time.sel(time=slice(initial_day,final_day))
NOAA_hourly = NOAA.sel(time=time)
MSLP = NOAA_hourly.mslp
lat = NOAA_hourly.lat
lon = NOAA_hourly.lon

## Just to get the NOAA lat lon
lat_points_NOAA, lon_points_NOAA = [], []
for t in range(0, len(time), 1): 

    lon_array_sel = lon.isel(time=t)
    lat_array_sel = lat.isel(time=t)
    
    lon_points_NOAA.append(lon_array_sel.values)
    lat_points_NOAA.append(lat_array_sel.values)

# Separacao dos dados vindo do ERA5 e do Modelo
if label_data == 'ERA5':

    #abrindo os dados do era5 e deixando padronizados:
    dataset_dry = xr.open_dataset(name_file_dry).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'msl': 'mslp'})
    dataset_dry     = (dataset_dry.assign_coords(lon=((dataset_dry.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')

    lat_data = dataset_dry.lat.sel(lat=slice(latN, latS))
    lon_data = dataset_dry.lon.sel(lon=slice(lonW,lonE))

    MSLP_data = dataset_dry.mslp.sel(lat=slice(latN, latS), lon=slice(lonW, lonE)) / 100 # to hPa

else: # agora os dados vindo do modelo:
    model_data = (xr.open_dataset(name_file_prec).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'})).sel(time=time,lat=slice(latS,latN),lon=slice(lonW,lonE))

    lat_data = model_data.lat
    lon_data = model_data.lon
    MSLP_data = model_data.mslp/100

datasets = [
    (MSLP, lat, lon, 'o', 'NOAA', 'green'),
    (MSLP_data, lat_data, lon_data, 's', label_data, 'blue')
]

dlat, dlon = 2.8, 2.8

# resolvendo 2
dataframes = {}

for dataset_MSLP, lat_array, lon_array, marker, label, color in datasets:

    lat_points, lon_points, mslp_points, time_steps = [], [], [], []

    for t in range(len(time)):
        MSLP_t = dataset_MSLP.isel(time=t)

        if label == 'NOAA':
            lon_array_sel = lon_array.isel(time=t)
            lat_array_sel = lat_array.isel(time=t)
            
            lon_points.append(lon_array_sel.values)
            lat_points.append(lat_array_sel.values)

            mslp_points.append(MSLP_t.values)
            time_steps.append(t)

        else:
            # Região para busca do mínimo (baseado no NOAA)
            upper_lat, lower_lat = lat_points_NOAA[t] + dlat, lat_points_NOAA[t] - dlat
            left_lon, right_lon = lon_points_NOAA[t] - dlon, lon_points_NOAA[t] + dlon

           
            lon_sliced = lon_array.sel(lon=slice(left_lon, right_lon))
            if label_data == 'ERA5':
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
            else:
                # Se não houver pontos válidos, pula para o próximo timestep
                print(f"No valid points found for {label} at timestep {t}. Skipping...")
                continue  # Pula para o próximo timestep
            
    # Criar DataFrame
    df = pd.DataFrame({
        'time step': time_steps,
        'mslp': mslp_points,
        'lat': lat_points,
        'lon': lon_points
    })

    dataframes[label] = df


# --------------------- SALVAR EXCEL ------------------------

excel_name = f'track_data_{label_data}.xlsx'
with pd.ExcelWriter(excel_name) as writer:
    for label, df in dataframes.items():
        df.to_excel(writer, sheet_name=label, index=False)

print(f"Tabela salva com sucesso em {excel_name}!")

# Pegando os dois DataFrames já existentes
df_noaa = dataframes['NOAA']
df_model = dataframes[label_data]  # Pode ser ERA5 ou Modelo, conforme sua lógica anterior

# Fazendo merge pelo time step
df_merged = pd.merge(df_noaa, df_model, on='time step', suffixes=('_NOAA', '_MODEL'))
df_merged[['lat_NOAA', 'lon_NOAA', 'lat_MODEL', 'lon_MODEL']] = df_merged[['lat_NOAA', 'lon_NOAA', 'lat_MODEL', 'lon_MODEL']].astype(float)


df_merged['erro'] = df_merged.apply(
    lambda row: haversine(
        (row['lon_NOAA'], row['lat_NOAA']),
        (row['lon_MODEL'], row['lat_MODEL'])
    ),
    axis=1
)

# perguntar como implementar isso!
# def classificar_area(lat, lon):
#     # Exemplo fictício: 
#     # Latitudes e longitudes negativas => continente
#     # Latitudes e longitudes positivas => oceano
#     if lat < 0 and lon < 0:
#         return 'Continente'
#     else:
#         return 'Oceano'

# df_merged['area'] = df_merged.apply(lambda row: classificar_area(row['lat_NOAA'], row['lon_NOAA']), axis=1)
# print(df_merged[['time step', 'lat_NOAA', 'lon_NOAA', 'area']].head())

# df_oceano = df_merged[df_merged['area'] == 'Oceano']
# df_continente = df_merged[df_merged['area'] == 'Continente']

excel_name = f'track_data_{label_data}_with_error.xlsx'
with pd.ExcelWriter(excel_name) as writer:
    df_merged.to_excel(writer, sheet_name='Geral', index=False)
    # df_oceano.to_excel(writer, sheet_name='Oceano', index=False)
    # df_continente.to_excel(writer, sheet_name='Continente', index=False)

print(f"Tabelas com erro salvas com sucesso em {excel_name}!")

time_2 = pd.to_datetime(time.values)
time_label = time_2.strftime('%m/%dT%H')

plt.plot(
            time_label, df_merged['erro'],
            color=color, linestyle='-', linewidth=1.8, label=label,
        )
plt.xticks(np.arange(0,len(time_label),6))
plt.grid()
plt.title(f'Errors from {label_data} trajectories in km')
plt.savefig('test.png')