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

####################################################

from   source.data_own import data_day
import source.functions as fnc
from source.cartopyTEST import cartopy_amazon

# to work without display
plt.switch_backend('agg')

output_path = '/mnt/beegfs/bianca.fusinato/dados_mestrado/python_plots/Dissertation/results/'

# Estacao chuvosa

ds_chuvosaCP = xr.open_dataset('~/dados/chuvosaCP_combined.nc')
ds_chuvosaOFF = xr.open_dataset('~/dados/chuvosaOFF_combined.nc')
ds_chuvosaERA5 = xr.open_dataset('~/dados/chuvosaERA5_combined.nc')
ds_chuvosaGPM = xr.open_dataset('~/dados/chuvosaGPM_combined.nc')

data = ds_chuvosaCP.time
lats = ds_chuvosaCP.lat
lons = ds_chuvosaCP.lon

latERA5 = ds_chuvosaERA5.latitude
lonERA5 = ds_chuvosaERA5.longitude

latGPM = ds_chuvosaGPM.lat
lonGPM = ds_chuvosaGPM.lon

idx_chuvosa = 35

precCP = ds_chuvosaCP.totprec[idx_chuvosa,:,:]
#print(precCP.time.values)
precOFF = ds_chuvosaOFF.totprec[idx_chuvosa,:,:]
#print(precOFF.time.values)
precERA5 = ds_chuvosaERA5.tp[idx_chuvosa,:,:]
precGPM = ds_chuvosaGPM.precip_media[idx_chuvosa,:,:]

cartopy_amazon(precCP, lats, lons, lim_min=0, lim_max=20, num_div=11, plotname='ColdPool-ON', figname='tpCP_chuvosa', out= output_path, cbar=True)
cartopy_amazon(precOFF, lats, lons, lim_min=0, lim_max=20, num_div=11, plotname='ColdPool-OFF', figname='tpOFF_chuvosa', out= output_path, cbar=True)
#cartopy_amazon(precERA5, latERA5, lonERA5, figname='tpERA5_chuvosa', out= output_path, cbar=True)
#cartopy_amazon(precGPM, latGPM, lonGPM, figname='tpGPM_chuvosa', out= output_path, cbar=True)



