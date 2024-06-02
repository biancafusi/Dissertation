#!/usr/bin/python
# -*- coding: UTF-8 -*-


#################################
#PYTHON CODE TO PLOT DIFFERENS 
#MAPS PROJECTION USING THE 
#LIBRARY BASEMAP. 
#################################
#PYTHON CODE TO PLOT DIFFERENS 
# Data:13/04/22
#################################
# By: Jhonatan A. A Manco
# Modified by: Bianca Fusinato
#################################
import xarray as xr
import os
import numpy as np
import datetime as dt  
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import proplot as pplt
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib.ticker import FormatStrFormatter
####################################################

from   source.data_own import data_day
import source.functions as fnc
from source.cartopyTEST import cartopy_amazon

# to work without display
plt.switch_backend('agg')

output_path = '/mnt/beegfs/bianca.fusinato/dados_mestrado/python_plots/Dissertation/results/'

def plot_precipitation(idx, season_string, output_path):
    ds_CP = xr.open_dataset(f'~/dados/{season_string}CP_combined.nc')
    ds_OFF = xr.open_dataset(f'~/dados/{season_string}OFF_combined.nc')
    ds_ERA5 = xr.open_dataset(f'~/dados/{season_string}ERA5_combined.nc')
    ds_GPM = xr.open_dataset(f'~/dados/{season_string}GPM_combined.nc')

    data = ds_CP.time
    lats = ds_CP.lat
    lons = ds_CP.lon

    latERA5 = ds_ERA5.latitude
    lonERA5 = ds_ERA5.longitude

    latGPM = ds_GPM.lat[:]
    lonGPM = ds_GPM.lon[:]

    # Extraindo os dados para o índice fornecido
    precCP = ds_CP.totprec[idx, :, :]
    precOFF = ds_OFF.totprec[idx, :, :]
    
    precERA5 = ds_ERA5.tp[idx,:,:]*1000
    #precERA5 = prec*1000
    #precERA5 = precERA5.astype('float64')
    
    dsGPM = ds_GPM.transpose('time', 'lat', 'lon')
    precGPM = dsGPM.precip_media[idx, :, :]

    # Calculando e imprimindo os valores máximos
    a = precCP.max().item()
    b = precERA5.max().item()
    c = precOFF.max().item()
    d = precGPM.max().item()

    print(f'O máximo na estação {season_string} do CPON é: {a}')
    print(f'O máximo na estação {season_string} do ERA5 é: {b}')
    print(f'O máximo na estação {season_string} do CPOFF é: {c}')
    print(f'O máximo na estação {season_string} do GPM é: {d}')
    print('')

    # Definindo os limites e divisões conforme a estação
    if season_string == 'chuvosa':
        lim_max_CP = 24
        num_div_CP = 13
        lim_max_OFF = 20
        num_div_OFF = 11
        lim_max_ERA5 = 10
        num_div_ERA5 = 10
        lim_max_GPM = 24
        num_div_GPM = 13
    elif season_string == 'seca':
        lim_max_CP = 14
        num_div_CP = 8
        lim_max_OFF = 10
        num_div_OFF = 2
        lim_max_ERA5 =8
        num_div_ERA5 =1
        lim_max_GPM = 20
        num_div_GPM = 11
    elif season_string == 'transicao':
        lim_max_CP = 22
        num_div_CP = 12
        lim_max_OFF = 14
        num_div_OFF = 8
        lim_max_ERA5 = 9
        num_div_ERA5 = 1
        lim_max_GPM = 36
        num_div_GPM = 10

    # Gerando os plots
    cartopy_amazon(precCP, lats, lons, lim_min=0, lim_max=lim_max_CP, num_div=num_div_CP, plotname='ColdPool-ON', figname=f'tpCP_{season_string}', out=output_path, cbar=True)
    cartopy_amazon(precOFF, lats, lons, lim_min=0, lim_max= lim_max_OFF, num_div= num_div_OFF, plotname='ColdPool-OFF', figname=f'tpOFF_{season_string}', out=output_path, cbar=True)
    cartopy_amazon(precERA5, latERA5, lonERA5, lim_min=0, lim_max=lim_max_ERA5, num_div=num_div_CP, plotname='ERA', figname=f'tpERA5_{season_string}', out=output_path, cbar=True)
    cartopy_amazon(precGPM, latGPM, lonGPM, lim_min=0, lim_max= 18, num_div= 10, plotname='GPM-IMERG', figname='tpGPM_seca', out=output_path, cbar=True)

# Estacao chuvosa:
idx_chuvosa = 45
season_wet = 'chuvosa'
plot_precipitation(idx_chuvosa, season_wet, output_path)

# Estacao seca:
idx_seca = 139
season_dry = 'seca'
plot_precipitation(idx_seca, season_dry, output_path)

# Estacao transicao:
idx_transicao = 217
season_transition = 'transicao'
plot_precipitation(idx_transicao, season_transition, output_path)

