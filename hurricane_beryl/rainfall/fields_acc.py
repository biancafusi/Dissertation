import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as mcolors
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from namelist_for_acc import *
import matplotlib

matplotlib.use("Agg")

'''
NOT WORKING!
'''

dataset = xr.open_dataset(name_file_prec)

if label_data == 'ERA5':
    lats = dataset.latitude.sel(latitude=slice(latN, latS))
    lons = dataset.longitude.sel(longitude=slice(lonW, lonE))

    slice_prec = dataset.tp.sel(valid_time=slice(initial_day, final_day), latitude=slice(latN, latS), longitude=slice(lonW, lonE)) * 1000

    time = dataset.valid_time.sel(valid_time=slice(initial_day, final_day)).values

    prec_acc = slice_prec.sum(dim='valid_time')

    MSLP_ERA5 = dataset.msl.sel(latitude=slice(latN, latS), longitude=slice(lonW, lonE)) / 100  # to hPa4
    
    lat_points = []
    lon_points = []
    MSLP_values = []

    for t in range(0, len(time), 1): 
        MSLP_t = MSLP_ERA5.isel(valid_time=t)
        mask = (MSLP_t.values == np.min(MSLP_t.values))
        lat_t, lon_t = np.meshgrid(lats, lons, indexing='ij')
        valid_mask = (lat_t <= 40) & (lon_t > -97) & mask
        lat_points.extend(lat_t[valid_mask].ravel())  
        lon_points.extend(lon_t[valid_mask].ravel()) 
        MSLP_values.extend(MSLP_t.values[valid_mask].ravel())

    lat_points = np.array(lat_points)
    lon_points = np.array(lon_points)
    MSLP_values = np.array(MSLP_values)

elif label_data != 'ERA5' and label_data != 'GPM':
    
    lats = dataset.latitude.sel(latitude=slice(latS,latN))
    lons = dataset.longitude.sel(longitude=slice(lonW,lonE))


    dataset_cut = dataset.sel(Time=final_day,
                              latitude=slice(latS,latN),
                              longitude=slice(lonW,lonE))
    prec1 = dataset_cut.rainc
    prec2 = dataset_cut.rainnc
    prec_acc = prec1[:]+prec2[:]

    dataset_hourly = dataset.sel(Time=slice(initial_day,final_day),
                              latitude=slice(latS,latN),
                              longitude=slice(lonW,lonE))
    time = dataset.Time.sel(Time=slice(initial_day, final_day)).values

    MSLP = dataset_hourly.mslp / 100

    lat_points = []
    lon_points = []
    MSLP_values = []

    for t in range(0, len(time), 1): 
        MSLP_t = MSLP.isel(Time=t)
        mask = ((MSLP_t.values == np.min(MSLP_t.values)) & (MSLP_t.values <= 999))
        lat_t, lon_t = np.meshgrid(lats, lons, indexing='ij')
        valid_mask = (lat_t <= 40) & (lon_t > -97) & mask
        lat_points.extend(lat_t[valid_mask].ravel())  
        lon_points.extend(lon_t[valid_mask].ravel()) 
        MSLP_values.extend(MSLP_t.values[valid_mask].ravel())

    lat_points = np.array(lat_points)
    lon_points = np.array(lon_points)
    MSLP_values = np.array(MSLP_values)


elif label_data == 'GPM+NOAA':

    '''
    NEED TO BE CONTINUE
    '''

    dataset = dataset.assign_coords(longitude=((dataset.longitude + 180) % 360) - 180).sortby('longitude')
        
    time1 = dataset.time
    prec1 = dataset.precipitation
    prec = prec1.transpose('time', 'latitude', 'longitude')

    prec_acc = prec.sel(time=slice(initial_day,final_day),
                              latitude=slice(latN,latS),
                              longitude=slice(lonW,lonE))
        
    lat = prec_acc.latitude
    lon = prec_acc.longitude
    



def total_acc_prec(data, lats, lons, lat_points, lon_points, lim_min='', lim_max='', num_points='', title='', figname='', out='', cbar=True, unit='mm/day'):
    '''Plots the total accumulated rain within a period with the storm path.'''

    lonW, lonE, latS, latN = -106, -50, 10, 41

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

    ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree())

    max_value = np.max(data)
    ax.text(110, 39, f'Max Acc. Rain (mm/day): {max_value:.2f}', ha='left', va='top', fontsize=8, bbox=dict(boxstyle='square',
                    edgecolor='black', facecolor='white'))
    
    ax.set_yticks(np.arange(latS, latN, 5), crs=ccrs.PlateCarree())
    ax.set_xticks(np.linspace(lonW, lonE, 9, dtype=int), crs=ccrs.PlateCarree())
   
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
    ax.plot(lon_points, lat_points, color='black', linestyle=':', linewidth=1.0, label=label_data, transform=ccrs.PlateCarree())

    ax.text(
        lon_points[0], lat_points[0],  # Coordinates of the starting point
        label_data,  # Text to display
        color='black',  # Text color
        fontsize=8,  # Text size
            # Text box style
        transform=ccrs.PlateCarree()  # Coordinate system
    )

    fig.savefig('%s%s.png' % (out, figname), format='png', dpi=300, bbox_inches='tight')

    return fig

total_acc_prec(prec_acc/num_days, lats, lons, lat_points, lon_points, lim_min=0, lim_max=36, num_points=2, title=title, out=where_to_save, figname=fig_name)