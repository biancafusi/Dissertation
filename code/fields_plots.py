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

from   Parameters import b1, out_fig 

# own function to transform the data in data_time 
from   source.data_own import data_day

import source.functions as fnc

# Function with the definition of differents projetions
from source.cartopyTEST import cartopy_amazon

# to work without display
#plt.switch_backend('agg')

####from   source.nc_make  import  savetonc

datas=b1.time
lats =b1.lat
lons =b1.lon

temp = b1.t2mj[24:49,:,:]
resultados1 = []

for i in range(24,49):
    soma = temp[i,:,:].sum

exit()



tota =b1.totprec[30,:,:]
conv =b1.convprec[30,:,:]



cartopy_amazon(mean_totprec,lats,lons,nn=12,plotname='Temperature',figname='temp_secamediaCP00',color='RdBu_r',out=out_fig,cbar=True)

#TOTAL PRECIPITATION
cartopy_amazon(tota,lats,lons,b1=0,b2=9,nn=30,plotname='Total Precipitation',figname='total_secaCP00',color='RdBu_r',out=out_fig,cbar=True)

#CONVECTIVE PRECIPITATION
cartopy_amazon(conv,lats,lons,b1=0,b2=9,nn=30,plotname='Convective Precipitation',figname='conv_secaCP00',color='RdBu_r',out=out_fig,cbar=True)




#cartopy_f(t,lats,lons,color='RdBu_r',out='',cbar=True)
#plt.show()










