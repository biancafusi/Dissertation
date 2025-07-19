import xarray as xr
import numpy as np
from plotter_variables import *
from plots_beryl import *

name_file = '/home/bianca/Documentos/masters/data/july_fields_180.nc'

dataset = xr.open_dataset(name_file)

initial_day = '2024-07-03T00'
final_day = '2024-07-11T00'

'''
* valid_time  (valid_time) datetime64[ns] 3kB 2024-07-01 ... 2024-07-17T23:...
* longitude   (longitude) float64 12kB -180.0 -179.8 -179.5 ... 179.5 179.8
* latitude    (latitude) float64 6kB 90.0 89.75 89.5 ... -89.5 -89.75 -90.0
'''
lonW, lonE, latS, latN = -106, -50, 5, 41

lats = dataset.latitude.sel(latitude=slice(latN,latS))
lons = dataset.longitude.sel(longitude=slice(lonW,lonE))

slice_prec = dataset.tp.sel(valid_time=slice(initial_day,final_day),latitude=slice(latN,latS),longitude=slice(lonW,lonE))*1000

time = dataset.valid_time.sel(valid_time=slice(initial_day,final_day)).values

timestep = 1

accumulated = np.zeros_like(slice_prec)

while timestep <=len(time):

    print(timestep)
    accumulated[timestep,:,:] = accumulated[timestep-1,:,:] + slice_prec[timestep,:,:]

    #plot aqui
    beryl_acc_prec(accumulated[timestep,:,:], lats, lons, lim_min=0, lim_max=400, title='test', figname=f'test{timestep}', cbar=True, unit='mm/h')


    timestep += 1

