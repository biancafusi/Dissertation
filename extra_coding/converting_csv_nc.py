import pandas as pd
import xarray as xr
import numpy as np

'''
READ ME:
            This code takes a .csv file (with some editing) and turns into .nc file
            If this would be used for taking the hurricanes data, it is more safe to get them
            thought the hurricanes_tracker.py code.
'''

# # Namelist:

data_main_location = '/home/bianca/Documentos/masters/data/'
data_name = 'NOAA_data_2.csv'
nc_file_name = 'NOAA_updated_2.nc'

# # Code:
dataframe = pd.read_csv(data_main_location + data_name)
dataframe = dataframe.drop(['Unnamed: 7', 'Unnamed: 8'], axis=1) # cleaning the garbage

dataframe['time'] = pd.to_datetime(dataframe['Date'] + ' ' + dataframe['(UTC)'])
dataframe = dataframe.drop(['Date', '(UTC)'], axis=1)  

convert_dict = {'(CKZ)':np.float64, '(kts)':np.float64, '(km/h)':np.float64}
dataframe = dataframe.astype(convert_dict)

latitude = dataframe['Lat'].values
longitude = dataframe['Lon'].values

# essential
ds = xr.Dataset(
    {
        "pressure": ("time", dataframe['(CKZ)'].values),
        "wind_speed_kts": ("time", dataframe['(kts)'].values),
        "wind_speed_kmh": ("time", dataframe['(km/h)'].values),
    },
    coords={
        "time": dataframe['time'].values,
        "latitude": ("time", latitude),
        "longitude": ("time", longitude),
    }
)

# not necessary
ds['pressure'].attrs["units"] = "hPa"
ds['wind_speed_kts'].attrs["units"] = "knots"
ds['wind_speed_kmh'].attrs["units"] = "km/h"
ds['latitude'].attrs["units"] = "degrees_north"
ds['longitude'].attrs["units"] = "degrees_east"

output_path = data_main_location + nc_file_name
ds.to_netcdf(output_path)

