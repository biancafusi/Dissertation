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

#from   Parameters_jhona import ds_chuvosaCP, media_chuvosa  

# own function to transform the data in data_time 
from   source.data_own import data_day

import source.functions as fnc

# Function with the definition of differents projetions
from source.cartopyTEST import cartopy_amazon

# to work without display
plt.switch_backend('agg')

####from   source.nc_make  import  savetonc



'''

datas = ds_chuvosaCP.time
lats  = ds_chuvosaCP.lat
lons  = ds_chuvosaCP.lon

#tota =b1.totprec[35,:,:]
#conv =b1.convprec[35,:,:]

#datas2=b2.time
#lats2=b2.latitude
#lons2=b2.longitude

precipitacao_minima = round(media_chuvosa.min().item(), 1);
precipitacao_maxima = round(media_chuvosa.max().item(), 1);


#precERA5 = b2.tp[35,:,:]
#convERA5 = b2.cp[35,:,:]

#temp = b1.t2mj[24:49,:,:]
#resultados1 = []

#for i in range(24,49):
#    soma = temp[i,:,:].sum

#exit()

#cartopy_amazon(mean_totprec,lats,lons,nn=12,plotname='Temperature',figname='temp_secamediaCP00',color='RdBu_r',out=out_fig,cbar=True)

#TOTAL PRECIPITATION
cartopy_amazon(media_chuvosa,lats,lons,nn=5,plotname='Total Precipitation - BRAMS',figname='teste',color='Blues',out=out_fig,cbar=True)

#CONVECTIVE PRECIPITATION
#cartopy_amazon(conv,lats,lons,b1=0,b2=9,nn=30,plotname='Convective Precipitation - BRAMS',figname='conv_secaCP00',color='Blues',out=out_fig,cbar=True)

#TOTAL PRECIPITATION
#cartopy_amazon(precERA5,lats2,lons2,b1=0,b2=9,nn=30,plotname='Total Precipitation - ERA5',figname='total_ERA5',color='Blues',out=out_fig,cbar=True)

#CONVECTIVE PRECIPITATION
#cartopy_amazon(convERA5,lats2,lons2,b1=0,b2=9,nn=30,plotname='Convective Precipitation - ERA5',figname='conv_ERA',color='Blues',out=out_fig,cbar=True)




#cartopy_f(t,lats,lons,color='RdBu_r',out='',cbar=True)
#plt.show()

'''

'''
#TESTE COM UM DADO
ds = xr.open_dataset('~/dados/chuvosaCP_combined.nc')
output_dir = os.path.expanduser('~/dados/')

datas = ds.time
lats = ds.lat
lon = ds.lon

tota = ds.totprec[3,:,:]
precipitacao_minima = round(tota.min().item(), 1);
precipitacao_maxima = round(tota.max().item(), 1);

cartopy_amazon(tota, lats, lon, nn=12, plotname='Teste', figname='teste', color='Blues', out=output_dir, cbar=True)
'''
2014-02-15
2014-02-24
#Teste com mean
# Função para calcular a média da precipitação
#def calcular_media_precipitacao(ds, var_name):
#    return ds[var_name].mean(dim='time')

# Caminhos dos arquivos de dados
ds_chuvosaCP_path = os.path.expanduser('~/dados/chuvosaCP_combined.nc')
#ds_secaCP_path = os.path.expanduser('~/dados/secaCP_combined.nc')
#ds_transicaoCP_path = os.path.expanduser('~/dados/transicaoCP_combined.nc')
ds_chuvosaERA5_path = os.path.expanduser('~/dados/chuvosaERA5_combined.nc')

# Abrir os datasets
ds_chuvosaCP = xr.open_dataset(ds_chuvosaCP_path)
#ds_secaCP = xr.open_dataset(ds_secaCP_path)
#ds_transicaoCP = xr.open_dataset(ds_transicaoCP_path)
ds_chuvosaERA5 = xr.open_dataset(ds_chuvosaERA5_path)

totaCP = ds_chuvosaCP.totprec[144,:,:]
totaERA5 = ds_chuvosaERA5.tp[144+24,:,:]*1000

print(f'A hora CP eh: {totaCP.time.values}')
print(f'A hora ERA5 eh: {totaERA5.time.values}')

lats = ds_chuvosaCP.lat
lon = ds_chuvosaCP.lon

latsERA5 = ds_chuvosaERA5.latitude
lonERA5 = ds_chuvosaERA5.longitude

output_dir = os.path.expanduser('~/dados/')
'''
#VERIFICAR SE TA CERTO A LONGITUDE
lats = ds_chuvosaCP.lat
lon = ds_chuvosaCP.lon

latsERA5 = ds_chuvosaERA5.latitude
lonERA5 = ds_chuvosaERA5.longitude

#Accessing the lat data through specific lat
latss = lats.sel(lat=-3, method="nearest").values
lons = lon.sel(lon=-60, method="nearest").values
print(latss)
print(lons)

# Initialize Basemap
map = Basemap(projection='cyl', resolution='l', 
              llcrnrlat=-10, urcrnrlat=10, 
              llcrnrlon=-70, urcrnrlon=-50)

# Transform the specific lat/lon to map coordinates
# Draw parallels and meridians with labels
parallels = np.arange(-10., 10., 5.)
meridians = np.arange(-70., 50., 5.)
map.drawparallels(parallels, labels=[1,0,0,0])
map.drawmeridians(meridians, labels=[0,0,0,1])

x, y = map(lons, latss)

# Plot the specific point
map.plot(x, y, 'bo', markersize=10)

plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.savefig('specific_point_map2.pdf', dpi=300, bbox_inches='tight')

exit()
'''
#print(f'CPlat:{lats}')
#print(f'ERA5lat:{latsERA5}')
#exit()
# Calcular a média das precipitações para cada período
#media_totprec_chuvosaCP = calcular_media_precipitacao(ds_chuvosaCP, 'totprec')
#media_convprec_chuvosaCP = calcular_media_precipitacao(ds_chuvosaCP, 'convprec')

#media_totprec_secaCP = calcular_media_precipitacao(ds_secaCP, 'totprec')
#media_convprec_secaCP = calcular_media_precipitacao(ds_secaCP, 'convprec')

#media_totprec_transicaoCP = calcular_media_precipitacao(ds_transicaoCP, 'totprec')
#media_convprec_transicaoCP = calcular_media_precipitacao(ds_transicaoCP, 'convprec')

cartopy_amazon(totaCP, lats, lon, nn=2, plotname='Teste', figname='totprec_chuvosaCP', color='Blues', out=output_dir, cbar=True)
cartopy_amazon(totaERA5, latsERA5, lonERA5, nn=2, plotname='Teste', figname='totprec_chuvosaERA5', color='Blues', out=output_dir, cbar=True)

exit()

cartopy_amazon(tota, lats, lon, nn=12, plotname='Teste', figname='teste', color='Blues', out=output_dir, cbar=True)
cartopy_amazon(tota, lats, lon, nn=12, plotname='Teste', figname='teste', color='Blues', out=output_dir, cbar=True)

cartopy_amazon(tota, lats, lon, nn=12, plotname='Teste', figname='teste', color='Blues', out=output_dir, cbar=True)
cartopy_amazon(tota, lats, lon, nn=12, plotname='Teste', figname='teste', color='Blues', out=output_dir, cbar=True)





