import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as mcolors
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib

matplotlib.use("Agg")

from namelist_for_helene_acc import *

'''
WORKING - REVIEWED MAY 24 2025
'''

# Função de plotar
def total_acc_prec(data, lats, lons, lim_min='', lim_max='', num_points='', title='', figname='', out='', cbar=True, unit='mm'):
    lonW, lonE, latS, latN = -92, -69, 17, 49

    largura_fig = 7 # polegadas
    altura_fig = 4 # polegadas

    projection = ccrs.PlateCarree(central_longitude=180.0, globe=None)
    
    fig = plt.figure(figsize=(largura_fig, altura_fig))
    ax = plt.axes(projection=projection)

    colors = [
        "#FFFFFF", "#E8F6FA", "#D1EEF5", "#B9E6F0", "#A2DEEB", "#8BD6E6", # Tons de azul claro
        "#75BED1", "#60A7BC", "#4A8FA7", "#357892", "#21627D",            # Azul escuro
        "#32CD32", "#3D9E0F", "#40A511",            # Tons de verde
        "#FFFF00", "#FFD700", "#FFA500", "#FF8C00", "#FF4500",            # Tons de amarelo/laranja
        "#FF6347", "#FF0000", "#B22222", "#8B0000",                       # Vermelho intenso
        "#800080",  "#4B0082"             # Roxo a preto                       # Roxo a preto
    ]

    new_labels = np.arange(lim_min, lim_max, num_points)
    
    new_pal = mcolors.LinearSegmentedColormap.from_list("custom", colors, N=len(new_labels))
    norm = mcolors.BoundaryNorm(boundaries=new_labels, ncolors=new_pal.N, clip=True)
    
    levels = new_labels
    filled = ax.contourf(lons.values, lats.values, data, levels=levels,
                         transform=ccrs.PlateCarree(),
                         cmap=new_pal, alpha=0.95, extend='both', norm=norm)

    ax.add_feature(cfeature.COASTLINE, alpha=0.4, linewidth=0.4, edgecolor='black')
    ax.add_feature(cfeature.BORDERS, alpha=0.4, linewidth=0.4)
    ax.add_feature(cfeature.LAND, alpha=0.4, linewidth=0.4)
    ax.add_feature(cfeature.STATES, alpha=0.4, linewidth=0.2)
    ax.add_feature(cfeature.OCEAN, alpha=0.4, linewidth=0.3)
    ax.stock_img()

    ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree()) # lonW lonE latS latN
    # ax.set_adjustable('box')
    # ax.set_aspect('auto')

    max_value = np.max(data)
    ax.text(106, 47.2, f'Max Acc. (mm): \n {max_value:.2f}', ha='center', va='center', fontsize=8, bbox=dict(boxstyle='square',
                    edgecolor='black', facecolor='white'))
    
    ax.set_yticks(np.arange(latS, latN, 5), crs=ccrs.PlateCarree())
    ax.set_xticks(np.linspace(lonW, lonE, 7, dtype=int), crs=ccrs.PlateCarree())
   
    lon_formatter = LongitudeFormatter(number_format='.1f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.1f',
                                      degree_symbol='')

    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=6)

    if cbar:
        CB = fig.colorbar(filled, orientation='vertical', shrink=0.85, aspect=20)
        cbarlabels = new_labels
        CB.set_ticks(cbarlabels)
        CB.ax.tick_params(labelsize=6)
        CB.set_label(label=unit, loc='center', fontsize=6, rotation=90)
        
    fig.tight_layout()

    ax.set_title("%s" % (title), fontsize=8)

    # Plot the path
    # if lon_points and lat_points != 'Nan':
    #     ax.plot(lon_points, lat_points, color='black', linestyle='--', linewidth=0.8, label=label_data, transform=ccrs.PlateCarree())

    #     # Add a text box at the beginning of the path
    #     if len(lon_points) > 0 and len(lat_points) > 0:  # Ensure there are points to plot
    #         ax.text(
    #             lon_points[0], lat_points[0],  # Coordinates of the starting point
    #             label_data,  # Text to display
    #             color='black',  # Text color
    #             fontsize=8,  # Text size
    #             # Text box style
    #             transform=ccrs.PlateCarree()  # Coordinate system
    #     )

    fig.savefig(where_to_save+'%s%s.png' % (out, figname), format='png', dpi=300, bbox_inches='tight')

    return fig


# Oppening the data and plotting:

for label, data_path in data_information:
    print(f'Processing {label}...')

    if label == 'ERA5':
        
        # with the interpolation:
        dataset = xr.open_dataset(data_path).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon'})

        dataset_prec = (dataset.assign_coords(lon=((dataset.lon + 180) % 360) - 180).sortby('lon')).sel(time=slice(initial_day,final_day))
        
        lat_data = dataset_prec.lat.sel(lat=slice(latS,latN))
        lon_data = dataset_prec.lon.sel(lon=slice(lonW,lonE))

        slice_prec = dataset_prec.tp.sel(lat=slice(latS,latN), lon=slice(lonW, lonE)) * 1000

        rainfall = slice_prec.sum(dim='time')

        # plotting:
        title = f'Accumulated Precipitation of {label} \n between {initial_day} and {final_day}' 
        fig_name = f'Accumulated_Precipitation_{label}_{initial_day}_{final_day}'
        total_acc_prec(rainfall, lat_data, lon_data, lim_min=0, lim_max=600, 
                       num_points=50, title=title, figname=fig_name)

        #with native resolution:
        # dataset = xr.open_dataset(data_path).rename({'valid_time': 'time', 'latitude': 'lat', 'longitude': 'lon'})

        # dataset_prec = (dataset.assign_coords(lon=((dataset.lon + 180) % 360) - 180).sortby('lon')).sel(time=slice(initial_day,final_day))
        
        # lat_data = dataset_prec.lat.sel(lat=slice(latN,latS))
        # lon_data = dataset_prec.lon.sel(lon=slice(lonW,lonE))

        # slice_prec = dataset_prec.tp.sel(lat=slice(latN,latS), lon=slice(lonW, lonE)) * 1000

        # rainfall = slice_prec.sum(dim='time')

        # # plotting:
        # title = f'Accumulated Precipitation of {label} \n between {initial_day} and {final_day} \n Native Resolution' 
        # fig_name = f'Accumulated_Precipitation_{label}_{initial_day}_{final_day}'
        # total_acc_prec(rainfall, lat_data, lon_data, lim_min=0, lim_max=600, 
        #                num_points=50, title=title, figname=fig_name)

    elif label == 'GPM-IMERG':
        
        # at monan resolution:
        dataset = xr.open_dataset(data_path).rename({'latitude': 'lat', 'longitude': 'lon', 'precipitation': 'rainfall'}).transpose('time', 'lat', 'lon').sel(time=slice(initial_day,final_day))

        lat_data = dataset.lat.sel(lat=slice(latS,latN))
        lon_data = dataset.lon.sel(lon=slice(lonW, lonE))
        
        rainfall = (dataset.rainfall.sel(lat=slice(latS,latN), lon=slice(lonW, lonE))).sum(dim='time')

        # plotting:
        title = f'Accumulated Precipitation of {label} \n between {initial_day} and {final_day}' 
        fig_name = f'Accumulated_Precipitation_{label}_{initial_day}_{final_day}'
        total_acc_prec(rainfall, lat_data, lon_data, lim_min=0, lim_max=600, 
                       num_points=50, title=title, figname=fig_name)

        # at its native resolution:  
        # dataset = xr.open_dataset(data_path).rename({'precipitation': 'rainfall'}).sel(time=slice(initial_day,final_day))

        # lat_data = dataset.lat.sel(lat=slice(latS,latN))
        # lon_data = dataset.lon.sel(lon=slice(lonW, lonE))
        
        # rainfall = (dataset.rainfall.sel(lat=slice(latS,latN), lon=slice(lonW, lonE))).sum(dim='time')
        # rainfall = rainfall.transpose('lat', 'lon')

        # # plotting:
        # title = f'Accumulated Precipitation of {label} \n between {initial_day} and {final_day} \n Native Resolution' 
        # fig_name = f'Accumulated_Precipitation_{label}_{initial_day}_{final_day}'
        # total_acc_prec(rainfall, lat_data, lon_data, lim_min=0, lim_max=600, 
        #                num_points=50, title=title, figname=fig_name)

    elif label == 'GSMaP':

        # at MONAN 30km resolution:
        dataset = xr.open_dataset(data_path).rename({'latitude': 'lat', 'longitude': 'lon', 'precip': 'rainfall'}).transpose('time', 'lat', 'lon').sel(time=slice(initial_day,final_day))
        
        lat_data = dataset.lat.sel(lat=slice(latS,latN))
        lon_data = dataset.lon.sel(lon=slice(lonW, lonE))
        
        rainfall = ((dataset.rainfall).sel(lat=slice(latS,latN), lon=slice(lonW, lonE))).sum(dim='time')

        # plotting:
        title = f'Accumulated Precipitation of {label} \n between {initial_day} and {final_day}' 
        fig_name = f'Accumulated_Precipitation_{label}_{initial_day}_{final_day}'
        total_acc_prec(rainfall, lat_data, lon_data, lim_min=0, lim_max=600, 
                       num_points=50, title=title, figname=fig_name)

        # at GSMaP native resolution:
        # dataset = xr.open_dataset(data_path).rename({'precip': 'rainfall'}).transpose('time', 'lat', 'lon').sel(time=slice(initial_day,final_day))
        # dataset = (dataset.assign_coords(lon=((dataset.lon + 180) % 360) - 180).sortby('lon')).sel(time=slice(initial_day,final_day))

        # lat_data = dataset.lat.sel(lat=slice(latN,latS))
        # lon_data = dataset.lon.sel(lon=slice(lonW, lonE))
        
        # rainfall = ((dataset.rainfall).sel(lat=slice(latN,latS), lon=slice(lonW, lonE))).sum(dim='time')

        # # plotting:
        # title = f'Accumulated Precipitation of {label} \n between {initial_day} and {final_day} \n Native Resolution' 
        # fig_name = f'Accumulated_Precipitation_{label}_{initial_day}_{final_day}'
        # total_acc_prec(rainfall, lat_data, lon_data, lim_min=0, lim_max=600, 
        #                num_points=50, title=title, figname=fig_name)

    elif label == 'NWS':
        # at models' resolution:
        dataset = xr.open_dataset(data_path).rename({'latitude': 'lat', 'longitude': 'lon'}).transpose('time', 'lat', 'lon').sel(time=slice(initial_day,final_day))
        
        lat_data = dataset.lat.sel(lat=slice(latS,latN))
        lon_data = dataset.lon.sel(lon=slice(lonW, lonE))
        
        rainfall = ((dataset.rainfall).sel(lat=slice(latS,latN), lon=slice(lonW, lonE))).sum(dim='time')
        # plotting:
        title = f'Accumulated Precipitation of {label} \n between {initial_day} and {final_day}' 
        fig_name = f'Accumulated_Precipitation_{label}_{initial_day}_{final_day}'
        total_acc_prec(rainfall, lat_data, lon_data, lim_min=0, lim_max=600, 
                       num_points=50, title=title, figname=fig_name)

        # with native grid:
        # dataset = xr.open_dataset(data_path).sel(time=slice(initial_day,final_day))

        # lat_data = dataset.lat.sel(lat=slice(latS,latN))
        # lon_data = dataset.lon.sel(lon=slice(lonW, lonE))
        
        # rainfall = ((dataset.rainfall).sel(lat=slice(latS,latN), lon=slice(lonW, lonE))).sum(dim='time')
        # # plotting:
        # title = f'Accumulated Precipitation of {label} \n between {initial_day} and {final_day}' 
        # fig_name = f'Accumulated_Precipitation_{label}_{initial_day}_{final_day}'
        # total_acc_prec(rainfall, lat_data, lon_data, lim_min=0, lim_max=600, 
        #                num_points=50, title=title, figname=fig_name)



    else:
        # abrindo o dado
        dataset = xr.open_dataset(data_path).rename({'Time': 'time', 'latitude': 'lat', 'longitude': 'lon'}).sel(time=final_day, lat=slice(latS, latN), lon=slice(lonW, lonE))

        # fazendo o recorte de lat e lon
        lat_data = dataset.lat
        lon_data = dataset.lon

        rainfall = dataset.rainnc + dataset.rainc
        
        if label == 'CP-25':
            initial_day = '2024-09-25T00'
        else:
            initial_day = initial_day

        # plotting:
        title = f'Accumulated Precipitation of {label} \n between {initial_day} and {final_day}' 
        fig_name = f'Accumulated_Precipitation_{label}_{initial_day}_{final_day}'
        total_acc_prec(rainfall, lat_data, lon_data, lim_min=0, lim_max=600, 
                       num_points=50, title=title, figname=fig_name)