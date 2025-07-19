#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xarray as xr
import pandas as pd
import numpy as np

from namelist import *
from base_plot import *
'''
STATUS: WORKING

LAST UPDATED: MARCH 26 2025
'''

def calc_wspd(dataset):
    mag_wind = dataset.wspd
    return mag_wind*3.6

plot_type = 'OTHER'
            #'ONLY_RAIN'

# =========================== GETTING THE RAIN DATA ================================= #
# === VARIABLES ==== #
# Rain

# datasets = []

# for label, data_path in data_information_rain:

#     print(f'Processing {label}...')

#     if label == 'GPM':
#         dataset_prec = xr.open_dataset(data_path)

#         lats = dataset_prec.latitude.sel(latitude=slice(latS,latN))
#         lons = dataset_prec.longitude.sel(longitude=slice(lonW,lonE))

#         precipitation_hourly = dataset_prec.precipitation.sel(
#                 time=slice(initial_day, final_day), 
#                 latitude=slice(latS, latN), 
#                 longitude=slice(lonW, lonE)
#             ).transpose('time', 'latitude', 'longitude')      

#         time = dataset_prec.time.sel(time=slice(initial_day, final_day)).values

#     else:
#         dataset_prec = xr.open_dataset(data_path)

#         lats = dataset_prec.latitude.sel(latitude=slice(latS,latN))
#         lons = dataset_prec.longitude.sel(longitude=slice(lonW,lonE))

#         slice_prec_rainnc = dataset_prec.rainnc.sel(Time=slice(initial_day,final_day), latitude=slice(latS,latN), longitude=slice(lonW, lonE))
#         slice_prec_rainc = dataset_prec.rainc.sel(Time=slice(initial_day,final_day), latitude=slice(latS,latN), longitude=slice(lonW, lonE))

#         precipitation_hourly = slice_prec_rainnc + slice_prec_rainc
#         time = precipitation_hourly.Time

#     datasets.append({
#         'label': label,
#         'precipitation': precipitation_hourly,
#         'lat': lats,
#         'lon': lons,
#         'time': time

#     })
# print('Process finished!')

# # Encontrar os datasets corretos dentro da lista
# cp_on = next(item for item in datasets if item["label"] == "CP-ON")
# cp_off = next(item for item in datasets if item["label"] == "CP-OFF")
# cp_cpss = next(item for item in datasets if item["label"] == "CPSS-ON")

# # Calcular a diferença de precipitação
# diff_rain_CPON = cp_on['precipitation'] - cp_off['precipitation']
# diff_rain_CPSS = cp_cpss['precipitation'] - cp_on['precipitation']

# # Pegar as coordenadas e tempo
# lats = cp_on['lat']
# lons = cp_on['lon']
# time = cp_on['time']

# print('Processing diff....')
# # Adicionar ao datasets
# datasets.append({
#     'label': 'DIFF_CP-ON',
#     'precipitation': diff_rain_CPON,
#     'lat': lats,
#     'lon': lons,
#     'time': time
# })

# datasets.append({
#     'label': 'DIFF_CPSS-ON',
#     'precipitation': diff_rain_CPSS,
#     'lat': lats,
#     'lon': lons,
#     'time': time
# })

# # =================== PLOTTING SINGLE - PANEL 01 ========================================== #

# if plot_type == 'ONLY_RAIN':
#     for dataset in datasets:
#         label = dataset['label']
#         print(f'Plotting {label} ...')  

#         # Pular o CPSS-ON
#         if label == 'CPSS-ON':
#             continue

#         # Definir o caminho correto de saída baseado no label
#         out_path = saving_paths_dict.get(label, None)

#         for t in range(len(dataset['time'])):
#             beryl_prec(dataset['precipitation'][t, :, :], dataset['lat'], dataset['lon'],
#                     0.25, 25, 15, 
#                     title=label+' - '+np.datetime_as_string(time[t],unit='h'),
#                     figname=f'rain{str(t).zfill(3)}',
#                     out=out_path)

# else:
#     # =========== SNAPSHOT ========= #
#     diff_cp_cpss = next(item for item in datasets if item["label"] == 'DIFF_CP-ON')
#     cb_thicks = np.linspace(-10, 10, 5)
#     diff_plot(diff_cp_cpss['precipitation'][43, :, :], diff_cp_cpss['lat'], diff_cp_cpss['lon'],
#             -10, 10, cb_thicks, 
#             title='Diff Sea Spray'+' - '+np.datetime_as_string(time[43],unit='h'),
#             figname=f'rain{str(43).zfill(3)}',
#             out='/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_04/DIFF_RAIN/',
#             unit='mm/h')
# fazer os paineis dos dias 2024-07-04T20 até 2024-07-06T09
# animar

    # plotar cada label do dataframe em um único loop de tempo
    # fazer os painéis animados 1 e 2
    # fazer o cálculo da diferença de chuva
    # inserir uma função que plote essa diferença de chuva (paineis 3 e 4)



# =========================== GETTING THE RAIN DATA ================================= #
# === VARIABLES ==== #
# Wspd, sensible heat, latent heat

datasets_dry = []

for label, data_path in data_information_dry:

    print(f'Processing {label}...')

    dataset_dry = (xr.open_dataset(data_path)).sel(Time=slice(initial_day,final_day), latitude=slice(latS,latN), longitude=slice(lonW, lonE))

    lats = dataset_dry.latitude
    lons = dataset_dry.longitude
    time = dataset_dry.Time

    wspd = calc_wspd(dataset_dry)

    slice_latent_heat = dataset_dry.lh
    slice_sensible_heat = dataset_dry.hfx

    total_heat_flux = slice_latent_heat + slice_sensible_heat
    
    datasets_dry.append({
        'label': label,
        'wspd': wspd,
        'heat': total_heat_flux,
        'lat': lats,
        'lon': lons,
        'time': time

    })

print('Process finished!')

# ============================ PAINEL 03 e 04 ================================= #

# =========== SNAPSHOT ========= #
for dataset in datasets_dry:
    label = dataset['label']
    print(f'Plotting {label} ...')

    if label != 'CPSS-ON':
        if label == 'CP-OFF':
            out = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_03/CP-OFF_HEAT/'
        else:
            out = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_04/CP-ON_HEAT/'

        # Plota os gráficos
        beryl_heat_plot(
            dataset['heat'][43, :, :],
            dataset['lat'],
            dataset['lon'],
            -10, 10, 1, 
            title = f'{label} - {np.datetime_as_string(dataset["time"][43], unit="h")}',
            figname=f'rain{str(43).zfill(3)}',
            out=out,
            unit=r'$\mathregular{(W/m^2)}$',
        )
print('Plotting finished!')

# # calcular a diferença cpon e cpsson

# # Encontrar os datasets corretos dentro da lista
# cp_on = next(item for item in datasets_dry if item["label"] == "CP-ON")
# cp_off = next(item for item in datasets_dry if item["label"] == "CP-OFF")
# cpss_on = next(item for item in datasets_dry if item["label"] == "CPSS-ON")

# # Calcular a diferença de precipitação
# diff_heat_CPON = cp_on['heat'] - cp_off['heat']
# diff_heat_CPSS = cpss_on['heat'] - cp_on['heat']

# # Pegar as coordenadas e tempo
# lats = cp_on['lat']
# lons = cp_on['lon']
# time = cp_on['time']

# print('Processing diff....')
# # Adicionar ao datasets
# datasets_dry.append({
#     'label': 'DIFF_CP-ON',
#     'heat': diff_heat_CPON,
#     'wspd': None,
#     'lat': lats,
#     'lon': lons,
#     'time': time
# })

# datasets_dry.append({
#     'label': 'DIFF_CPSS-ON',
#     'heat': diff_heat_CPSS,
#     'wspd': None,
#     'lat': lats,
#     'lon': lons,
#     'time': time
# })

# # =========== SNAPSHOT ========= #
# diff_cp_on = next(item for item in datasets_dry if item["label"] == 'DIFF_CP-ON')
# diff_cpss = next(item for item in datasets_dry if item["label"] == 'DIFF_CPSS-ON')

# plotting = [diff_cp_on, diff_cpss]

# for file in plotting:
#     cb_thicks = np.linspace(-200, 350, 50)

#     if file == diff_cp_on:
#         title = 'Diff Cold Pool'+' - '+np.datetime_as_string(time[43],unit='h')+' ' +r'$\mathregular{(W/m^2)}$'
#         out = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_03/DIFF_HEAT/'
    
#     elif file == diff_cpss:
#         title = 'Diff Sea Spray'+' - '+np.datetime_as_string(time[43],unit='h')+' ' +r' $\mathregular{(W/m^2)}$'
#         out = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_04/DIFF_HEAT/'

#         print('oi')

#     diff_plot(file['heat'][43, :, :], file['lat'], file['lon'],
#             -200, 350, cb_thicks, 
#             title=title,
#             figname=f'rain{str(43).zfill(3)}',
#             out=out, unit=r'$\mathregular{(W/m^2)}$')

# # =========== SNAPSHOT ========= #
# for dataset in datasets_dry:
#     label = dataset['label']
#     print(f'Plotting {label} ...')

#     if label != 'CPSS-ON':
#         if label == 'CP-OFF':
#             out = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_03/CP-OFF_WSPD/'
#         else:
#             out = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_04/CP-ON_WSPD/'

#         # Plota os gráficos
#         beryl_prec(
#             dataset['wspd'][43, :, :],
#             dataset['lat'],
#             dataset['lon'],
#             0.25, 250, 20, 
#             title=f'{label} - {np.datetime_as_string(dataset["time"][43], unit="h")}',
#             figname=f'rain{str(43).zfill(3)}',
#             out=out,
#             unit='km/h'
#         )
# print('Plotting finished!')

# # calcular a diferença cpon e cpsson

# # Encontrar os datasets corretos dentro da lista
# cp_on = next(item for item in datasets_dry if item["label"] == "CP-ON")
# cp_off = next(item for item in datasets_dry if item["label"] == "CP-OFF")
# cpss_on = next(item for item in datasets_dry if item["label"] == "CPSS-ON")

# # Calcular a diferença de precipitação
# diff_wspd_CPON = cp_on['wspd'] - cp_off['wspd']
# diff_wspd_CPSS = cpss_on['wspd'] - cp_on['wspd']

# # Pegar as coordenadas e tempo
# lats = cp_on['lat']
# lons = cp_on['lon']
# time = cp_on['time']

# print('Processing diff....')
# # Adicionar ao datasets
# datasets_dry.append({
#     'label': 'DIFF_CP-ON',
#     'heat': None,
#     'wspd': diff_wspd_CPON,
#     'lat': lats,
#     'lon': lons,
#     'time': time
# })

# datasets_dry.append({
#     'label': 'DIFF_CPSS-ON',
#     'heat': None,
#     'wspd': diff_wspd_CPSS,
#     'lat': lats,
#     'lon': lons,
#     'time': time
# })

# # =========== SNAPSHOT ========= #
# diff_cp_on = next(item for item in datasets_dry if item["label"] == 'DIFF_CP-ON')
# diff_cpss = next(item for item in datasets_dry if item["label"] == 'DIFF_CPSS-ON')

# plotting = [diff_cp_on, diff_cpss]

# for file in plotting:
#     cb_thicks = np.linspace(-100, 100, 20)

#     if file == diff_cp_on:
#         title = 'Diff Cold Pool'+' - '+np.datetime_as_string(time[43],unit='h')+' ' +'km/h'
#         out = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_03/DIFF_WSPD/'
    
#     elif file == diff_cpss:
#         title = 'Diff Sea Spray'+' - '+np.datetime_as_string(time[43],unit='h')+' ' +'km/h'
#         out = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_04/DIFF_WSPD/'

#     diff_plot(file['wspd'][43, :, :], file['lat'], file['lon'],
#             -100, 100, cb_thicks, 
#             title=title,
#             figname=f'rain{str(43).zfill(3)}',
#             out=out, unit='km/h')


    


















# from namelist_fields_monan import *

# from plotter_variables import *
# from panel_1x3 import simple_panels
# from panel_4x4 import panel4x4


# plt.switch_backend('agg')  # Evita abrir janelas de gráficos

# if type_plot == 'RAIN':

#     RAIN_Plotter(ERA5_data, initial_day, final_day, where_to_save + 'ERA5/rain/')
#     RAIN_Plotter(GPM_data, initial_day, final_day, where_to_save + 'GPM/rain/')
#     RAIN_Plotter(CONTROL_rain, initial_day, final_day, where_to_save + 'berylERACN00/rain/',title_prefix='CONTROL')
#     RAIN_Plotter(EXPERIMENT_rain, initial_day, final_day,  where_to_save + 'berylERACN11/rain/',title_prefix='CP-ON')
    
#     panel4x4(131)

# elif type_plot == 'ACCUMULATED_PRECIP':
#     ACCUMULATED_PRECIP(ERA5_data, initial_day, final_day, where_to_save + 'ERA5/accumulated/')

# elif type_plot == 'MSLP':
#     MSLP_Plotter(ERA5_data, initial_day, final_day,  where_to_save + 'ERA5/mslp/')
#     MSLP_Plotter(CONTROL, initial_day, final_day,  where_to_save + 'berylERACN00/mslp/',title_prefix='CONTROL')
#     MSLP_Plotter(EXPERIMENT, initial_day, final_day,  where_to_save + 'berylERACN11/mslp/',title_prefix='CP-ON')

#     # simple_panels('MSLP', 131)

# elif type_plot == 'WIND':
#     WIND_Plotter(ERA5_data, initial_day, final_day,  where_to_save + 'ERA5/wind/')
#     WIND_Plotter(CONTROL, initial_day, final_day,  where_to_save + 'berylERACN00/wind/',title_prefix='CONTROL')
#     WIND_Plotter(EXPERIMENT, initial_day, final_day,  where_to_save + 'berylERACN11/wind/',title_prefix='CP-ON')
#     WIND_Plotter(EXPERIMENT, initial_day, final_day,  where_to_save + 'berylERACN11/wind_gf/',title_prefix='CP-ON',gust_front_on=True)

#     simple_panels('Wind', 131,gust_front_on=False)
#     simple_panels('Wind', 131, gust_front_on=True)
    
