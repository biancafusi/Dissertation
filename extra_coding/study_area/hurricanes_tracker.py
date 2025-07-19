import tropycal.tracks as tracks
import datetime as dt
import matplotlib.pyplot as plt

'''
READ ME:
        basin =             ”east_pacific”, ”north_atlantic”, ”west_pacific”, ”north_indian”
                            ”south_indian”, ”australia”, ”south_pacific”, ”south_atlantic”, ”all” 
        track_source =      Can be 'hurdat', 'ibtracs' (to get them all) (HURDAT2 by default)
        storm_name =        Is a str of storm name, everything in lowercase letters (dont forget '')
        storm_year =        Number (not a str), such as 2024
        save_nc =           Type 'YES' to save the nc file together, 'NO' to not save
        nc_file_name =      Str name with .nc at the end, for example 'helene.nc'
        plot_save_name =    Str name with .png at the end, for example 'Helene.png'

Obs.: HURDAT data is not available for the most recent hurricane seasons. 
To include the latest data up through today, the “include_btk” 
flag would need to be set to True, which reads in preliminary best track data 
from the NHC website.    

Obs.2: To get this code run, please se how to properly install the tropycal library at 
the link below.

More information: https://tropycal.github.io/tropycal/index.html
Information about each function are describe on: 
https://tropycal.github.io/tropycal/api/generated/tropycal.tracks.TrackDataset.html#tropycal.tracks.TrackDataset
'''

# # namelist:
basin = 'north_atlantic'
track_source = 'ibtracs'
storm_name = 'beryl'
storm_year = 2024
save_nc = 'YES'
nc_file_name = 'Beryl.nc'
plot_save_name = 'Beryl_2024.png'

# Tracker code:

basin = tracks.TrackDataset(basin=basin, source=track_source, include_btk=True)

storm = basin.get_storm((storm_name, storm_year))

# print(storm) # show a preview of the data set (is commented)

basin.plot_storm((storm_name, storm_year)) # this is to plot the path
plt.savefig(plot_save_name)

if save_nc == 'YES':
    storm.to_xarray().to_netcdf(nc_file_name)

storm.plot(prop={'dots':False,'linecolor':'mslp','linewidth':3.0})

legend = plt.gca().get_legend()
if legend:
    legend.set_frame_on(True)
    legend.set_bbox_to_anchor((1, 1))  # move para o canto superior direito (ajustável)
    legend.set_title("Legend")
plt.tight_layout()
plt.savefig("helene_mslp_2024.png", bbox_inches='tight', dpi=300)

storm.plot(prop={'dots':False,'linecolor':'vmax','linewidth':3.0})
plt.savefig('helene_wind_2024.png')