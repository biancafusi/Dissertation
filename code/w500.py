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

from   Parameters import *#u3,u5


# own function to transform the data in data_time 
from   source.data_own          import data_day

import source.functions as fnc


# Function with the definition of differents projetions
from   source.cartopyplot   import cartopy1,cartopy_f

from   source.nc_make  import  savetonc


#import xarray as xr
#import cartopy.crs as ccrs
#import metpy.calc as met
#from  metpy.units import units
#from  scipy.integrate import quad


#print(w5)
print(t8)
#print(w5.variables)
#print(w5.expver[1].values)


#To calculate the divergent, skip=1
#skip=10

#levs =w5.values
datas=w5.time
lats =w5.latitude
lons =w5.longitude
w    =w5.w[0,0,:,:]
t    =t8.t[0,0,:,:]


print(w5.time.values)

#cartopy1(w,lats,lons,b1=100,b2=100,nn=10,plotname='',figname='',color='RdBu_r',out='',cbar=True):
cartopy_f(w,lats,lons,b1=-0.5,b2=0.5,color='RdBu_r',out='',cbar=True)
cartopy_f(t,lats,lons,color='RdBu_r',out='',cbar=True)
plt.show()










