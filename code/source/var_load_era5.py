    #################################################
    # Program to read variable of a nc file
    # using python with NetCdf
    # Create by: Jhonatan Aguirre
    # Date:06/02/2020
    # working:yes
    #################################################

# Python library to work with Netcdf4
from  netCDF4         import Dataset,num2date, date2num

import datetime as dt

import numpy as np

import xarray as xr

class variables(object):

    def __init__(self):

        self.lat        = 'lat' 
        self.lon        = 'lon'	
        self.time       = 'time'
        self.plev       = 'plev'
        self.zg         = 'z' 
        self.u          = 'u' 
        self.v          = 'v' 

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

class variables_2(object):

    def __init__(self):

        self.lat        = 'latitude' 
        self.lon        = 'longitude'	
        self.data       = 'time'
        self.level      = 'level'
        self.z          = 'z'
        self.d          = 'd' 
        self.pv         = 'pv' 
        self.u          = 'u' 
        self.v          = 'v' 
        self.v          = 'w' 
        self.vo         = 'vo' 

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

class variables_3(object):

    def __init__(self):

        self.lat        = 'latitude' 
        self.longitude  = 'longitude'	
        self.time       = 'time'
        self.level      = 'lev'
        self.div        = 'd' 
        self.cf         = 'cc' 
        self.gp         = 'z'
        self.pv         = 'pv'
        self.rh         = 'r' 
        self.clwc       = 'clwc' 
        self.q          = 'q' 
        self.T          = 't' 
        self.u          = 'u' 
        self.v          = 'v' 
        self.w          = 'w' 
        self.vo         = 'vo' 

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

def xarray_mean(file_l,it=1,ft=1,ilt=1,flt=1,ilg=1,flg=1,ilev=1,flev=1):

    label=variables_2()
    nc_file    = '%s'%(file_l)
    nc_v       =  xr.open_dataset(nc_file)

    #nc_v       = nc_v.metpy.parse_cf()
    np=8

    label.lat        = nc_v.variables['latitude']
    label.lon        = nc_v.variables['longitude']	
    label.data       = nc_v.variables['time']
    label.level      = nc_v.variables['level']
    label.d          = nc_v.variables['d'] 
    label.pv         = nc_v.variables['pv'] 
    label.u          = nc_v.variables['u'] 
    label.v          = nc_v.variables['v'] 
    label.v          = nc_v.variables['w'] 
    label.vo         = nc_v.variables['vo'] 

    return label,nc_v


def xarray_era5_month(file_l):

    label=variables_3()

    nc_file    = '%s'%(file_l)

    nc_v       =  xr.open_dataset(nc_file)
    #nc_v       =  nc_v.metpy.parse_cf()

    np=8

    #variables name 
    label.data       = nc_v.variables['time'][:]
    label.lat        = nc_v.variables['latitude'][:]
    label.lon        = nc_v.variables['longitude'][:]	
    label.level      = nc_v.variables['level'][:]
    label.d          = nc_v.variables['d'][:,:,:,:] 
    label.pv         = nc_v.variables['pv'][:,:,:,:] 
    label.w          = nc_v.variables['u'][ :,:,:,:] 
    label.u          = nc_v.variables['u'][ :,:,:,:] 
    label.v          = nc_v.variables['v'][ :,:,:,:] 
    label.vo         = nc_v.variables['vo'][:,:,:,:]
    label.gp          = nc_v.variables['z'][:,:,:,:]
    label.T          = nc_v.variables['t'][:,:,:,:]
    label.clwc       = nc_v.variables['clwc'][:,:,:,:]
    label.q          = nc_v.variables['q'][:,:,:,:]
    label.rh         = nc_v.variables['r'][:,:,:,:]
    label.cf         = nc_v.variables['cc'][:,:,:,:]

    return label,nc_v

def xarray_era5(file_l,it=1,ft=1,ilt=1,flt=1,ilg=1,flg=1,ilev=1,flev=1):

    label=variables()

    nc_file    = '%s'%(file_l)

    nc_v       =  xr.open_dataset(nc_file)
    #nc_v       =  nc_v.metpy.parse_cf()

    np=8

    if (flg!=1):

        #variables name 
        label.data       = nc_v.variables['time'][:]
        label.lat        = nc_v.variables['latitude'][::np]
        label.lon        = nc_v.variables['longitude'][ilg:flg:np]	
        label.level      = nc_v.variables['level'][:]
        label.d          = nc_v.variables['d'][ :,:,::np,ilg:flg:np] 
        label.pv         = nc_v.variables['pv'][:,:,::np,ilg:flg:np] 
        label.u          = nc_v.variables['u'][ :,:,::np,ilg:flg:np] 
        label.v          = nc_v.variables['v'][ :,:,::np,ilg:flg:np] 
        label.vo         = nc_v.variables['vo'][:,:,::np,ilg:flg:np]
        label.z          = nc_v.variables['z'][:,:,::np,ilg:flg:np]



    elif (flt!=1):

        label.data       = nc_v.variables['time'][:]
        label.lat        = nc_v.variables['latitude'][ilt:flt:np]
        label.lon        = nc_v.variables['longitude'][::np]	
        label.level      = nc_v.variables['level'][:]
        label.d          = nc_v.variables['d'][ :,:,ilt:flt:np,::np] 
        label.pv         = nc_v.variables['pv'][:,:,ilt:flt:np,::np] 
        label.u          = nc_v.variables['u'][ :,:,ilt:flt:np,::np] 
        label.v          = nc_v.variables['v'][ :,:,ilt:flt:np,::np] 
        label.vo         = nc_v.variables['vo'][:,:,ilt:flt:np,::np]

        label.z          = nc_v.variables['z'][:,:,ilt:flt:np,::np]

    elif (ft!=1):

        label.data       = nc_v.variables['time'][it:ft]
        label.lat        = nc_v.variables['latitude'][::np]
        label.lon        = nc_v.variables['longitude'][::np]	
        label.level      = nc_v.variables['level'][:]
        label.d          = nc_v.variables['d'][ it:ft,:,::np,::np] 
        label.pv         = nc_v.variables['pv'][it:ft,:,::np,::np] 
        label.u          = nc_v.variables['u'][ it:ft,:,::np,::np] 
        label.v          = nc_v.variables['v'][ it:ft,:,::np,::np] 
        label.vo         = nc_v.variables['vo'][it:ft,:,::np,::np]
        label.z          = nc_v.variables['z'][it:ft,:,::np,::np]


    else:

        label.data       = nc_v.variables['time'][it:ft]
        label.lat        = nc_v.variables['latitude'][ilt:flt:np]
        label.lon        = nc_v.variables['longitude'][ilg:flg:np]	
        label.level      = nc_v.variables['level'][:]
        label.d          = nc_v.variables['d'][ it:ft,ilt:flt:np,ilg:flg:np] 
        label.pv         = nc_v.variables['pv'][it:ft,ilt:flt:np,ilg:flg:np] 
        label.u          = nc_v.variables['u'][ it:ft,ilt:flt:np,ilg:flg:np] 
        label.v          = nc_v.variables['v'][ it:ft,ilt:flt:np,ilg:flg:np] 
        label.vo         = nc_v.variables['vo'][it:ft,ilt:flt:np,ilg:flg:np]
        label.z          = nc_v.variables['z'][it:ft,ilt:flt:np,ilg:flg:np]


    return label,nc_v


def xarray_uv(file_l,it=1,ft=1,ilt=1,flt=1,ilg=1,flg=1,ilev=1,flev=1):

    label=variables()
    nc_file    = '%s'%(file_l)
    nc_v       =  xr.open_dataset(nc_file)

    #nc_v       = nc_v.metpy.parse_cf()

    np=8

    if (flg!=1):
        #variables name 
        label.time       = nc_v.variables['time'][:]
        label.lat        = nc_v.variables['lat'][::np]
        label.lon        = nc_v.variables['lon'][ilg:flg:np]
        label.plev       = nc_v.variables['plev'][:]	
        label.u          = nc_v.variables['u'][:,:,::np,ilg:flg:np]	
        label.v          = nc_v.variables['v'][:,:,::np,ilg:flg:np]	
        label.zg         = nc_v.variables['z'][:,:,::np,ilg:flg:np]	

    elif (flt!=1):
        #variables name 
        label.time       = nc_v.variables['time'][:]
        label.lat        = nc_v.variables['lat'][ilt:flt:np]
        label.lon        = nc_v.variables['lon'][::np]
        label.plev       = nc_v.variables['plev'][:]	
        label.u          = nc_v.variables['u'][:,:,ilt:flt:np,::np]	
        label.v          = nc_v.variables['v'][:,:,ilt:flt:np,::np]	
        label.zg         = nc_v.variables['z'][:,:,ilt:flt:np,::np]	

    elif (ft!=1):
        label.time       = nc_v.variables['time'][it:ft]
        label.lat        = nc_v.variables['lat'][::np]
        label.lon        = nc_v.variables['lon'][::np]
        label.plev       = nc_v.variables['plev'][:]	
        label.u          = nc_v.variables['u'][it:ft,:,::np,::np]	
        label.v          = nc_v.variables['v'][it:ft,:,::np,::np]	
        label.zg         = nc_v.variables['z'][it:ft,:,::np,::np]	


    else:

        label.data       = nc_v['time'][it:ft]
        label.lats       = nc_v['latitude'][ilt:flt:np]
        label.lons       = nc_v['longitude'][ilg:flt:np]
        label.pressure   = nc_v['pressure'][ilev:flev]
        label.u          = nc_v['x_wind'][it:ft,ilev:flev,ilt:flt:np,ilg:flg:np] 


    return label,nc_v

def ncload_uv(file_l):

    label=variables()
    nc_file    = '%s'%(file_l)
    nc_v       =  xr.open_dataset(nc_file )
    #nc_v       =  nc_v.metpy.parse_cf()


    #variables name 
    label.time       = nc_v.variables['time'][:]
    #label.time=xr.DataArray(label.time)

    np=8

    label.lat        = nc_v.variables['lat'][::np]
    label.lon        = nc_v.variables['lon'][::np]
    label.plev       = nc_v.variables['plev'][:]	
    label.u          = nc_v.variables['u'][:,:,::np,::np]	
    label.v          = nc_v.variables['v'][:,:,::np,::np]	
    label.zg         = nc_v.variables['z'][:,:,::np,::np]	



    return label,nc_v


