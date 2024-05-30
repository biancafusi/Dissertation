###########################################
# PYTHON FILE TO 
# DEFINED MULTIPLES PLOT PROJECTION
#USING THE BASEMAP LIBRARY
###########################################

import numpy  as np 

import matplotlib as mpl

import matplotlib.pyplot as plt

from matplotlib.ticker import FormatStrFormatter, ScalarFormatter

from   source.plotparameters import *


import cartopy.crs as ccrs

import cartopy.feature as cf

from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

#from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.feature import NaturalEarthFeature

#used the user parameter to plot(plotparameter.py)

mpl.rcParams.update(params)


def cartopy1(data,lats,lons,b1=100,b2=100,nn=10,plotname='',figname='',color='RdBu_r',out='',cbar=True):

    if b1==b2 and b1==100:

        b1=np.min(data[:])
        b2=np.max(data[:])
        
    #projection=ccrs.Robinson(central_longitude=180.0, globe=None)
    projection=ccrs.PlateCarree(central_longitude=180.0, globe=None)

    #fig = plt.figure()
    fig = plt.figure(figsize=(4,3))

    ax  = fig.add_subplot(1, 1, 1, projection=projection)

    # make the map global rather than have it zoom in to
    # the extents of any plotted data
    ax.set_global()
    ax.stock_img()
    ax.coastlines()

    ax.gridlines(draw_labels=False)
    #ax.xlabel_style = {'size': 6, 'color': 'red'}
    #xlabel_style = {'color': 'red', 'weight': 'bold'}
    #ax.tick_params(axis='both', labelsize=8)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)


    levels= np.linspace(b1,b2,nn,endpoint=True)


    #filled=ax.contourf(lons, lats, data,levels=levels,
    #            transform=ccrs.PlateCarree(),
    #            cmap='RdBu_r')

    filled=ax.contourf(data.longitude.values, data.latitude.values, data.values, levels=levels,
                transform=ccrs.PlateCarree(),
                #cmap='coolwarm',alpha=1.0)
                #cmap='Spectral_r',alpha=1.0)
                #cmap='RdYlBu_r',alpha=1.0)
                cmap=color,alpha=1.3,extend='both')

    #lines  = ax.contour(lons, lats, data, levels=filled.levels,
    #                    colors=['black'] ,alpha=0.5,linewidths=0.5,
    #                    transform=ccrs.PlateCarree())
    lines  = ax.contour(lons, lats, data, levels=filled.levels,
                        colors=['black'] ,alpha=0.5,linewidths=0.5,
                        transform=ccrs.PlateCarree())

    ax.set_xticks([-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
    ax.set_yticks([-78.5, -60, -25.5, 25.5, 60, 80], crs=ccrs.PlateCarree())



    lon_formatter = LongitudeFormatter(number_format='.1f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.1f',
                                      degree_symbol='')
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    # Add a colorbar for the filled contour.
    #fig.colorbar(filled, orientation='horizontal',shrink=0.5)

    if cbar: 
        CB=fig.colorbar(filled, orientation='vertical',shrink=0.5)
        #ax.set_xlim(data[ni],data[nf])
        #ax.set_ylim([nv1,nv2])
        cbarlabels = np.linspace(b1,b2,11,endpoint=True)
        CB.set_ticks(cbarlabels[::2])

    # Use the line contours to place contour labels.
    #ax.clabel(
    #    lines,  # Typically best results when labelling line contours.
    #    colors=['black'],
    #    manual=False,  # Automatic placement vs manual placement.
    #    inline=True,  # Cut the line where the label will be placed.
    #    fmt=' {:.0f} '.format,  # Labes as integers, with some extra space.
    #)


    ax.set_title("%s"%(plotname),fontsize=8)

    fig.savefig('%s%s.pdf'%(out,figname),bbox_inches='tight', format='pdf', dpi=200)
	       
    return fig     

def cartopy_amazon(data,lats,lons,nn=2,plotname='',figname='',color='',out='',cbar=True):

    #if b1==b2 and b1==100:

     #   b1=np.min(data[:])
     #   b2=np.max(data[:])
     
    b1 = round(data.min().item(), 1)
    b2 = round(data.max().item(), 1)

    print(f'b1:{b1}')
    print(f'b2:{b2}')


    projection=ccrs.PlateCarree(central_longitude=180.0, globe=None)

    fig = plt.figure(figsize=(4,3))

    ax  = plt.axes(projection=projection)
    
    #levels= np.linspace(b1, b2, nn, endpoint=True)
    levels = np.linspace(0, 20, 5)
    filled=ax.contourf(lons.values, lats.values, data.values, levels=levels,
                transform=ccrs.PlateCarree(),
                #cmap='coolwarm',alpha=0.9)
                #cmap='Spectral_r',alpha=1.0)
                #cmap='RdYlBu_r',alpha=1.0)
                cmap=color,alpha=1.0,extend='both') 
                   
    #lines  = ax.contour(lons, lats, data, levels=filled.levels,
    #                    colors=['black'] ,alpha=0.3,linewidths=0.05,
    #                    transform=ccrs.PlateCarree())
    
    ax.add_feature(cf.COASTLINE,alpha=0.4)
    ax.add_feature(cf.BORDERS,alpha=0.4)
    ax.add_feature(cf.LAND,alpha=0.4)
    ax.add_feature(cf.STATES,alpha=0.4)
    ax.add_feature(cf.OCEAN,alpha=0.4)
    ax.stock_img()
    
    ax.set_extent([-69, -45, -9, 8])

# ax.set_extent: Aqui se define as lat lon visiveis no plot

    ax.set_yticks(range(-9,10,3), crs=ccrs.PlateCarree())
    ax.set_xticks(range(-69,-44,6), crs=ccrs.PlateCarree())
    
    lon_formatter = LongitudeFormatter(number_format='.1f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.1f',
                                      degree_symbol='')
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)   
    
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
   
    if cbar: 
        CB=fig.colorbar(filled, orientation='horizontal',shrink=0.5)
        #ax.set_xlim(data[ni],data[nf])
        #ax.set_ylim([nv1,nv2])
        cbarlabels = np.linspace(0,b2,1,endpoint=True)
        CB.ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        CB.ax.tick_params(labelsize=5)
        CB.set_label(label='mm/h',loc='center',  fontsize=5)
        CB.set_ticks(cbarlabels[::2])

    ax.set_title("%s"%(plotname),fontsize=8)

    fig.savefig('%s%s.pdf'%(out,figname),bbox_inches='tight', format='pdf', dpi=200)
	       
    return fig 


def cartopy_f(data,lats,lons,b1=100,b2=100,nn=10,plotname='',figname='',color='RdBu_r',out='',cbar=True):

    if b1==b2 and b1==100:

        b1=np.min(data[:])
        b2=np.max(data[:])
        
    #projection=ccrs.Robinson(central_longitude=180.0, globe=None)
    projection=ccrs.PlateCarree(central_longitude=180.0, globe=None)

    #fig = plt.figure()
    fig = plt.figure(figsize=(4,3))

    ax  = fig.add_subplot(1, 1, 1, projection=projection)

    # make the map global rather than have it zoom in to
    # the extents of any plotted data
    #ax.set_global()
    #ax.stock_img()
    ax.coastlines()

    ax.gridlines(draw_labels=False)
    #ax.xlabel_style = {'size': 6, 'color': 'red'}
    #xlabel_style = {'color': 'red', 'weight': 'bold'}
    #ax.tick_params(axis='both', labelsize=8)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)


    levels= np.linspace(b1,b2,nn,endpoint=True)


    #filled=ax.contourf(lons, lats, data,levels=levels,
    #            transform=ccrs.PlateCarree(),
    #            cmap='RdBu_r')


    filled=ax.contourf(lons.values, lats.values, data.values, levels=levels,
                transform=ccrs.PlateCarree(),
                #cmap='coolwarm',alpha=1.0)
                #cmap='Spectral_r',alpha=1.0)
                #cmap='RdYlBu_r',alpha=1.0)
                cmap=color,alpha=1.0,extend='both')

    #lines  = ax.contour(lons, lats, data, levels=filled.levels,
    #                    colors=['black'] ,alpha=0.5,linewidths=0.5,
    #                    transform=ccrs.PlateCarree())
    lines  = ax.contour(lons, lats, data, levels=filled.levels,
                        colors=['black'] ,alpha=0.5,linewidths=0.5,
                        transform=ccrs.PlateCarree())

    #ax.set_extent([260, 340, -60, 20])

    ax.set_xticks([-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
    ax.set_yticks([-78.5, -60, -25.5, 10], crs=ccrs.PlateCarree())



    lon_formatter = LongitudeFormatter(number_format='.1f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.1f',
                                      degree_symbol='')
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    # Add a colorbar for the filled contour.
    #fig.colorbar(filled, orientation='horizontal',shrink=0.5)

    if cbar: 
        CB=fig.colorbar(filled, orientation='vertical',shrink=0.5)
        #ax.set_xlim(data[ni],data[nf])
        #ax.set_ylim([nv1,nv2])
        cbarlabels = np.linspace(b1,b2,11,endpoint=True)
        CB.set_ticks(cbarlabels[::2])

    # Use the line contours to place contour labels.
    #ax.clabel(
    #    lines,  # Typically best results when labelling line contours.
    #    colors=['black'],
    #    manual=False,  # Automatic placement vs manual placement.
    #    inline=True,  # Cut the line where the label will be placed.
    #    fmt=' {:.0f} '.format,  # Labes as integers, with some extra space.
    #)


    ax.set_title("%s"%(plotname),fontsize=8)

    fig.savefig('%s%s.pdf'%(out,figname),bbox_inches='tight', format='pdf', dpi=200)


	       
    return fig     

def cartopy_sudeste(data,lats,lons,b1=100,b2=100,nn=10,plotname='',figname='fig1',out=''):


    gray_cmap = mpl.cm.get_cmap('gray', 120)                            # Read the reversed 'gray' cmap
    gray_cmap = gray_cmap(np.linspace(0, 1, 120))                     # Create the array
    colors = ["#ffa0ff", "#0806ff", "#3bcfff", "#feff65", "#ff7516"]  # Custom colors
    my_colors = mpl.cm.colors.ListedColormap(colors)                      # Create a custom colormap
    my_colors = my_colors(np.linspace(0, 1, 50))                      # Create the array
    gray_cmap[70:120, :] = my_colors                                     # Join both cmaps arrays

    my_cmap1 = mpl.cm.colors.ListedColormap(gray_cmap)
    my_cmap2 = mpl.cm.colors.ListedColormap(gray_cmap)


    if b1==b2 and b1==100:

        b1=np.min(data[:])
        b2=np.max(data[:])
        
    #projection=ccrs.Robinson(central_longitude=180.0, globe=None)
    projection=ccrs.PlateCarree(central_longitude=180.0, globe=None)

    fig = plt.figure(figsize=(3,2))

    ax  = fig.add_subplot(1, 1, 1, projection=projection)

    ax.tick_params(axis='x', labelsize=7)
    ax.tick_params(axis='y', labelsize=7)

    # make the map global rather than have it zoom in to
    # the extents of any plotted data
    ax.set_global()
    ax.stock_img()
    ax.coastlines()
    ax.gridlines(draw_labels=False)

    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)

    #Contries
    ax.add_feature(cfeature.BORDERS, linestyle='-', alpha=0.80,facecolor='none')

    ax.add_feature(cfeature.LAKES, edgecolor='navy',alpha=0.80,facecolor='none')

    ax.add_feature(cfeature.RIVERS, edgecolor='navy',alpha=0.80,facecolor='none')

    #MOMO STATES
    #ax.add_feature(cfeature.STATES.with_scale('50m'))


    states = cfeature.NaturalEarthFeature(category='cultural', scale='50m', facecolor='none', name='admin_1_states_provinces_lines')

    ax.add_feature(states, edgecolor='black',alpha=1.0,linestyle='-', linewidth=1)


    ax.set_extent([260, 340, -60, 20])

    ax.set_xticks([260, 280,300,320,340], crs=ccrs.PlateCarree())
    ax.set_yticks([ -60,-40, -20.0, 0, 20.0], crs=ccrs.PlateCarree())


    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)


    levels= np.linspace(b1,b2,nn,endpoint=True)


    #filled=ax.contourf(lons, lats, data,levels=levels,
    #            transform=ccrs.PlateCarree(),
    #            cmap='RdBu_r')

    #filled=ax.contourf(lons, lats, data,levels=levels,
    #            transform=ccrs.PlateCarree(),
    #            cmap=my_cmap2)

    #filled=ax.contourf(lons, lats, data,levels=levels,
    #            transform=ccrs.PlateCarree(),
    #            cmap='Greys_r')
    filled=ax.contourf(lons, lats, data,levels=levels,
                transform=ccrs.PlateCarree(),
                cmap='rainbow',alpha=1.0)


    img = plt.imread('bluemarble.png')

    img_extent = (-180, 180, -90, 90)

    ax.imshow(img, origin='upper', extent=img_extent, transform=ccrs.PlateCarree())


    #lines  = ax.contour(lons, lats, data, levels=filled.levels,
    #                    colors=['black'] ,alpha=0.5,linewidths=0.5,
    #                    transform=ccrs.PlateCarree())


    # Add a colorbar for the filled contour.

    #CB=fig.colorbar(filled, orientation='vertical',shrink=0.5)
    #cbarlabels = np.linspace(b1,b2,11,endpoint=True)
    #CB.set_ticks(cbarlabels[::2])


    ax.set_title("%s"%(plotname),fontsize=5)

    fig.savefig('%s%s.pdf'%(out,figname),bbox_inches='tight', format='pdf', dpi=200)

    return fig

def cartopy_vector(datau,datav,scale=1, width=0.1,data=[0],color='RdBu_r',b1=100,b2=100,nn=10,plotname='',figname='fig1',out='',cbar=True,MPAS=False):


    #try:
    #    data=data.values
    #    datau=datau.values
    #    datav=datav.values
    #    lats=lats.values
    #    lons=lons.values
    #except AttributeError:
    #    data=data
    #    datau=datau
    #    datav=datav
    #    lats=lats
    #    lons=lons

    if MPAS:
       lats=data.lat.values
       lons=data.lon.values
       ulats=datau.lat.values
       ulons=datau.lon.values
    else:
        lats=data.latitude.values
        lons=data.longitude.values
        ulats=datau.latitude.values
        ulons=datau.longitude.values

        
    #projection=ccrs.Robinson(central_longitude=180.0, globe=None)
    projection=ccrs.PlateCarree(central_longitude=180.0, globe=None)

    fig = plt.figure(figsize=(3,2))

    #ax  = fig.add_subplot(1, 1, 1, projection=projection)
    ax  = plt.axes(projection=projection)  # note that I changed the map projection
    
    # make the map global rather than have it zoom in to
    # the extents of any plotted data
    ax.set_global()
    #ax.stock_img()
    
    ax.coastlines( linestyle='-', alpha=1.00,linewidth=1)

    #grid
    ax.gridlines(draw_labels=False)

    ax.tick_params(axis='x', labelsize=7)
    ax.tick_params(axis='y', labelsize=7)

    #ax.add_feature(cfeature.LAND)

    #Contries
    ax.add_feature(cfeature.BORDERS, linestyle='-', alpha=1.00,facecolor='none',linewidth=0.5)

    ax.add_feature(cfeature.LAKES, edgecolor='navy',alpha=1.00,facecolor='none',linewidth=0.5)

    ax.add_feature(cfeature.RIVERS, edgecolor='navy',alpha=1.00,facecolor='none',linewidth=0.5)

    #MOMO STATES
    #ax.add_feature(cfeature.STATES.with_scale('50m'))


    states = cfeature.NaturalEarthFeature(category='cultural', scale='50m', facecolor='none', name='admin_1_states_provinces_lines')

    ax.add_feature(states, edgecolor='black',alpha=1.0,linewidth=0.5)

    #resol = '50m'
    #bodr = cfeature.NaturalEarthFeature(category='cultural', 
    #name='admin_0_boundary_lines_land', scale=resol, facecolor='none', alpha=0.7)
    #ax.add_feature(bodr, linestyle='--', edgecolor='k', alpha=1)
    #plt.show()
    #exit()

    ax.set_extent([260, 340, -60, 20])

    ax.set_xticks([260, 280,300,320,340], crs=ccrs.PlateCarree())
    ax.set_yticks([ -60,-40, -20.0, 0, 20.0], crs=ccrs.PlateCarree())

    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)


    if b1==b2 and b1==100:

        b1=np.min(data[:].values)
        b2=np.max(data[:].values)


    if(len(data)==1):

        data = np.sqrt(datau**2 + datav**2)
        #b1=np.min(datau[:])
        #b2=np.max(datav[:])

    levels= np.linspace(b1,b2,nn,endpoint=True)


    filled=ax.contourf(lons, lats, data.values, levels=levels,
                transform=ccrs.PlateCarree(),
                #cmap='coolwarm',alpha=1.0)
                #cmap='Spectral_r',alpha=1.0)
                #cmap='RdYlBu_r',alpha=1.0)
                cmap=color,alpha=1.0,extend='both')
    #
    #qv = ax.quiver(lons, lats ,datau.values, datav.values, transform=ccrs.PlateCarree(),color='black',scale=800, width=0.002)

    #qv = ax.quiver(lons, lats ,datau.values, datav.values, transform=ccrs.PlateCarree(),color='black',scale=250, width=0.0035)#,headlength=0.05)

    qv = ax.quiver(ulons, ulats ,datau.values, datav.values, transform=ccrs.PlateCarree(),color='black',scale=scale, width=width)#,headlength=0.05)

    #ax.quiverkey(qv, X=1.00, Y=1.10, U=100,label=r'100[kgkg$^{-1}$ms$^{-1}$Pa]', labelpos='E',fontproperties={'size':5})
    ax.quiverkey(qv, X=1.05, Y=1.02, U=100,label=r'100', labelpos='E',fontproperties={'size':5}, labelsep=0.01)
    
    #qv = ax.quiver(lons, lats ,datau.values, datav.values, transform=ccrs.PlateCarree(),color='black',scale=1, width=0.0015)#,headlength=0.05)


    if cbar:
    # Add a colorbar for the filled contour.
        CB=fig.colorbar(filled, orientation='vertical',shrink=0.5)
        cbarlabels = np.linspace(b1,b2,11,endpoint=True)
        CB.set_ticks(cbarlabels[::2])

    ax.set_title("%s"%(plotname),fontsize=6)

    fig.savefig('%s%s.pdf'%(out,figname),bbox_inches='tight', format='pdf', dpi=200)
	       
    return fig,qv     

def barra(color='RdBu_r',b1=100,b2=100,nn=10,plotname='',figname='',out='',label=''):

    if b1==b2 and b1==100:

        b1=np.min(data[:].values)
        b2=np.max(data[:].values)

    levels= np.linspace(b1,b2,nn,endpoint=True)

    fig,ax = plt.subplots(figsize=(4,0.5))
    fig.subplots_adjust(bottom=0.5)

    cmap = color
    norm = mpl.colors.Normalize(vmin=b1, vmax=b2)
    CB=fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),cax=ax, orientation='horizontal',shrink=1.0,extend='both',label=label)
    cbarlabels = np.linspace(b1,b2,11,endpoint=True)

    #CB.set_ticks(cbarlabels[::3])
    #CB.ax.set_title(r'%s'%clabel,fontsize=6)

    #ax.quiverkey(q, X=0.25, Y=0.45, U=500,label=r'[kgkg$^{-1}$ms$^{-1}$Pa]', labelpos='E')


    fig.savefig('%s%s.pdf'%(out,figname),bbox_inches='tight', format='pdf', dpi=100)

def narrow_q(q,plotname='',figname='',out='',label=''):


    fig,ax = plt.subplots(figsize=(8,0.5))
    #fig.subplots_adjust(bottom=0.5)

    ax.quiverkey(q, X=0.25, Y=0.45, U=500,label=r'[kgkg$^{-1}$ms$^{-1}$Pa]', labelpos='E')


    fig.savefig('%s%s.pdf'%(out,figname),bbox_inches='tight', format='pdf', dpi=100)
	       
    return fig     

    
