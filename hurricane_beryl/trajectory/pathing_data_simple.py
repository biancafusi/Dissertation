import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib

from codes_updated.namelist_for_pathing import *

# matplotlib.use("Agg") # This line is deactivating the graph terminal part

'''
Developed by Bianca Fusinato.
READ ME:        
            The code logic is described as follows:
            Get all the data at the same time period;
            Save all the data into one dataset;
            Plot the minimum value of MSLP into simple xy graph of each dataset.

Obs.: One could modify the 'Preparing the data' part in other to adequate to one's data
Obs.2: One could modify the logic to get the minimum MSLP values
Obs.3: The default color for the experiment line in the graph is red, but can be changed
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
lat = NOAA_hourly.lat
lon = NOAA_hourly.lon

# Model data:
EXPERIMENT_hourly = EXPERIMENT.sel(time=time,lat=slice(latS,latN),lon=slice(lonW,lonE))

lat_EXPERIMENT = EXPERIMENT_hourly.lat
lon_EXPERIMENT = EXPERIMENT_hourly.lon
MSLP_EXPERIMENT = EXPERIMENT_hourly.mslp/100

CONTROL_hourly = CONTROL.sel(time=time,lat=slice(latS,latN),lon=slice(lonW,lonE))

lat_CONTROL = CONTROL_hourly.lat
lon_CONTROL = CONTROL_hourly.lon
MSLP_CONTROL = CONTROL_hourly.mslp/100

# ERA5 data:
ERA5_hourly = ERA5.sel(time=time, method='nearest')
ERA5_hourly = ERA5_hourly.sel(lat=slice(latN,latS),lon=slice(lonW,lonE))
ERA5_hourly = ERA5_hourly.transpose('time', 'lat', 'lon')
lat_ERA5 = ERA5_hourly.lat[::-1]
lon_ERA5 = ERA5_hourly.lon
MSLP_ERA5 = ERA5_hourly.mslp.sel(lat=lat_ERA5) / 100  # to hPa

# One could add more type of data following this structure
datasets = [
    (MSLP, lat, lon, 'o', 'NOAA', 'green'),
    (MSLP_ERA5, lat_ERA5, lon_ERA5, 's', 'ERA5', 'blue'),
    (MSLP_EXPERIMENT,  lat_EXPERIMENT, lon_EXPERIMENT, '^', label_experiment, 'red'),
    (MSLP_CONTROL, lat_CONTROL, lon_CONTROL, '*', label_control, control_color)
]

#################################### PLOT ##########################################

plt.figure(figsize=(15, 9))
proj = ccrs.Mercator()
ax = plt.axes(projection=proj)

# Map behind the plot
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)
ax.set_extent([-102, -68, 13, 36], crs=ccrs.PlateCarree()) # One could change this to get the study-area lat/lon region

gl = ax.gridlines(
    crs=ccrs.PlateCarree(), draw_labels=True,
    linewidth=1, color='gray', alpha=0.5, linestyle='--'
)

for dataset_MSLP, lat_array, lon_array, marker, label, color in datasets:
    
    lat_points, lon_points, MSLP_values = [], [], []

    for t in range(0, len(time), 1): 

            MSLP_t = dataset_MSLP.isel(time=t)

            if label == 'NOAA':

                lon_array_sel = lon_array.isel(time=t)
                lat_array_sel = lat_array.isel(time=t)

                lon_points.append(lon_array_sel.values)
                lat_points.append(lat_array_sel.values)

            else:
                if label != 'ERA5':
                    mask = (MSLP_t.values == np.min(MSLP_t.values))
                else:
                    mask = MSLP_t.values == np.min(MSLP_t.values)

                lat_t, lon_t = np.meshgrid(lat_array, lon_array, indexing='ij')
                valid_mask = (lat_t <= 40) & (lon_t > -97) & mask
                lat_points.extend(lat_t[valid_mask].ravel())  
                lon_points.extend(lon_t[valid_mask].ravel()) 
                MSLP_values.extend(MSLP_t.values[valid_mask].ravel())
    
    lat_points = np.array(lat_points)
    lon_points = np.array(lon_points)
    MSLP_values = np.array(MSLP_values)

    ax.plot(
        lon_points, lat_points,
        color=color, linestyle='-', marker=marker, linewidth=1.8, label=label,
        transform=ccrs.PlateCarree()
    )

ax.legend(loc='upper right', fontsize=10)
ax.set_adjustable('box')
ax.set_aspect('auto')

ax.set_title(graph_title,fontsize=12)
plt.tight_layout()

plt.savefig(where_save + saving_name, dpi=300, bbox_inches='tight')


