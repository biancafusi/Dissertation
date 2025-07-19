# import pyproj
# from pyproj import datadir
# datadir.set_data_dir("/home/bianca/anaconda3/envs/master/share/proj")
import matplotlib.pyplot as plt
import geopandas as gpd
import xarray as xr
import shapely
from shapely.geometry import Point, box
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset   

import matplotlib

matplotlib.use("Agg")

# Spatial and temporal definitions:
lonW, lonE, latS, latN = -92, -69, 17, 49

initial_day = '2024-09-25T00'
final_day = '2024-09-29T00'

# Folders:
# where_to_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/new_helene_outputs/masked_dataset_hourly_rainfall/'
where_to_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/new_helene_outputs/masked_15km_native/'
run_folder = '/mnt/beegfs/bianca.fusinato/monan/model/'

# # data information for hourly precipitation (MONAN RESOLUTION):
# # not accumulated!
# data_information = [
#     ('ERA5', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/era5/x1.655362.era5_helene_moist_native.nc.nc'),
#     ('GPM-IMERG', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/new_imerg/x1.655362.3B-HHR.MS.MRG.3IMERG.2024092201_1hour.nc'),
#     ('GSMaP', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/GSMaP/x1.655362.helene_gsmap.nc'),
#     ('NWS', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/NWS/x1.655362.rainfall.nc'),
#     ('CP-ON', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
#     ('CP-OFF', run_folder+'helene_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
#     ('CP-15km', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/cp-15/x1.655362.helene_15km_hourly.nc'),
#     ('CP-1HD050', run_folder+'helene_cporg1_gustf1_sub3d0_LT1HD050_ERA5_x1.655362/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
#     ('CP-25', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092500/diag/only_precip_diag_dc.2024-09-25_00.00.00.nc')
# ]

# data information for hourly precipitation (15km NATIVE):
# not accumulated!
data_information = [
    ('ERA5', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/era5/x1.655362.era5_helene_moist_native.nc.nc'),
    ('GPM-IMERG', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/new_imerg/x1.655362.3B-HHR.MS.MRG.3IMERG.2024092201_1hour.nc'),
    ('GSMaP', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/GSMaP/x1.655362.helene_gsmap.nc'),
    ('NWS', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/NWS/x1.655362.rainfall.nc'),
    ('CP-ON', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
    ('CP-OFF', run_folder+'helene_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
    ('CP-15km', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.2621442/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
    ('CP-1HD050', run_folder+'helene_cporg1_gustf1_sub3d0_LT1HD050_ERA5_x1.655362/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
    ('CP-25', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092500/diag/only_precip_diag_dc.2024-09-25_00.00.00.nc')
]

ref_time = np.datetime64(initial_day)

def creating_USA_mask(lat_array, lon_array):
    # Carrega shapefile de terra
    countries = gpd.read_file("/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/new_helene_outputs/shapefiles_usa/ne_10m_admin_0_countries.shp")

    # Extrai lat/lon do rainfall_data
    lon = lon_array
    lat = lat_array

    # Cria meshgrid
    lon2d, lat2d = np.meshgrid(lon, lat)

    usa = countries[countries['ADMIN'] == 'United States of America']

    # Achata e cria pontos
    points = gpd.GeoSeries([Point(xy) for xy in zip(lon2d.ravel(), lat2d.ravel())])

    # Cria GeoDataFrame
    gdf_points = gpd.GeoDataFrame(geometry=points, crs="EPSG:4326")

    # Verifica se cada ponto está dentro de algum polígono de terra
    land_mask_flat = gdf_points.within(usa.unary_union)

    # Converte de volta para shape 2D
    land_mask = land_mask_flat.values.reshape(lat2d.shape)

    return land_mask

def creating_not_USA_mask(lat_array, lon_array):
    # Carrega shapefile de terra
    countries = gpd.read_file("/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/new_helene_outputs/shapefiles_usa/ne_10m_admin_0_countries.shp")

    # Extrai lat/lon do rainfall_data
    lon = lon_array
    lat = lat_array

    # Cria meshgrid
    lon2d, lat2d = np.meshgrid(lon, lat)

    usa = countries[countries['ADMIN'] == 'United States of America']

    # Achata e cria pontos
    points = gpd.GeoSeries([Point(xy) for xy in zip(lon2d.ravel(), lat2d.ravel())])

    # Cria GeoDataFrame
    gdf_points = gpd.GeoDataFrame(geometry=points, crs="EPSG:4326")

    # Verifica se cada ponto está dentro de algum polígono de terra
    land_mask_flat = ~gdf_points.within(usa.unary_union)

    # Converte de volta para shape 2D
    land_mask = land_mask_flat.values.reshape(lat2d.shape)

    return land_mask


def creating_nc_files(label, lat_data, lon_data, rainfall, type_mask):
    
    # criando um novo arquivo:
    ncfile = Dataset(where_to_save + f'{label}_{type_mask}_hourly.nc',mode='w',format='NETCDF4_CLASSIC') 

    # dando um título para o arquivo:
    ncfile.title=f'Rainfall hourly {label} data'

    # dando as dimensões para o arquivo (obrigatorio):   
    ncfile.createDimension('time', len(rainfall.time)) 
    ncfile.createDimension('lat', len(lat_data))     # latitude axis
    ncfile.createDimension('lon', len(lon_data))    # longitude axis

    # criando as dimensões variáveis do arquivo:
    time = ncfile.createVariable('time', np.float64, ('time',))
    time.units = 'hours since 2024-09-25T00'
    time.long_name = 'time'

    lat = ncfile.createVariable('lat', np.float32, ('lat',))
    lat.units = 'degrees_north'
    lat.long_name = 'latitude'
    lon = ncfile.createVariable('lon', np.float32, ('lon',))
    lon.units = 'degrees_east'
    lon.long_name = 'longitude'

    # criando a variável chuva:
    rainfall_hourly = ncfile.createVariable('rainfall',np.float64,('time','lat','lon'))
    rainfall_hourly.units = 'mm/h' # degrees Kelvin
    rainfall_hourly.standard_name = 'rainfall_hourly'# this is a CF standard name

    # colocando a chuva, latitudes e longitudes dentro do novo arquivo:
    rainfall_hourly[:,:,:] = rainfall
    lat[:] = lat_data
    lon[:] = lon_data
    # diferença em horas
    time_hours = (rainfall.time.values - ref_time) / np.timedelta64(1, 'h')
    time[:] = time_hours

    ncfile.close(); print('Dataset is closed!')

# ======================================================

for label, input_file_data in data_information:
    print(f'Processing {label} data...')
    
    if label == 'ERA5':

        dataset = xr.open_dataset(input_file_data).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon', 'tp': 'rainfall'})
        time = dataset.time.sel(time=slice(initial_day,final_day))
        time_steps =  np.arange(0, len(time), 1)
        dataset_moist = (dataset.assign_coords(lon=((dataset.lon + 180) % 360) - 180).sortby('lon')).sel(time=time, method='nearest')
        
        lat_data = np.round(dataset_moist.lat.sel(lat=slice(latS,latN)).values, 1)
        lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)

        rainfall = (dataset_moist.rainfall.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)) * 1000)

        land_mask_USA = creating_USA_mask(lat_data, lon_data)
        rainfall_USA_only = rainfall.where(land_mask_USA)

        land_mask_not_USA = creating_not_USA_mask(lat_data, lon_data)
        rainfall_not_USA = rainfall.where(land_mask_not_USA)

        creating_nc_files(label, lat_data, lon_data, rainfall_USA_only, 'USA')
        creating_nc_files(label, lat_data, lon_data, rainfall_not_USA, 'not_USA')
    
    elif label == 'NWS':

        dataset = xr.open_dataset(input_file_data).rename({'latitude': 'lat', 'longitude': 'lon'}).sel(lat=slice(latS,latN),lon=slice(lonW,lonE),time=slice(initial_day,final_day))

        lat_data = np.round(dataset.lat.values, 1)
        lon_data = np.round(dataset.lon.values, 1)

        rainfall = dataset.rainfall

        land_mask_USA = creating_USA_mask(lat_data, lon_data)
        rainfall_USA_only = rainfall.where(land_mask_USA)

        land_mask_not_USA = creating_not_USA_mask(lat_data, lon_data)
        rainfall_not_USA = rainfall.where(land_mask_not_USA)

        creating_nc_files(label, lat_data, lon_data, rainfall_USA_only, 'USA')
        creating_nc_files(label, lat_data, lon_data, rainfall_not_USA, 'not_USA')

    elif label == 'GSMaP':
      
        dataset_moist = xr.open_dataset(input_file_data).rename({'latitude': 'lat', 'longitude': 'lon', 'precip': 'rainfall'}).transpose('time', 'lat', 'lon').sel(time=slice(initial_day,final_day))
        dataset_moist = dataset_moist.assign_coords(lon=((dataset_moist.lon + 180) % 360) - 180).sortby('lon')

        lat_data = np.round(dataset_moist.lat.sel(lat=slice(latS,latN)).values, 1) 
        lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)

        rainfall = ((dataset_moist.rainfall).sel(lat=slice(latS,latN), lon=slice(lonW, lonE)))
        
        land_mask_USA = creating_USA_mask(lat_data, lon_data)
        rainfall_USA_only = rainfall.where(land_mask_USA)

        land_mask_not_USA = creating_not_USA_mask(lat_data, lon_data)
        rainfall_not_USA = rainfall.where(land_mask_not_USA)

        creating_nc_files(label, lat_data, lon_data, rainfall_USA_only, 'USA')
        creating_nc_files(label, lat_data, lon_data, rainfall_not_USA, 'not_USA')
    
    elif label == 'GPM-IMERG':

        dataset_moist = xr.open_dataset(input_file_data).rename({'latitude': 'lat', 'longitude': 'lon', 'precipitation': 'rainfall'}).transpose('time', 'lat', 'lon').sel(time=slice(initial_day,final_day))

        lat_data = np.round(dataset_moist.lat.sel(lat=slice(latS,latN)).values, 1)
        lon_data = np.round(dataset_moist.lon.sel(lon=slice(lonW, lonE)).values, 1)

        rainfall = (dataset_moist.rainfall.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)))

        land_mask_USA = creating_USA_mask(lat_data, lon_data)
        rainfall_USA_only = rainfall.where(land_mask_USA)

        land_mask_not_USA = creating_not_USA_mask(lat_data, lon_data)
        rainfall_not_USA = rainfall.where(land_mask_not_USA)

        creating_nc_files(label, lat_data, lon_data, rainfall_USA_only, 'USA')
        creating_nc_files(label, lat_data, lon_data, rainfall_not_USA, 'not_USA')
       
    else:
        
        dataset_moist = xr.open_dataset(input_file_data).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'}).sel(time=slice(initial_day, final_day), 
                                                                                                                             lat=slice(latS, latN), lon=slice(lonW, lonE))
        
        lat_data = np.round(dataset_moist.lat.values, 1)
        lon_data = np.round(dataset_moist.lon.values, 1)

        rainfall = dataset_moist.rainnc + dataset_moist.rainc

        land_mask_USA = creating_USA_mask(lat_data, lon_data)
        rainfall_USA_only = rainfall.where(land_mask_USA)

        land_mask_not_USA = creating_not_USA_mask(lat_data, lon_data)
        rainfall_not_USA = rainfall.where(land_mask_not_USA)

        creating_nc_files(label, lat_data, lon_data, rainfall_USA_only, 'USA')
        creating_nc_files(label, lat_data, lon_data, rainfall_not_USA, 'not_USA')
       