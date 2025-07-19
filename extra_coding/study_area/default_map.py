import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy as np
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

def plot_map_slice(lonW, lonE, latS, latN, save_name, title=None):

    stamen_terrain = cimgt.GoogleTiles(style='satellite')
    fig, ax = plt.subplots(
        figsize=(4.5, 3.5),
        subplot_kw={"projection": stamen_terrain.crs}
    )

    ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree())
    ax.add_image(stamen_terrain, 8)

    ax.set_yticks(np.linspace(latS , latN, 6, dtype=int), crs=ccrs.PlateCarree())
    ax.set_xticks(np.linspace(lonW,lonE,6, dtype=int), crs=ccrs.PlateCarree())
    
    lon_formatter = LongitudeFormatter(number_format='.1f',
                                        degree_symbol='',
                                        dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.1f',
                                        degree_symbol='')

    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)

    if title != None:
        ax.set_title(title, fontsize=10)

    plt.savefig(save_name, dpi=300, bbox_inches="tight")


# lonW, lonE, latS, latN = -100, -90, 25, 35
lonW, lonE, latS, latN = -92, -82, 17.5, 22.5
#lonW, lonE, latS, latN = -66, -56, 8, 18
save_name = 'Yucatan.png'

plot_map_slice(lonW, lonE, latS, latN, save_name, title='A: Yucatán Peninsula')