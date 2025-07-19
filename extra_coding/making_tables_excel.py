import pandas as pd
import xarray as xr
import numpy as np

from codes_updated.namelist_for_pathing import *
'''
Developed by Bianca Fusinato.
READ ME:        
            The code logic is described as follows:
            Get all the data at the same time period;
            Save all the data into one dataset;
            Get the minimum MSLP;
            With this minimum, creates a box to look for the maximum Vmax inside off it,
            being the minimum MSLP point at the center;
            Get a pandas dataframe with all those data;
            Export into excel table format.

Obs.: One could modify the 'Preparing the data' part in other to adequate to one's data
Obs.2: One could modify the logic to get the minimum MSLP values
'''

############################ PREPARING THE DATA ##########################################
NOAA = xr.open_dataset(NOAA_path)
ERA5 = xr.open_dataset(ERA5_path)
CONTROL = xr.open_dataset(CONTROL_path)
EXPERIMENT = xr.open_dataset(EXPERIMENT_path)

# Rename to get time lat lon
ERA5 = ERA5.rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'msl': 'mslp'})
EXPERIMENT = EXPERIMENT.rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'})
CONTROL = CONTROL.rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'})

# Defining the time according to my reference data:
time = NOAA.time.sel(time=slice(initial_time,final_time))
NOAA_hourly = NOAA.sel(time=time)
MSLP = NOAA_hourly.mslp
WSPD_MAX = NOAA_hourly.vmax*1.852       # Passing from knots to km/h. This is already the maximum values!
lat = NOAA_hourly.lat
lon = NOAA_hourly.lon

# Model data:
EXPERIMENT_hourly = EXPERIMENT.sel(time=time,lat=slice(latS,latN),lon=slice(lonW,lonE))


lat_EXPERIMENT = EXPERIMENT_hourly.lat
lon_EXPERIMENT = EXPERIMENT_hourly.lon
MSLP_EXPERIMENT = EXPERIMENT_hourly.mslp/100
WSPD_EXPERIMENT = calc_wind_gustfront(EXPERIMENT_hourly)

CONTROL_hourly = CONTROL.sel(time=time,lat=slice(latS,latN),lon=slice(lonW,lonE))

lat_CONTROL = CONTROL_hourly.lat
lon_CONTROL = CONTROL_hourly.lon
MSLP_CONTROL = CONTROL_hourly.mslp/100

if label_control == 'CP-OFF':                   # KEEP IN MIND THAT THIS MIGHT BE CHANGED
    WSPD_CONTROL = calc_wind(CONTROL_hourly)
else:
    WSPD_CONTROL = calc_wind_gustfront(CONTROL_hourly)

# ERA5 data:
ERA5_hourly = ERA5.sel(time=time, method='nearest')
ERA5_hourly = ERA5_hourly.sel(lat=slice(latN,latS),lon=slice(lonW,lonE))
ERA5_hourly = ERA5_hourly.transpose('time', 'lat', 'lon')
lat_ERA5 = ERA5_hourly.lat[::-1]
lon_ERA5 = ERA5_hourly.lon
MSLP_ERA5 = ERA5_hourly.mslp.sel(lat=lat_ERA5) / 100    # to hPa
WSPD_ERA5 = calc_wind(ERA5_hourly)                      # KEEP IN MIND THAT THIS MIGHT BE CHANGED


datasets = [
    (MSLP, WSPD_MAX, lat, lon, 'NOAA'),
    (MSLP_ERA5, WSPD_ERA5, lat_ERA5, lon_ERA5, 'ERA5'),
    (MSLP_EXPERIMENT, WSPD_EXPERIMENT, lat_EXPERIMENT, lon_EXPERIMENT, label_experiment),
    (MSLP_CONTROL, WSPD_CONTROL, lat_CONTROL, lon_CONTROL, label_control)
]


#################################### TABLE ##########################################

columns = ['MSLP (hPa)', 'WSPD (km/h)', 'Lat', 'Lon']

index = ['NOAA', 'ERA5', 'CP-ON', 'CP-OFF']

dlat, dlon = 0.25, 0.25

with pd.ExcelWriter(excel_spreadsheet_name + '.xlsx') as writer:  
    
    for t in range(0, 28, 1):

        for dataset_MSLP, dataset_WSPD, lat_array, lon_array, label, in datasets:
                    
            MSLP_t = dataset_MSLP.isel(time=t)
            WSPD_t = dataset_WSPD.isel(time=t)

            if label == 'NOAA':

                lon_array_sel = lon_array.isel(time=t)
                lat_array_sel = lat_array.isel(time=t)

                lon_points = lon_array_sel.values
                lat_points = lat_array_sel.values
                MSLP_values = MSLP_t.values 
                WSPD_values = WSPD_t.values

                NOAA_data = MSLP_values, WSPD_values, lat_points, lon_points 

            else:       

                lat_t, lon_t = np.meshgrid(lat_array, lon_array, indexing='ij') 

                mask = MSLP_t.values == np.min(MSLP_t.values)
                valid_mask = (lat_t <= 40) & (lon_t > -97) & mask
                
                MSLP_values = MSLP_t.values[valid_mask]
                lat_points = lat_t[valid_mask]
                lon_points = lon_t[valid_mask]

                if MSLP_values.size > 0:
                    MSLP_values = MSLP_values[0]
                    lat_points = lat_points[0]
                    lon_points = lon_points[0]

                if label == 'ERA5':

                    # Calculating the wind nearby minimum MSLP point
                    upper_lat, lower_lat = lat_points + dlat, lat_points - dlat
                    left_lon, right_lon = lon_points - dlon, lon_points - dlon

                    WSPD_sliced = WSPD_t.sel(lat=slice(upper_lat,lower_lat),lon=slice(left_lon,right_lon))
                    mask_wind = WSPD_t.values == np.max(WSPD_sliced.values)
                    WSPD_values = WSPD_t.values[mask_wind]
                    WSPD_values = WSPD_values.item()

                
                elif label != 'ERA5':
                
                    # Calculating the wind nearby minimum MSLP point
                    upper_lat, lower_lat = lat_points + dlat, lat_points - dlat
                    left_lon, right_lon = lon_points - dlon, lon_points + dlon

                    WSPD_sliced = WSPD_t.sel(lat=slice(lower_lat, upper_lat),lon=slice(left_lon,right_lon))

                    mask_wind = WSPD_t.values == np.max(WSPD_sliced.values)
                    WSPD_values = WSPD_t.values[mask_wind]
                    if WSPD_values.size > 0:
                        WSPD_values = WSPD_values[0]
                

            if label == 'ERA5':
                ERA5_data = MSLP_values, WSPD_values, lat_points, lon_points 
            
            if label == label_experiment:
                EXPERIMENT_data = MSLP_values, WSPD_values, lat_points, lon_points 
            
            if label == label_control:
                CONTROL_data = MSLP_values, WSPD_values, lat_points, lon_points

        data_in_dataframe = pd.DataFrame([NOAA_data, ERA5_data,EXPERIMENT_data,CONTROL_data],index, columns)
        timestamp = pd.Timestamp(time[t].values).strftime('%Y%m%d_%H%M%S')

        # Write data to a new sheet
        data_in_dataframe.to_excel(writer, sheet_name=timestamp)


