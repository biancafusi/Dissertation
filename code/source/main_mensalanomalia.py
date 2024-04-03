#################################
#PYTHON CODE TO PLOT DIFFERENS 
#MAPS PROJECTION USING THE 
#LIBRARY BASEMAP. 
#################################
#PYTHON CODE TO PLOT DIFFERENS 
# Data:13/04/22
#################################
# By: Pedro  
#    Jhonatan A. A Manco         #
#################################

import os, sys
import numpy as np
import datetime as dt  
import matplotlib.pyplot as plt

# Function with the definition of differents projetions
from   plotprojection    import plot_own_cyli,plot_own_ortho, plot_own_robin, plot_anom
# Function to concatenate nc files 
from   concfunction      import conc_func
# Function to read ncfiles 
from   netCDF4           import Dataset
# Own Functions, to read the data, make anomaly 
from   function          import filename2,anom

# own function to transform the data in data_time 
from   data_own          import data_day

# Function to look the ncfiles
from   variablesfunction import ncdump

#Functtion with the adress of the data files 
from files_adress import gpcp_data

from anomalia import anom2

#Arquivo que faz as medias de maneira manual
nc_f = gpcp_data

#To show the file variables
nc_fid = Dataset(nc_f, 'r')   # Dataset is the class behavior to open the file
                              # and create an instance of the ncCDF4 class
#nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)
lats, lons, air,time = filename2(nc_f)

#necessidade de arrumar dt_time
dt_time = [dt.date(1800, 1, 1) + dt.timedelta(hours=t*24) 
           for t in time]

#representacao mensal (media de 3 meses)
#print(dt_time)


#2020 dates
date1= dt.date(2020,1,1)
date2 = dt.date(2020,2,1)
date3 = dt.date(2020,3,1)
index1 = data_day(date1,dt_time)
index2 = data_day(date2,dt_time)
index3 = data_day(date3,dt_time)

#2021 dates
date4= dt.date(2021,1,1)
date5 = dt.date(2021,2,1)
date6 = dt.date(2021,3,1)
index4 = data_day(date1,dt_time)
index5 = data_day(date2,dt_time)
index6 = data_day(date3,dt_time)


alljanuary = []
allfebruary = []
allmarch = []
firstmonth = 0
secondmonth =1
thirdmonth = 2
for i in range(0,int(len(dt_time)/12)):
	soma_month = air[firstmonth,:,:]
	soma_month2 = air[secondmonth,:,:]
	soma_month3 = air[thirdmonth,:,:]
	firstmonth = firstmonth+12
	secondmonth = secondmonth+12
	thirdmonth = thirdmonth+12
	alljanuary.append(soma_month)
	allfebruary.append(soma_month2)
	allmarch.append(soma_month3)
	

#Anomalia de cada mês do trimestre de 2020
media1 = np.mean(alljanuary,axis = 0)
media2 = np.mean(allfebruary,axis = 0)
media3 = np.mean(allmarch,axis = 0)

anomalia = anom2(media1,air[index4,:,:])
anomalia2 = anom2(media2,air[index5,:,:])
anomalia3 = anom2(media3,air[index6,:,:])

#PLOT PARA ANOMALIA DE CADA MÊS DE 2020
fig1 = plot_anom(anomalia,lats,lons,'Jan Anomalia 2020','Jan2020')
fig2 = plot_anom(anomalia2,lats,lons,'Fev Anomalia 2020','Fev2020')
fig3 = plot_anom(anomalia3,lats,lons,'Mar Anomalia 2020','Mar2020')


#Anomalia de cada mês do trimestre de 2021
media4 = np.mean(alljanuary,axis = 0)
media5 = np.mean(allfebruary,axis = 0)
media6 = np.mean(allmarch,axis = 0)

anomalia4 = anom2(media1,air[index4,:,:])
anomalia5 = anom2(media2,air[index5,:,:])
anomalia6 = anom2(media3,air[index6,:,:])

#PLOT PARA ANOMALIA DE CADA MÊS DE 2021
fig4 = plot_anom(anomalia4,lats,lons,'Jan Anomalia 2021','Jan2021')
fig5 = plot_anom(anomalia5,lats,lons,'Fev Anomalia 2021','Fev2021')
fig6 = plot_anom(anomalia6,lats,lons,'Mar Anomalia 2021','Mar2021')


plt.show()
