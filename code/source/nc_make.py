#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
##################################################

Programa para salvar dados em um arquivo NetCdf
Data:18/05/23
por:Jhonatan  A. A. M

##################################################
"""
#Importar bibliotecas a ser usadas 

# biblioteca python para trabalhar com dados  
import datetime as dt  
# Multiplas funções matematica e para trabalhar com vetores no python   
import numpy as np

#Permite ler,criar arquivos Netcdf 
from netCDF4 import Dataset 


#Data de hoje para criação do arquivo 
today = dt.datetime.today()

def savetonc(times,levs,lats,lons,vars,name):

    #Abrindo o novo arquivo nc.
    #Formato: 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', 'NETCDF4'
    
    new_file = Dataset('%s'%(name), 'w', format='NETCDF4')
    new_file.description = "This file contais the u wind \n anomaly from 1978 to 2014 only of the summer period (DJF), winter (j,j,a)"
    
    # Data e criador
    new_file.history     = "Created " + today.strftime("%d/%m/%y")
    new_file.author      = "Jhonatan A. A manco"
    

    #Tamanho do tempo, use np.shape or len()
    dtime      =len(times)
    tamanho_lat=len(lats)
    tamanho_lon=len(lons)
    
    #new_file.createDimension('lev', tamanho_lev)
    td =new_file.createDimension('time', dtime)
    lad=new_file.createDimension('latitude', tamanho_lat)
    lod=new_file.createDimension('longitude', tamanho_lon)

    #new_file.createVariable('lev' ,'i4', ('lev'))

    tim      = new_file.createVariable('time','f', ('time'))
    latitude = new_file.createVariable('latitude'  ,'f8', ('latitude'))
    longitude= new_file.createVariable('longitude' ,'f8', ('longitude'))
    new_file.variables['time'][:]=times       
    new_file.variables['latitude'][:]=lats      
    new_file.variables['longitude'][:]=lons  

    # Colocando os dados nas dimensoes criadas 
    #tim       =new_file.variables['time'][:]       
    #latitude  =new_file.variables['latitude'][:]       
    #longitude =new_file.variables['longitude'][:]  

    tim.units='hours since 1970-01-01 00:00:0' 
    tim.calendar='360_day' 

    #latitude.units='degrees_north' 
    #longitude.units='degrees_east'
    latitude.units='degrees_north' 
    longitude.units='degrees_east'
    
    #tim = times[:] 
    #latitude = lats[:] 
    #longitude= lons[:]

    #Criando variaveis desejadas 
    #print(vars[0].shape, tamanho_lat,tamanho_lon,dtime)

    
    #######Variavel 1
    var_1 = new_file.createVariable('u_anly_summer', 'f8', ('time','latitude', 'longitude'))
    var_1.setncatts({'long_name': u" Wind anomaly of the u component ",\
                        'units': u"m/s", 'level': u'0-17',\
                        'var_desc': u"u created using Metoff model",\
                        'statistic': u'anomalia de djf\nM'})
    
    #colocando os dados na variavel 1 neste caso anomalia 
    new_file.variables['u_anly_summer'][:] = vars 
    
    #Fecha o novo arquivo aberto.
    new_file.close() 

    return 

def savetonc2(times,levs,lats,lons,vars,name):

    #Abrindo o novo arquivo nc.
    #Formato: 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', 'NETCDF4'
    
    new_file = Dataset('%s.nc'%name, 'w', format='NETCDF4')
    new_file.description = "This file contais the u wind \n anomaly from 1978 to 2014 only of the summer period (DJF), winter (j,j,a)"
    
    # Data e criador
    new_file.history     = "Created " + today.strftime("%d/%m/%y")
    new_file.author      = "Jhonatan A. A manco"
    

    #Tamanho do tempo, use np.shape or len()
    dtime =len(times[0])
    new_file.createDimension('time1', dtime)

    dtime =len(times[2])
    new_file.createDimension('time2', dtime)

    #Tamanho das dimensoes. 
    #Pode usar  np.shape() para saber estes tamanhos 

    #tamanho_lev=len(levs)

    tamanho_lat=len(lats)
    tamanho_lon=len(lons)
    
    #Lat e Lon
    #new_file.createDimension('lev', tamanho_lev)
    new_file.createDimension('longitude', tamanho_lon)
    new_file.createDimension('latitude', tamanho_lat)


    t1=new_file.createVariable('time1'    ,'f', ('time1'))
    t2=new_file.createVariable('time2'    ,'f', ('time2'))
    lt=new_file.createVariable('latitude' ,'f8', ('latitude'))
    lg=new_file.createVariable('longitude','f8', ('longitude'))

    #new_file.createVariable('lev' ,'i4', ('lev'))


    # Colocando os dados nas dimensoes criadas 
    new_file.variables['time1'][:]      = times[0]
    new_file.variables['time2'][:]      = times[2]
    new_file.variables['longitude'][:]  = lons
    new_file.variables['latitude'][:]   = lats
    #new_file.variables['lev'][:]  = levs

    t1.units='hours since 1970-01-01 00:00:0' 
    t1.calendar='360_day' 

    t2.units='hours since 1970-01-01 00:00:0' 
    t2.calendar='360_day' 

    lt.units='degrees_north' 
    lg.units='degrees_east'



##############3
    us = new_file.createVariable('u3as', 'f8', ('time1','latitude', 'longitude'))
    us.setncatts({'long_name': u"Summer Wind anomaly of \n the u component from 1978 to 2014 Lev:%s"%(levs),\
                        'units': u"m/s", 'level': u'0-17',\
                        'var_desc': u"Created using Metoff model",\
                        'statistic': u'anomalia de djf\nM'})
    
    #colocando os dados na variavel 1 neste caso anomalia 
    new_file.variables['u3as'][:] = vars[0] 
##############3

    uw = new_file.createVariable('u3aw', 'f8', ('time2','latitude', 'longitude'))
    uw.setncatts({'long_name': u"Winter Wind anomaly of \n the u component from 1978 to 2014",\
                        'units': u"m/s", 'level': u'%s'%levs,\
                        'var_desc': u"Created using Metoff model",\
                        'statistic': u'anomalia de jja\nM'})
    
    #colocando os dados na variavel 1 neste caso anomalia 
    new_file.variables['u3aw'][:] = vars[1] 

##############3
    us = new_file.createVariable('u5as', 'f8', ('time1','latitude', 'longitude'))
    us.setncatts({'long_name': u"Summer Wind anomaly of \n the u component from 1978 to 2014 Lev:%s"%(levs),\
                        'units': u"m/s", 'level': u'0-17',\
                        'var_desc': u"Created using Metoff model",\
                        'statistic': u'anomalia de djf\nM'})
    
    #colocando os dados na variavel 1 neste caso anomalia 
    new_file.variables['u5as'][:] = vars[2] 

##############3

    uw = new_file.createVariable('u5aw', 'f8', ('time2','latitude', 'longitude'))
    uw.setncatts({'long_name': u"Winter Wind anomaly of \n the u component from 1978 to 2014",\
                        'units': u"m/s", 'level': u'%s'%levs,\
                        'var_desc': u"Created using Metoff model",\
                        'statistic': u'anomalia de jja\nM'})
    
    #colocando os dados na variavel 1 neste caso anomalia 
    new_file.variables['u5aw'][:] = vars[3] 


##############3

    vs = new_file.createVariable('v3as', 'f8', ('time1','latitude', 'longitude'))
    vs.setncatts({'long_name': u"Summer Wind anomaly of \n the u component from 1978 to 2014",\
                        'units': u"m/s", 'level': u'%s'%levs,\
                        'var_desc': u"Created using Metoff model",\
                        'statistic': u'anomalia de jja\nM'})
    
    #############
    #colocando os dados na variavel 1 neste caso anomalia 
    new_file.variables['v3as'][:] = vars[4] 

    vs = new_file.createVariable('v3aw', 'f8', ('time2','latitude', 'longitude'))
    vs.setncatts({'long_name': u"Winter Wind anomaly of \n the u component from 1978 to 2014",\
                        'units': u"m/s", 'level': u'%s'%levs,\
                        'var_desc': u"Created using Metoff model",\
                        'statistic': u'anomalia de jja\nM'})
    
    #colocando os dados na variavel 1 neste caso anomalia 
    new_file.variables['v3aw'][:] = vars[5] 

    #########3

    vs = new_file.createVariable('v5as', 'f8', ('time1','latitude', 'longitude'))
    vs.setncatts({'long_name': u"Summer Wind anomaly of \n the u component from 1978 to 2014",\
                        'units': u"m/s", 'level': u'%s'%levs,\
                        'var_desc': u"Created using Metoff model",\
                        'statistic': u'anomalia de jja\nM'})
    
    #############
    #colocando os dados na variavel 1 neste caso anomalia 
    new_file.variables['v5as'][:] = vars[6] 

    vs = new_file.createVariable('v5aw', 'f8', ('time2','latitude', 'longitude'))
    vs.setncatts({'long_name': u"Winter Wind anomaly of \n the u component from 1978 to 2014",\
                        'units': u"m/s", 'level': u'%s'%levs,\
                        'var_desc': u"Created using Metoff model",\
                        'statistic': u'anomalia de jja\nM'})
    
    #colocando os dados na variavel 1 neste caso anomalia 
    new_file.variables['v5aw'][:] = vars[7] 
    
    
    #Fecha o novo arquivo aberto.
    new_file.close() 

    return 
