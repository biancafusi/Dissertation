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

from   Parameters import b1 

# own function to transform the data in data_time 
from   source.data_own          import data_day

import source.functions as fnc

# Function with the definition of differents projetions
from   source.cartopyplot   import cartopy1,cartopy_amazon


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

conv =b1.t2mj[0,:,:]
tota =b1.totprec[4,:,:]
prec =b1.convprec[4,:,:]


######print(b1.time.values)

#cartopy1(w,lats,lons,b1=100,b2=100,nn=10,plotname='',figname='',color='RdBu_r',out='',cbar=True):
cartopy_amazon(conv,lats,lons,b1=20,b2=35,color='RdBu_r',out='',cbar=True)
cartopy_amazon(tota,lats,lons,color='RdBu_r',out='',cbar=True)
cartopy_amazon(prec,lats,lons,color='RdBu_r',out='',cbar=True)
#cartopy_f(t,lats,lons,color='RdBu_r',out='',cbar=True)
plt.show()










