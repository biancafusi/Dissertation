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

def plot_precipitation_mean(season_string, output_path):
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

    dsGPM = ds_GPM.transpose('time', 'lat', 'lon')

    # Calculando a media nos dias:
    CP_acum = ds_CP['totprec'].sum(dim='time')
    CP_media = CP_acum / 10
    
    OFF_acum = ds_OFF['totprec'].sum(dim='time')
    OFF_media = OFF_acum / 10    
    
    ERA5_acum = (ds_ERA5['tp']*1000).sum(dim='time')
    ERA5_media = ERA5_acum / 10

    GPM_acum = dsGPM['precip_media'].sum(dim='time')
    GPM_media = GPM_acum / 10

    # Definindo os limites e divisões conforme a estação
    if season_string == 'chuvosa':
        lim_max_CP = 45
        num_div_CP = 10
        lim_max_OFF = 40
        num_div_OFF = 11
        lim_max_ERA5 = 40
        num_div_ERA5 = 11
        lim_max_GPM = 45
        num_div_GPM = 10
    elif season_string == 'seca':
        lim_max_CP = 40
        num_div_CP = 11
        lim_max_OFF = 40
        num_div_OFF = 11
        lim_max_ERA5 = 40
        num_div_ERA5 = 11
        lim_max_GPM = 40
        num_div_GPM = 11
    elif season_string == 'transicao':
        lim_max_CP = 40
        num_div_CP = 11
        lim_max_OFF = 40
        num_div_OFF = 11
        lim_max_ERA5 = 60
        num_div_ERA5 = 7
        lim_max_GPM = 40
        num_div_GPM = 11

    # Gerando os plots
    cartopy_amazon(CP_media, lats, lons, lim_min=0, lim_max=lim_max_CP, num_div=num_div_CP, plotname='ColdPool-ON', figname=f'mediaCP_{season_string}', out=output_path, cbar=True, unit='mm/day')
    cartopy_amazon(OFF_media, lats, lons, lim_min=0, lim_max= lim_max_OFF, num_div= num_div_OFF, plotname='ColdPool-OFF', figname=f'mediaOFF_{season_string}', out=output_path, cbar=True, unit='mm/day')
    cartopy_amazon(ERA5_media, latERA5, lonERA5, lim_min=0, lim_max=lim_max_ERA5, num_div=num_div_CP, plotname='ERA', figname=f'mediaERA5_{season_string}', out=output_path, cbar=True, unit='mm/day')
    cartopy_amazon(GPM_media, latGPM, lonGPM, lim_min=0, lim_max=lim_max_GPM, num_div= num_div_GPM, plotname='GPM-IMERG', figname=f'mediaGPM_{season_string}', out=output_path, cbar=True, unit='mm/day')

# Estacao chuvosa:
season_wet = 'chuvosa'
plot_precipitation_mean(season_wet, output_path)
print('carregou chuvosa')

# Estacao seca:
season_dry = 'seca'
plot_precipitation_mean(season_dry, output_path)
print('carregou seca')

# Estacao transicao:
season_transition = 'transicao'
plot_precipitation_mean(season_transition, output_path)
print('carregou transicao')
