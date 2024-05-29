#!/usr/bin/python
# -*- coding: UTF-8 -*-

#################################
#PYTHON CODE TO PLOT DIFFERENS 
#MPAS DATA USING CARTOPY AND XARRAY. 
#################################
#PYTHON CODE TO PLOT DIFFERENS 
# Data:01/11/23
#################################
# By: Jhonatan A. A Manco
#################################

# Function to load the ncfiles
import xarray as xr

import source.data_own  as dn

import os as os


#Path to the files 
path='/mnt/beegfs/jhonatan.aguirre/MPAS_Model_Regional/2024050100/pos/runs/GFS/postprd' 

# TO open  a unique file
mp1=path + '/mpas.2024-05-01_00.00.00.nc'
#m1 =  xr.open_dataset(mp1)

# Out figure folder
out_fig='/home/jhonatan.aguirre/git_report/mpas_python/document/fig/'

###################################################3

datei=[0,1,5,2024]
datef=[12,1,5,2024]
hours_step=3

mm=dn.concatenate(datei,datef,hours_step,path,'mpas.')

###########################33
###########################33

# Check if the directory exists
if not os.path.exists(out_fig):
    # If it doesn't exist, create it
    os.makedirs(out_fig)


#TO see the variables
#print(mm.variables)
#[print(i) for i in mm.data_vars]
#print(list(mm.keys()))
#exit()
#print(ds.time)
#print(ncdatas)

#exit()


