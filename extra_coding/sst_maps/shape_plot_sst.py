import numpy  as np 
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, ScalarFormatter, MaxNLocator, FuncFormatter
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib

matplotlib.use("Agg")


def beryl_sst(data, lats, lons, lim_min='', lim_max='', num_points='', title='', figname='', out='', cbar=True, unit='mm/h'):

    lonW, lonE, latS, latN = -106, -50, 10, 40


    largura_fig = 7 #polegadas
    altura_fig = 4 #polegadas

    b1 = lim_min
    b2 = lim_max
    
    projection=ccrs.PlateCarree(central_longitude=180.0, globe=None)
    
    fig = plt.figure(figsize=(largura_fig, altura_fig))
    ax  = plt.axes(projection=projection)

    #clr = ['#fdfdfd','#b0d0fb','#4290f9','#25eb2e','#f79f48','#ffc300','#ff5733', '#ff0000','#800080']
    #clr = ['#FFFFFF', '#C7E1FF', '#8FCBFF', '#57B4FF', '#1F9EFF', '#0080FF', '#00B366', '#66E600', '#B3FF00', '#b3ff00','#e6d800','#FF9900', '#FF3300','#CC00CC']
    # clr =['#FFFFFF', '#C9E5FF', '#93CCFF', '#5EB2FF', '#2899FF', '#007FFF', '#0080B3', '#008066', \
    # '#00801A', '#1AB319','#33E619', '#80FF00', '#B3FF00', '#E6FF00', '#FFFF00', '#FFCC00', '#FF9900', \
    # '#FF6600', '#FF3300', '#FF0000','#CC00CC', '#9900CC', '#6600CC', '#3300CC', '#0000CC']
    # colors = [
    # "#FFFFFF", "#E8F6FA", "#D1EEF5", "#B9E6F0", "#A2DEEB", "#8BD6E6", # Tons de azul claro
    # "#75BED1", "#60A7BC", "#4A8FA7", "#357892", "#21627D",            # Azul escuro
    # "#32CD32", "#3D9E0F", "#40A511",            # Tons de verde
    # "#FFFF00", "#FFD700", "#FFA500", "#FF8C00", "#FF4500",            # Tons de amarelo/laranja
    # "#FF6347", "#FF0000", "#B22222", "#8B0000",                       # Vermelho intenso
    # "#800080",  "#4B0082", '#641405'             # Roxo a preto                       # Roxo a preto
    # ]
    #colors = [
    #     '#FFFFFF', '#ADD8E6', '#90EE90', '#FFDAB9', '#FFB6C1','#DDA0DD', '#A9A9A9'
    # ]
    # new_labels = [0.1, 0.5, 1, 1.5, 2, 4, 6, 8, 10, 12, 15, 18, 21, 25]
    # new_labels = np.arange(100,400,50)
    new_labels = np.arange(18,35,1)

    # new_pal = mcolors.LinearSegmentedColormap.from_list("custom",colors,N=len(new_labels))
    # new_pal = mcolors.LinearSegmentedColormap.from_list("custom",colors,N=len(new_labels))

    colors =['darkblue', 'palegreen', 'yellow', 'red']
    new_pal = mcolors.LinearSegmentedColormap.from_list("custom",colors,N=30)
    norm = mcolors.BoundaryNorm(boundaries=new_labels,ncolors=new_pal.N,clip=True)
    
    levels= new_labels
    # filled=ax.contourf(lons.values, lats.values, data.values, levels=levels,
    #             transform=ccrs.PlateCarree(),
    #             cmap=new_pal,alpha=0.95,extend='both',norm=norm
    #             )
    filled=ax.contourf(lons.values, lats.values, data.values, levels=levels,
            transform=ccrs.PlateCarree(),
            cmap=new_pal,alpha=0.95,extend='both',norm=norm
            )

    ax.add_feature(cf.COASTLINE,alpha=0.4,linewidth=0.4,edgecolor='black')
    ax.add_feature(cf.BORDERS,alpha=0.4,linewidth=0.4)
    ax.add_feature(cf.LAND,alpha=0.4,linewidth=0.4)
    ax.add_feature(cf.STATES,alpha=0.4,linewidth=0.2)
    ax.add_feature(cf.OCEAN,alpha=0.4,linewidth=0.3)
    ax.stock_img()

    ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree()) #lonW lonE latS latN
    ax.set_adjustable('box')
    ax.set_aspect('auto')
    

    max_value = np.max(data)
    ax.text(116,39,f'Max Value: {max_value:.2f}', ha='left', va='top', fontsize=8, bbox=dict(boxstyle='square',
                    edgecolor='black', facecolor='white'))
    
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

    ax.set_title("%s"%(title),fontsize=8)

    fig.savefig('%s%s.png'%(out,figname), format='png',dpi=300,bbox_inches='tight')

    return fig