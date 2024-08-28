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
#################################

import numpy as np

import datetime as dt  

import matplotlib.pyplot as plt

####################################################

from   Parameters import *


# own function to transform the data in data_time 
from   source.data_own          import data_day

import source.functions as fnc


# Function with the definition of differents projetions
from   source.cartopyplot   import cartopy1,cartopy_f

from   source.nc_make  import  savetonc

import xarray as xr



print()
print('*****')
print('START')
print('*****')


d1 = ['1999-05-11T18:00:00', '1999-06-21T18:00:00', '2003-07-10T18:00', '2009-08-17T18:00', '2015-09-19T18:00', '2016-06-25T18:00', '2018-07-19T18:00']

datas  = [np.datetime64(s) for s in d1 ]

#var0 = w5.sel(time=datas[0])
#var1 = w5.sel(time=datas[1])
#print(var0)
#print(var1)
#var3= xr.concat([var0,var1],dim='time')
#print(var3.time)
#exit()


#print(var0)
#exit()

#exp=w5
#var='w'

exp=t8
var='t'

#Range of dates in 'datas'
nt = np.shape(datas)[0]

#Compact all times

#for s in datas:
    #var1 = w5.sel(time=s)

for s in range(0,nt):
    var0 = exp.sel(time=datas[s],method='nearest')
    if s>0:
        #var0=xr.combine_by_coords([var0,var1])
        var0=xr.concat([var0,var1],dim='time')

    var1=var0
    print(var1.time.values)



###for s in range(0,nt):
###    s=0
###    var0 = w5.sel(time=datas[0])---1999-05-11
###    if s>0:
###        #xr.concat(var,var1, dim='time)
###        xxxxxxxxxxvar0=xr.combine_by_coords([var0,var1])
###    #comp.append(var1)
###    var1=1999-05-11
###
###    s=1
###    var0 = w5.sel(time=datas[1])---1999-06-21
###    if s>0:
###        var0=xr.combine_by_coords([1999-06-21,1999-05-11])
###    #comp.append(var1)
###    var1=[1999-06-21,1999-05-11]
###
###    s=2
###    var0 = w5.sel(time=datas[1])---2004-07-10
###    if s>0:
###        var0=xr.combine_by_coords([2004-07-10,1999-06-21,1999-05-11])
###    #comp.append(var1)
###    var1=[2004-07-10,1999-06-21,1999-05-11]
###
###
###    #print(comp[s].time.values)


#Xarray concatenate the times in one DataArray
#ss = xr.concat(comp, dim='time')
#print(ss['time'])
#exit()

#Mean in time with xarray

ss=var1[var]
lats =exp.latitude
lons =exp.longitude

varm = ss.mean(dim='time')


cartopy_f(varm[0,:,:], lats,lons,b1=230,b2=290,color='RdBu_r',out='',cbar=True)
plt.show()










