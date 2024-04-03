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

import os, sys
import numpy as np
import datetime as dt  
import matplotlib.pyplot as plt

# Function with the definition of differents projetions
from   plotprojection    import plot_own_cyli,plot_own_ortho, plot_own_robin
# Function to concatenate nc files 
from   concfunction      import conc_func
# Function to read ncfiles 
from   netCDF4           import Dataset
# Own Functions, to read the data, make anomaly 
from   function          import filename2,anom

# own function to transform the data in data_time 
from   data_own          import data_day

# Function to look the ncfiles
from   variablesfunction import ncdump

from files_adress import robin_data


nc_f = gpcp_data

#To show the file variables
nc_fid = Dataset(nc_f, 'r') 
                              
#nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)
lats, lons, air,time = filename2(nc_f)

# Data begins from 1800/1/1
# *24 because it is in days not in hours!
dt_time = [dt.date(1800, 1, 1) + dt.timedelta(hours=t*24) 
           for t in time]


#Defined the data to use:
#from--- to  
date_start1  = dt.date(2021,1,1)
date_finish1 = dt.date(2021,1,1)
#Found the index of the specified data in the vector dt_time
index1       = data_day(date_start1,dt_time)
index2       = data_day(date_finish1,dt_time)

#Cylindrical projection 
#ok
fig1=plot_own_cyli(air[index1,:,:],lats,lons,'','cylindrical_projection')

#Orthogonal  projection 
#ok
fig2=plot_own_ortho(air[index1,:,:],lats,lons,'','orthogonal_projection')

#Robin projection 
#ok, mas nao funciona colocando o brasil no centro
fig3=plot_own_robin(air[index1,:,:],lats,lons,'','robin_projection')

plt.show()





