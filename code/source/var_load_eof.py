#################################################
# Program to read variable of a nc file
# using python with NetCdf
# Create by: Jhonatan Aguirre
# Date:06/02/2020
# working:yes
#################################################

# Python library to work with Netcdf4
from    netCDF4         import Dataset

# To save the time coordinate in specific format
from    netCDF4         import num2date, date2num

import datetime as dt

import numpy as np

import xarray as xr


class variables(object):

    def __init__(self):

        self.time1       = 'time1'
        self.time2       = 'time2'
        self.lats        = 'latitude' 
        self.lons        = 'longitude'	
        self.u3as        = 'u3as' 
        self.u3aw        = 'u3aw' 
        self.u5as        = 'u5as' 
        self.u5aw        = 'u5aw' 
        self.v3as        = 'v3as' 
        self.v3aw        = 'v3aw' 
        self.v5as        = 'v5as' 
        self.v5aw        = 'v5aw' 

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

def ncload(file_l):

    label      = variables()
    nc_file    = '%s'%(file_l)
    nc_v       = Dataset(nc_file,'r+')

    #variables name 
    label.time1      = nc_v.variables['time1']
    label.time2      = nc_v.variables['time2']

    label.lats       = nc_v.variables['latitude'] 
    label.lons       = nc_v.variables['longitude']	

    label.u3as        = nc_v.variables['u3as'] 
    label.u3aw        = nc_v.variables['u3aw'] 
    label.u5as        = nc_v.variables['u5as'] 
    label.u5aw        = nc_v.variables['u5aw'] 
    label.v3as        = nc_v.variables['v3as'] 
    label.v3aw        = nc_v.variables['v3aw'] 
    label.v5as        = nc_v.variables['v5as'] 
    label.v5aw        = nc_v.variables['v5aw'] 

    tu = "hours since 1970-01-01 00:00:00 +00:00:00"
    tc = "360_day"

    label.data1       = num2date(label.time1[:],units=tu,calendar=tc)
    label.data2       = num2date(label.time2[:],units=tu,calendar=tc)

    return label

class variables_vor(object):

    def __init__(self):

        self.time        = 'time'
        self.time1       = 'time1'
        self.time2       = 'time2'
        self.lats        = 'latitude' 
        self.lons        = 'longitude'	
        self.levs        = 'lev'	
        self.avsummer    = 'anomaly_summer_v' 
        self.avwinter    = 'anomaly_winter_v' 
        self.assummer    = 'anomaly_summer_s' 
        self.aswinter    = 'anomaly_winter_s' 

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

def ncload_vor(file_l):

    label=variables_vor()
    nc_file    = '%s'%(file_l)
    nc_v       =  xr.open_dataset(nc_file)

    #variables name 
    #label.time       = nc_v.variables['time']
    label.time1       = nc_v.variables['time1']
    label.time2       = nc_v.variables['time2']

    label.lats       = nc_v.variables['latitude'] 
    label.lons       = nc_v.variables['longitude']	

    label.levs       = nc_v.variables['lev']	

    label.avsummer    = nc_v.variables['anomaly_summer_v'] 
    label.avwinter    = nc_v.variables['anomaly_winter_v'] 
    label.assummer    = nc_v.variables['anomaly_summer_s'] 
    label.aswinter    = nc_v.variables['anomaly_winter_s'] 


    return label
