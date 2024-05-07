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
from source.cartopyplot import cartopy1, cartopy_amazon

def mean_over_time_range(data, time_var, start_time, end_time):
    start_index = (time_var >= start_time).argmax()
    end_index = (time_var >= end_time).argmax()
    return data[start_index:end_index].mean(axis=0)

# Example usage:
start_time = 24  # Starting time index
end_time = 49    # Ending time index

mean_temp = mean_over_time_range(b1.t2mj, b1.time, start_time, end_time)
mean_totprec = mean_over_time_range(b1.totprec, b1.time, start_time, end_time)
mean_convprec = mean_over_time_range(b1.convprec, b1.time, start_time, end_time)

# to work without display
#plt.switch_backend('agg')

####from   source.nc_make  import  savetonc

#print(b1)

#To calculate the divergent, skip=1
#skip=10

#levs =w5.values
datas=b1.time
lats =b1.lat
lons =b1.lon

#lats = lats.where((lats>-9)&(lats<6),drop=True) 

temp =b1.t2mj[30,:,:]
tota =b1.totprec[30,:,:]
conv =b1.convprec[30,:,:]

######print(b1.time.values)

#cartopy1(w,lats,lons,b1=100,b2=100,nn=10,plotname='',figname='',color='RdBu_r',out='',cbar=True):
cartopy_amazon(temp,lats,lons,nn=12,plotname='Temperature',figname='temp_secaCP00',color='RdBu_r',out=out_fig,cbar=True)
cartopy_amazon(tota,lats,lons,b1=0,b2=9,nn=30,plotname='Total Precipitation',figname='total_secaCP00',color='RdBu_r',out=out_fig,cbar=True)
cartopy_amazon(conv,lats,lons,b1=0,b2=9,nn=30,plotname='Convective Precipitation',figname='conv_secaCP00',color='RdBu_r',out=out_fig,cbar=True)
#cartopy_f(t,lats,lons,color='RdBu_r',out='',cbar=True)
#plt.show()










