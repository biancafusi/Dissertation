#################################################
# Program to read variable of a nc file
# using python with NetCdf
# Create by: Jhonatan Aguirre
# Date:06/02/2020
# working:yes
#################################################

# Python library to work with Netcdf4
from    netCDF4         import Dataset,num2date, date2num

import datetime as dt

import numpy as np

import xarray as xr

class variables(object):

    def __init__(self):
        self.lats       = 'latitude' 
        self.lons       = 'longitude'	
        self.time       = 'time'
        self.pressure   = 'pressure'
        self.zg         = 'geopotential_height' 
        self.u          = 'x_wind' 
        self.v          = 'y_wind' 

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)


def ncload_v(file_l):

    label=variables()
    nc_file    = '%s'%(file_l)
    nc_v = Dataset(nc_file,'r',format='NETCDF4')

    #variables name 
    label.time       = nc_v.variables['time']
    label.lats       = nc_v.variables['latitude'] 
    label.lons       = nc_v.variables['longitude']	
    label.pressure   = nc_v.variables['pressure']
    label.v         = nc_v.variables['y_wind'] 

    tu = "hours since 1970-01-01 00:00:00 +00:00:00"
    tc = "360_day"

    label.data       = num2date(label.time[:],units=tu,calendar=tc)


    return label

def xarray_v(file_l,it=1,ft=1,ilt=1,flt=1,ilg=1,flg=1,ilev=1,flev=1):

    label      =  variables()
    nc_file    = '%s'%(file_l)
    nc_v       =  xr.open_dataset(nc_file)

    #nc_v       = nc_v.metpy.parse_cf()



    if (flt!=1):

        #variables name 
        label.data       = nc_v['time']
        label.lats       = nc_v['latitude'][ilt:flt] 
        label.lons       = nc_v['longitude']
        label.pressure   = nc_v['pressure']
        label.v          = nc_v['y_wind'][:,:,ilt:flt,:] 


    elif (flg!=1):
        label.data       = nc_v['time']
        label.lats       = nc_v['latitude'][:] 
        label.lons       = nc_v['longitude'][ilg:flg]	
        label.pressure   = nc_v['pressure'][:]
        label.v          = nc_v['y_wind'][:,:,:,ilg:flg] 


    elif (ft!=1):
        label.data       = nc_v['time'][it:ft]
        label.lats       = nc_v['latitude'] 
        label.lons       = nc_v['longitude']	
        label.pressure   = nc_v['pressure']
        label.v          = nc_v['y_wind'][it:ft,:,:,:] 

    elif (flev!=1):
        label.data       = nc_v['time']
        label.lats       = nc_v['latitude']
        label.lons       = nc_v['longitude']
        label.pressure   = nc_v['pressure'][ilev:flev]
        label.v          = nc_v['y_wind'][:,ilev:flev,:,:] 

    else:

        label.data       = nc_v['time'][it:ft]
        label.lats       = nc_v['latitude'][ilt:flt]
        label.lons       = nc_v['longitude'][ilg:flt]
        label.pressure   = nc_v['pressure'][ilev:flev]
        label.v          = nc_v['y_wind'][it:ft,ilev:flev,ilt:flt,ilg:flt] 


    return label,nc_v

##xr.open_dataset('wrfout_d01_2019-04-16_15_00_00', decode_coords=False).to_netcdf('test.nc')

def xarray_u(file_l,it=1,ft=1,ilt=1,flt=1,ilg=1,flg=1,ilev=1,flev=1):

    label=variables()
    nc_file    = '%s'%(file_l)
    nc_v       =  xr.open_dataset(nc_file)

    #nc_v       = nc_v.metpy.parse_cf()

    if (flt!=1):

        #variables name 
        label.data       = nc_v['time']
        label.lats       = nc_v['latitude'][ilt:flt] 
        label.lons       = nc_v['longitude']
        label.pressure   = nc_v['pressure']
        label.u          = nc_v['x_wind'][:,:,ilt:flt,:] 

    elif (flg!=1):
        label.data       = nc_v['time']
        label.lats       = nc_v['latitude'][:] 
        label.lons       = nc_v['longitude'][ilg:flg]	
        label.pressure   = nc_v['pressure'][:]
        label.u          = nc_v['x_wind'][:,:,:,ilg:flg] 


    elif (ft!=1):
        label.data       = nc_v['time'][it:ft]
        label.lats       = nc_v['latitude'] 
        label.lons       = nc_v['longitude']	
        label.pressure   = nc_v['pressure']
        label.u          = nc_v['x_wind'][it:ft,:,:,:] 

    elif (flev!=1):
        label.data       = nc_v['time']
        label.lats       = nc_v['latitude']
        label.lons       = nc_v['longitude']
        label.pressure   = nc_v['pressure'][ilev:flev]
        label.u          = nc_v['x_wind'][:,ilev:flev,:,:] 

    else:

        label.data       = nc_v['time'][it:ft]
        label.lats       = nc_v['latitude'][ilt:flt]
        label.lons       = nc_v['longitude'][ilg:flt]
        label.pressure   = nc_v['pressure'][ilev:flev]
        label.u          = nc_v['x_wind'][it:ft,ilev:flev,ilt:flt,ilg:flt] 


    return label,nc_v


def ncload_u(file_l):

    label=variables()

    # Your filename
    nc_file    = '%s'%(file_l)

    # Dataset is the class behavior to open the file
    # and create an instance of the ncCDF4 class
    nc_v = Dataset(nc_file,'r',format='NETCDF4')

    #To see the nc file
    #nc_attrs, nc_dims, nc_vars = ncdump

    #variables name 
    label.time       = nc_v.variables['time']
    label.lats       = nc_v.variables['latitude'] 
    label.lons       = nc_v.variables['longitude']	
    label.pressure   = nc_v.variables['pressure']

    #label.zg         = nc_v.variables['geopotential_height'] 
    label.u         = nc_v.variables['x_wind'] 
    #label.va         = nc_v.variables['x_wind'] 


    #time calendar to transform to datatime python data
    #+ to UTC-4
    #- to UTC+4

    tu = "hours since 1970-01-01 00:00:00 +00:00:00"
    #tc = "gregorian"
    tc = "360_day"

    #dt.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    #print(dt.datetime.strptime(label.time[10].ctime(), "%c"))


    label.data       = num2date(label.time[:],units=tu,calendar=tc)

    #print(label.data[10])

    #print(dt.datetime.strptime(label.data[10], "%c"))
    #exit()

    return label

class anomaly_vars(object):

    def __init__(self):

        self.lat        = 'lat' 
        self.lon        = 'lon'	
        self.time1      = 'time1'
        self.time2      = 'time2'
        self.us         = 'u_anly_summer' 
        self.uw         = 'u_anly_winter' 

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

#To assint the label of the family of 
#variables

def ncload_anomaly(file_l):

    label=anomaly_vars()


    # Your filename
    nc_file    = '%s'%(file_l)

    nc_v = Dataset(nc_file,'r+')

    #To see the nc file
    #nc_attrs, nc_dims, nc_vars = ncdump

    #variables name 
    label.time1      = nc_v.variables['time1']
    label.time2      = nc_v.variables['time2']
    label.lat        = nc_v.variables['lat'] 
    label.lon        = nc_v.variables['lon']	
    #label.pressure    = nc_v.variables['lev']


    label.us         = nc_v.variables['u_anly_summer'] 
    label.uw         = nc_v.variables['u_anly_winter'] 

    tu = "hours since 1970-01-01 00:00:00 +00:00:00"
    tc = "360_day"

    label.data1       = num2date(label.time1[:],units=tu,calendar=tc)
    label.data2       = num2date(label.time2[:],units=tu,calendar=tc)

    return label

