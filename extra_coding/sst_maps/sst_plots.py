import xarray as xr
import numpy as np
from shape_plot_sst import *
from namelist_sst import *

def SST_PLOTTER(file_path, initial_day, final_day, output_path, title_prefix):

    raw_data = xr.open_dataset(file_path)

    if title_prefix == 'ERA5':
        dataset = raw_data.assign_coords(longitude=((raw_data.longitude + 180) % 360) - 180).sortby('longitude')
        
        time = dataset.valid_time.sel(valid_time=slice(initial_day,final_day)).values
        
        sliced_dataset = dataset.sel(longitude=slice(lonW,lonE),latitude=slice(latN,latS),valid_time=slice(initial_day,final_day))
        lat = dataset.latitude.sel(latitude=slice(latN,latS))
        lon = dataset.longitude.sel(longitude=slice(lonW,lonE))
        
        slice_sst = sliced_dataset.sst - 273.15
    
    elif title_prefix == 'NOAA':
        print('not ready yet ...')
    
    else:
        time = raw_data.Time.sel(Time=slice(initial_day,final_day)).values
        
        sliced_dataset = raw_data.sel(longitude=slice(lonW,lonE),latitude=slice(latS,latN),Time=slice(initial_day,final_day))
        lat = raw_data.latitude.sel(latitude=slice(latS,latN))
        lon = raw_data.longitude.sel(longitude=slice(lonW,lonE))

        slice_sst = sliced_dataset.sst - 273.15
    
    
    plot_sst = slice_sst[0,:,:]
    
    beryl_sst(plot_sst, lat, lon, lim_min=18, lim_max=35, num_points=11, 
    title=title_prefix+' - '+np.datetime_as_string(time[0],unit='h')+' '+'(°C)', figname=f'sst_{title_prefix}', out=output_path, cbar=True, unit='°C')
        
        
    return False


SST_PLOTTER(data_path, initial_day, final_day, output_path, title_prefix)