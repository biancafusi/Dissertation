import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as mcolors
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib

matplotlib.use("Agg")

from namelist_for_acc import *

'''
WORKING - REVIEWED MAR 11
'''

# Plot:

if label_data == 'ERA5':
    
    if convertion_to_180 != 'ON':
        print('DEVELOPING ...')

    elif convertion_to_180 == 'ON':
        dataset_prec = xr.open_dataset(name_file_prec)
        dataset_dry = xr.open_dataset(name_file_dry)

        dataset_prec    = dataset_prec.assign_coords(longitude=((dataset_prec.longitude + 180) % 360) - 180).sortby('longitude')
        dataset_dry     = dataset_dry.assign_coords(longitude=((dataset_dry.longitude + 180) % 360) - 180).sortby('longitude')

        lats = dataset_prec.latitude.sel(latitude=slice(latN, latS))
        lons = dataset_prec.longitude.sel(longitude=slice(lonW,lonE))

        slice_prec = dataset_prec.tp.sel(valid_time=slice(initial_day, final_day), latitude=slice(latN, latS), longitude=slice(lonW, lonE)) * 1000

        time = dataset_prec.valid_time.sel(valid_time=slice(initial_day, final_day)).values

        prec_acc = slice_prec.sum(dim='valid_time')


elif label_data == 'GPM':
    dataset_prec = xr.open_dataset(name_file_prec)

    lats = dataset_prec.latitude.sel(latitude=slice(latS,latN))
    lons = dataset_prec.longitude.sel(longitude=slice(lonW,lonE))

    slice_prec = dataset_prec.precipitation.sel(time=slice(initial_day, final_day), latitude=slice(latS,latN), longitude=slice(lonW, lonE))

    time = dataset_prec.time.sel(time=slice(initial_day, final_day)).values

    prec_acc = slice_prec.sum(dim='time')

    prec_acc = prec_acc.transpose('latitude','longitude')

else:

    # abrindo o dado
    dataset_prec = xr.open_dataset(name_file_prec)

    # fazendo o recorte de lat e lon
    lats = dataset_prec.latitude.sel(latitude=slice(latS,latN))
    lons = dataset_prec.longitude.sel(longitude=slice(lonW,lonE))

    # fazendo o recorte no último tempo de rodada, ou seja
    # precisa ser a file que já está com a precipitação acumulada 'only_precip'
    slice_prec_rainnc = dataset_prec.rainnc.sel(Time=final_day, latitude=slice(latS,latN), longitude=slice(lonW, lonE))
    slice_prec_rainc = dataset_prec.rainc.sel(Time=final_day, latitude=slice(latS,latN), longitude=slice(lonW, lonE))

    prec_acc = slice_prec_rainnc + slice_prec_rainc

def total_acc_prec(data, lats, lons, lat_points, lon_points, lim_min='', lim_max='', num_points='', title='', figname='', out='', cbar=True, unit='mm/day'):
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

    ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree()) # lonW lonE latS latN
    # ax.set_adjustable('box')
    # ax.set_aspect('auto')

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
    if lon_points and lat_points != 'Nan':
        ax.plot(lon_points, lat_points, color='black', linestyle='--', linewidth=0.8, label=label_data, transform=ccrs.PlateCarree())

        # Add a text box at the beginning of the path
        if len(lon_points) > 0 and len(lat_points) > 0:  # Ensure there are points to plot
            ax.text(
                lon_points[0], lat_points[0],  # Coordinates of the starting point
                label_data,  # Text to display
                color='black',  # Text color
                fontsize=8,  # Text size
                # Text box style
                transform=ccrs.PlateCarree()  # Coordinate system
        )

    fig.savefig(where_to_save+'%s%s.png' % (out, figname), format='png', dpi=300, bbox_inches='tight')

    return fig

total_acc_prec(prec_acc/num_days, lats, lons, lat_points='Nan', lon_points='Nan', lim_min=0, lim_max=36, num_points=2, title=title, figname=fig_name)