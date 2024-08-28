###########################################
# PYTHON FILE TO 
# DEFINED MULTIPLES PLOT PROJECTION
#USING THE BASEMAP LIBRARY
###########################################

import numpy  as np 

import matplotlib as mpl

import matplotlib.pyplot as plt

#from  read_ncfiles import ncdump

#To import the library necessary to make the maps 

from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid

from source.plotparameters import *

from Parameters import out_folder 

import cartopy.crs as ccrs


#used the user parameter to plot(plotparameter.py)
mpl.rcParams.update(params)


def plot_own_cyli(datatoplot,lats,lons,plotname,figname):

    #open figure 
    fig = plt.figure() 

    #Adjust the location of the interior of the figgure 
    fig.subplots_adjust(left=0., right=1., bottom=0., top=0.9) # Setup the map. See http://matplotlib.org/basemap/users/mapsetup.html # for other projections.  #proj = ccrs.PlateCarree() 
	#proj = 'moll'
	
    proj  = 'cyl'
    #proj  = 'moll'
    #proj  = 'robin'
    
    #Define latitudes to plot (-90,90)
    
    lat_i =  -90 
    lat_f =   90
    
    #Define longitudes  to plot (0,360)
    lon_i =   0 
    lon_f =   360
    
    m = Basemap(projection=proj, llcrnrlat=lat_i, urcrnrlat=lat_f,\
                llcrnrlon=lon_i, urcrnrlon=lon_f, resolution='c', lon_0=0)
    
    #m = Basemap(projection='moll', llcrnrlat=-90, urcrnrlat=90,\
    #            llcrnrlon=0, urcrnrlon=360, resolution='c', lon_0=0)
    
    m.drawcoastlines()
    m.drawmapboundary()
    m.drawcountries()
    m.drawparallels(np.arange(-60.,60.,30.),labels=[1,0,0,0]) # draw parallels
    m.drawmeridians(np.arange(0,360.,60.)  ,labels=[0,0,0,1]) # draw meridians
    
    # Make the plot continuous
    #air_cyclic, lons_cyclic = addcyclic(datatoplot, lons)

    # Shift the grid so lons go from -180 to 180 instead of 0 to 360.
    #air_cyclic, lons_cyclic = shiftgrid(180.,air_cyclic, lons_cyclic, start=False)

    #air_cyclic, lons_cyclic = shiftgrid(180.,datatoplot, lons, start=False)

    # Create 2D lat/lon arrays for Basemapnc_f = './air.sig995.2012.nc'  # Your filename
    #lon2d, lat2d = np.meshgrid(lons_cyclic, lats)
    lon2d, lat2d = np.meshgrid(lons, lats)
    # Transforms lat/lon into plotting coordinates for projection
    x, y = m(lon2d, lat2d)
    
    #numero de contornos
    # Plot of air temperature with 11 contour intervals
    ncon = np.linspace(15200, 16800, 41, endpoint=True)


    #cs = m.contourf(x, y, datatoplot,  cmap=plt.cm.Spectral_r)
    cs = m.contourf(x, y, datatoplot,  cmap='RdBu_r')

    #cs = m.contourf(x, y, air_cyclic, ncon, cmap=plt.cm.Spectral_r)

    cbar = plt.colorbar(cs,ticks=ncon[::10], orientation='horizontal', shrink=0.5)

    #cbar = plt.colorbar(cs, orientation='horizontal', shrink=0.5)


    #cbar.set_label("%s (%s)" % (nc_fid.variables['air'].var_desc,\
    #                            nc_fid.variables['air'].units))
    #plt.title("%s on %s" % (nc_fid.variables['air'].var_desc, cur_time))
    plt.title("%s"%(plotname))
    
    
    plt.savefig('%s/%s.pdf'%(out_folder,figname),bbox_inches='tight', format='pdf', dpi=1000)
    
    #media de cada estacao 
    #media anual 
    #plt.show()
    
    return fig

def plot_own_robin(datatoplot,lats,lons,plotname,figname):

    #open figure 
    fig = plt.figure() 

    fig.subplots_adjust(left=0., right=1., bottom=0., top=0.9) 

    proj  = 'robin'
    
    #Define latitudes to plot (-90,90)

    lat_i =  -60 
    lat_f =   60
    
    #Define longitudes  to plot (0,360)
    lon_i = 00 
    lon_f = 360
   
    
    #datatoplot, lons = shiftgrid(180,datatoplot, lons, start=False)

        
    #unico que funcionou, pq nao sei, nao da para botar 
    #o brasil no meio do mapa!!
    m = Basemap(projection=proj, llcrnrlat=lat_i, urcrnrlat=lat_f,\
                llcrnrlon=lon_i, urcrnrlon=lon_f, resolution='c', lon_0=-180,lat_0=0)
    
    
    m.drawcoastlines()
    m.drawmapboundary()
    m.drawcountries()
    m.drawparallels(np.arange(-30.,30.,30.),labels=[1,0,0,0]) # draw parallels
    m.drawmeridians(np.arange(-180,180.,60.)  ,labels=[0,0,0,1]) # draw meridians

    air_cyclic=datatoplot
    lons_cyclic=lons

    lon2d, lat2d = np.meshgrid(lons_cyclic, lats)

    # Transforms lat/lon into plotting coordinates for projection
    x, y = m(lon2d, lat2d)
    
    #numero de contornos
    # Plot of air temperature with 11 contour intervals

    ncon = np.linspace(15200, 16800, 41, endpoint=True)

    cs = m.contourf(x, y, air_cyclic, ncon, cmap=plt.cm.Spectral_r)

    cbar = plt.colorbar(cs,ticks=ncon[::2], orientation='horizontal', shrink=0.5)

    plt.title("%s"%(plotname))
    
    plt.savefig("%s/%s.pdf"%(out_folder,figname),bbox_inches='tight', format='pdf', dpi=1000)
    
    return fig

def plot_own_ortho(datatoplot,lats,lons,plotname,figname):

    #open figure 
    fig = plt.figure() 

    fig.subplots_adjust(left=0., right=1., bottom=0., top=0.9) 

    proj  = 'ortho'
    
    m = Basemap(projection=proj,  resolution='c', lon_0=-60,lat_0=0)
    
    m.drawcoastlines()
    m.drawmapboundary()
    m.drawcountries()
    m.drawparallels(np.arange(-60.,60.,30.),labels=[1,0,0,0]) # draw parallels
    m.drawmeridians(np.arange(-180,180.,60.)  ,labels=[0,0,0,1]) # draw meridians
    
    air_cyclic, lons_cyclic = shiftgrid(180.,datatoplot, lons, start=False)

    lon2d, lat2d = np.meshgrid(lons_cyclic, lats)
    # Transforms lat/lon into plotting coordinates for projection
    x, y = m(lon2d, lat2d)
    
    #numero de contornos
    # Plot of air temperature with 11 contour intervals
    ncon = np.linspace(0.0001, 22, 23, endpoint=True)
    cs = m.contourf(x, y, air_cyclic, ncon, cmap=plt.cm.Spectral_r)

    cbar = plt.colorbar(cs,ticks=ncon[::2], orientation='horizontal', shrink=0.5)

    plt.title("%s"%(plotname))
    
    plt.savefig('%s/%s.pdf'%(out_folder,figname),bbox_inches='tight', format='pdf', dpi=1000)
    
    return fig
	
def plot_temporal(time,variable):

	plt.plot(time,variable)
	plt.title('Average anual temperature in Cachoeira Paulista')
	plt.savefig('iii')
	plt.show()
	return
	
	
#Pedro function
def plot_temporal2(time,constante,timevector,variableft):
	plt.plot(timevector,variableft,'r-')
	plt.plot(time, constante, c='b', marker='o')
	plt.title('Pointer function')
	plt.show()
	return




#Jhonathan function
def plot_temporal3(time,variabel,idex_t):
	plt.plot(time,variabel,'r-')
	plt.plot(time[idex_t], variabel[idex_t], c='b', marker='o')
	plt.title('Pointer function')
	plt.show()
	return

def plot_anom(datatoplot,lats,lons,plotname,figname):

	#3)To plot the medium temperature in Autumm 2012.  ################################################################### #open figure 
    fig = plt.figure() #Adjust the location of the interior of the figgure fig.subplots_adjust(left=0., right=1., bottom=0., top=0.9) # Setup the map. See http://matplotlib.org/basemap/users/mapsetup.html # for other projections.  #proj = ccrs.PlateCarree() 
	#proj = 'moll'
	
    #proj  = 'cyl'
    #proj  = 'moll'
    proj  = 'cyl'
    
    #Define latitudes to plot (-90,90)
    
    lat_i =   -90 
    lat_f =   90
    
    #Define longitudes  to plot (0,360)
    lon_i =  0.0 
    lon_f =  360.0
    
    m = Basemap(projection=proj, llcrnrlat=lat_i, urcrnrlat=lat_f,\
                llcrnrlon=lon_i, urcrnrlon=lon_f, resolution='c', lon_0=0)
    
    #m = Basemap(projection='moll', llcrnrlat=-90, urcrnrlat=90,\
    #            llcrnrlon=0, urcrnrlon=360, resolution='c', lon_0=0)
    
    m.drawcoastlines()
    m.drawmapboundary()
    m.drawcountries()
    m.drawparallels(np.arange(-60.,60.,30.),labels=[1,0,0,0]) # draw parallels
    m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1]) # draw meridians
    
    # Make the plot continuous
    #air_cyclic, lons_cyclic = addcyclic(datatoplot, lons[:])
    # Shift the grid so lons go from -180 to 180 instead of 0 to 360.
    #air_cyclic, lons_cyclic = shiftgrid(180., air_cyclic, lons_cyclic, start=False)
    # Create 2D lat/lon arrays for Basemapnc_f = './air.sig995.2012.nc'  # Your filename
    lon2d, lat2d = np.meshgrid(lons, lats[:])
    # Transforms lat/lon into plotting coordinates for projection
    x, y = m(lon2d, lat2d)
    
    #numero de contornos
    # Plot of air temperature with 11 contour intervals
    ncon = np.linspace(-9, 12, 43, endpoint=True)
    #cs = m.contourf(x, y, datatoplot, ncon, cmap=plt.cm.Spectral_r)
    cs = m.contourf(x, y, datatoplot, ncon, cmap='RdBu')
    #cs = m.contourf(x, y, air_cyclic, 11, cmap='autumn', extend='both')

    cbar = plt.colorbar(cs,ticks=ncon[::4], orientation='vertical', shrink=0.5)
    #cbar.set_label("%s (%s)" % (nc_fid.variables['air'].var_desc,\
    #                            nc_fid.variables['air'].units))
    #plt.title("%s on %s" % (nc_fid.variables['air'].var_desc, cur_time))
    plt.title("%s"%(plotname))
    
    
   # plt.savefig('%s'%(figname), dpi=1000)
    plt.savefig('%s.pdf'%(figname),bbox_inches='tight', format='pdf', dpi=1000)
    #media de cada estacao 
    #media anual 
    #plt.show()
    return fig     
	
#def plot_pointer(time,variable,c,marker)

	
	#return

def cartopy1(datatoplot,lats,lons,plotname,figname):


    #projection=ccrs.Robinson(central_longitude=180.0, globe=None)
    projection=ccrs.PlateCarree(central_longitude=180.0, globe=None)

    fig = plt.figure()

    ax  = fig.add_subplot(1, 1, 1, projection=projection)


    #ax = plt.axes( projection=ccrs.Robinson(central_longitude=180.0, globe=None))

    #fig = plt.figure(figsize=(10, 5))
    #Adjust the location of the interior of the figgure fig.subplots_adjust(left=0., right=1., bottom=0., top=0.9) # Setup the map. See http://matplotlib.org/basemap/users/mapsetup.html # for other projections.  #proj = ccrs.PlateCarree() 
    
    #ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson(central_longitude=180.0, globe=None))
    #ax = fig.add_subplot(1, 1, 1, projection=ccrs.InterruptedGoodeHomolosine())
    #ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude=180.0, globe=None))
    #ax = fig.add_subplot(1, 1, 1, projection=ccrs.TransverseMercator())

    # make the map global rather than have it zoom in to
    # the extents of any plotted data
    ax.set_global()
    ax.stock_img()
    ax.coastlines()

    #to add geodetic
    #ax.plot(-0.08, 51.53, 'o', transform=ccrs.PlateCarree())
    #ax.plot([-0.08, 132], [51.53, 43.17], transform=ccrs.PlateCarree())
    #ax.plot([-0.08, 132], [51.53, 43.17], transform=ccrs.Geodetic())
    ax.contourf(lons, lats, datatoplot,
                transform=ccrs.PlateCarree(),
                #cmap='nipy_spectral')
                cmap='RdBu_r')


    ax.set_title("%s"%(plotname))
    plt.title("%s"%(plotname))

    fig.savefig('%s%s.pdf'%(out_folder,figname),bbox_inches='tight', format='pdf', dpi=1000)
	       
    return fig     
