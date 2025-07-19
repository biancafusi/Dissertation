'''
PLOTS FUNCTIONS
'''

import numpy  as np 
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, ScalarFormatter, MaxNLocator, FuncFormatter
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib

matplotlib.use("Agg")

from namelist import latN, latS, lonE, lonW

def beryl_prec(data, lats, lons, lim_min='', lim_max='', num_div='', title='', figname='', out='', cbar=True, unit='mm/h'):
    
    largura_fig = 7  # polegadas
    altura_fig = 4  # polegadas

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

    new_labels = np.logspace(np.log10(lim_min), np.log10(lim_max), num_div)
    
    new_pal = mcolors.LinearSegmentedColormap.from_list("custom", colors, N=len(new_labels))
    norm = mcolors.BoundaryNorm(boundaries=new_labels, ncolors=new_pal.N, clip=True)
    
    # print(data.values)


    levels = new_labels

    # print(levels)
    # exit()
    filled = ax.contourf(lons.values, lats.values, data.values, levels=levels,
                         transform=ccrs.PlateCarree(),
                         cmap=new_pal, alpha=0.95, extend='both', norm=norm)

    ax.add_feature(cfeature.COASTLINE, alpha=0.4, linewidth=0.4, edgecolor='black')
    ax.add_feature(cfeature.BORDERS, alpha=0.4, linewidth=0.4)
    ax.add_feature(cfeature.LAND, alpha=0.4, linewidth=0.4)
    ax.add_feature(cfeature.STATES, alpha=0.4, linewidth=0.2)
    ax.add_feature(cfeature.OCEAN, alpha=0.4, linewidth=0.3)
    ax.stock_img()

    ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree()) # lonW lonE latS latN

    # max_value = np.max(data)
    # ax.text(110, 39, f'Max Acc. Rain (mm/day): {max_value:.2f}', ha='left', va='top', fontsize=8, bbox=dict(boxstyle='square',
    #                 edgecolor='black', facecolor='white'))
    
    ax.set_yticks(np.arange(latS, latN, 3), crs=ccrs.PlateCarree())
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

    fig.savefig('%s%s.png'%(out,figname),bbox_inches='tight', format='png', dpi=300)
    
    return False

def diff_plot(data, lats, lons, lim_min, lim_max, cb_thicks, title='', figname='', out='', cbar=True, unit=''):
    largura_fig = 7  # polegadas
    altura_fig = 4  # polegadas

    projection = ccrs.PlateCarree(central_longitude=180.0, globe=None)

    fig = plt.figure(figsize=(largura_fig, altura_fig))
    ax = plt.axes(projection=projection)

    colors = [(0, "blue"), (0.5, 'white'), (1, 'red')]
    n_bins = 20
    cmap_name = 'custom_bwr'
    cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

    levels = np.linspace(lim_min, lim_max, n_bins)

    # Aplicando os limites corretamente
    filled = ax.contourf(lons.values, lats.values, data.values, levels=levels, 
                         transform=ccrs.PlateCarree(),
                         cmap=cm, alpha=0.95, extend='both',
                         vmin=lim_min, vmax=lim_max)  # Agora lim_min e lim_max controlam o colorbar

    ax.add_feature(cfeature.COASTLINE, alpha=0.4, linewidth=0.4, edgecolor='black')
    ax.add_feature(cfeature.BORDERS, alpha=0.4, linewidth=0.4)
    ax.add_feature(cfeature.LAND, alpha=0.4, linewidth=0.4)
    ax.add_feature(cfeature.STATES, alpha=0.4, linewidth=0.2)
    ax.add_feature(cfeature.OCEAN, alpha=0.4, linewidth=0.3)
    ax.stock_img()

    ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree())
    ax.set_adjustable('box')
    ax.set_aspect('auto')

    ax.set_yticks(np.arange(latS, latN, 5), crs=ccrs.PlateCarree())
    ax.set_xticks(np.linspace(lonW, lonE, 9, dtype=int), crs=ccrs.PlateCarree())

    lon_formatter = LongitudeFormatter(number_format='.1f', degree_symbol='', dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.1f', degree_symbol='')

    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=6)

    if cbar:
        CB = fig.colorbar(filled, orientation='vertical', shrink=0.65, aspect=20)
        CB.set_ticks(np.linspace(lim_min, lim_max, 20))  # Define os ticks manualmente
        CB.ax.tick_params(labelsize=6)
        CB.set_label(label=unit, loc='center', fontsize=6, rotation=90)

    fig.tight_layout()  # Agora com os parênteses para evitar a faixa branca

    ax.set_title("%s" % (title), fontsize=8)
    fig.savefig('%s%s.png' % (out, figname), format='png', dpi=300, bbox_inches='tight')

    return fig


def beryl_heat_plot(data, lats, lons, lim_min='', lim_max='', num_points='', title='', figname='', out='', cbar=True, unit='mm/h'):

    largura_fig = 7 #polegadas
    altura_fig = 4 #polegadas

    b1 = lim_min
    b2 = lim_max
    
    projection=ccrs.PlateCarree(central_longitude=180.0, globe=None)
    
    fig = plt.figure(figsize=(largura_fig, altura_fig))
    ax  = plt.axes(projection=projection)

    colors = [
    "#FFFFFF", "#E8F6FA", "#D1EEF5", "#B9E6F0", "#A2DEEB", "#8BD6E6", # Tons de azul claro
    "#75BED1", "#60A7BC", "#4A8FA7", "#357892", "#21627D",            # Azul escuro
    "#32CD32", "#3D9E0F", "#40A511",            # Tons de verde
    "#FFFF00", "#FFD700", "#FFA500", "#FF8C00", "#FF4500",            # Tons de amarelo/laranja
    "#FF6347", "#FF0000", "#B22222", "#8B0000",                       # Vermelho intenso
    "#800080",  "#4B0082", '#641405'             # Roxo a preto                       # Roxo a preto
    ]

    new_labels = np.arange(-50,1000,100)

    new_pal = mcolors.LinearSegmentedColormap.from_list("custom",colors,N=len(new_labels))

    norm = mcolors.BoundaryNorm(boundaries=new_labels,ncolors=new_pal.N,clip=True)
    
    levels= new_labels
    filled=ax.contourf(lons.values, lats.values, data.values, levels=levels,
                transform=ccrs.PlateCarree(),
                cmap=new_pal,alpha=0.95,extend='both',norm=norm
                )

    ax.add_feature(cfeature.COASTLINE, alpha=0.4, linewidth=0.4, edgecolor='black')
    ax.add_feature(cfeature.BORDERS, alpha=0.4, linewidth=0.4)
    ax.add_feature(cfeature.LAND, alpha=0.4, linewidth=0.4)
    ax.add_feature(cfeature.STATES, alpha=0.4, linewidth=0.2)
    ax.add_feature(cfeature.OCEAN, alpha=0.4, linewidth=0.3)
    ax.stock_img()

    ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree()) #lonW lonE latS latN
    ax.set_adjustable('box')
    ax.set_aspect('auto')

    # max_value = np.max(data)
    # ax.text(116,39,f'Max Value: {max_value:.2f}', ha='left', va='top', fontsize=8, bbox=dict(boxstyle='square',
    #                 edgecolor='black', facecolor='white'))
    
    ax.set_yticks(np.arange(latS , latN, 5), crs=ccrs.PlateCarree())
    ax.set_xticks(np.linspace(lonW,lonE,9,dtype=int), crs=ccrs.PlateCarree())
   
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
        
    fig.tight_layout

    ax.set_title("%s"%(title)+' '+r'$\mathregular{(W/m^2)}$',fontsize=8)

    fig.savefig('%s%s.png'%(out,figname), format='png',dpi=300,bbox_inches='tight')

    return fig