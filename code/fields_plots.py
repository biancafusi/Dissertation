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

import numpy as np

import datetime as dt  

import matplotlib.pyplot as plt

####################################################

from   Parameters import b1, b2, out_fig 

# own function to transform the data in data_time 
from   source.data_own import data_day

import source.functions as fnc

# Function with the definition of differents projetions
from source.cartopyTEST import cartopy_amazon

# to work without display
plt.switch_backend('agg')

####from   source.nc_make  import  savetonc

datas=b1.time
lats =b1.lat
lons =b1.lon

tota =b1.totprec[35,:,:]
conv =b1.convprec[35,:,:]

datas2=b2.time
lats2=b2.latitude
lons2=b2.longitude

precipitacao_minima = round(tota.min().item(), 1);
precipitacao_maxima = round(tota.max().item(), 1);


precERA5 = b2.tp[35,:,:]
convERA5 = b2.cp[35,:,:]

#temp = b1.t2mj[24:49,:,:]
#resultados1 = []

#for i in range(24,49):
#    soma = temp[i,:,:].sum

#exit()

#cartopy_amazon(mean_totprec,lats,lons,nn=12,plotname='Temperature',figname='temp_secamediaCP00',color='RdBu_r',out=out_fig,cbar=True)

#TOTAL PRECIPITATION
cartopy_amazon(tota,lats,lons,nn=5,plotname='Total Precipitation - BRAMS',figname='total_secaCP00',color='Blues',out=out_fig,cbar=True)

#CONVECTIVE PRECIPITATION
#cartopy_amazon(conv,lats,lons,b1=0,b2=9,nn=30,plotname='Convective Precipitation - BRAMS',figname='conv_secaCP00',color='Blues',out=out_fig,cbar=True)

#TOTAL PRECIPITATION
#cartopy_amazon(precERA5,lats2,lons2,b1=0,b2=9,nn=30,plotname='Total Precipitation - ERA5',figname='total_ERA5',color='Blues',out=out_fig,cbar=True)

#CONVECTIVE PRECIPITATION
#cartopy_amazon(convERA5,lats2,lons2,b1=0,b2=9,nn=30,plotname='Convective Precipitation - ERA5',figname='conv_ERA',color='Blues',out=out_fig,cbar=True)




#cartopy_f(t,lats,lons,color='RdBu_r',out='',cbar=True)
#plt.show()










