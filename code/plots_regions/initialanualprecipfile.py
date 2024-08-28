import pandas as pd
import os, sys
from netCDF4 import Dataset
from function import filename2,anom
import numpy as np
from concfunction import conc_func
import datetime as dt  
from plot import plot_precip, plot_anom
from data_own import data_day
from variablesfunction import ncdump
import matplotlib.pyplot as plt
from anomalia import anom2

#Arquivo que faz as medias de maneira manual
arquivo = 'precip.mon.mean.nc'
nc_f = arquivo

#To show the file variables
nc_fid = Dataset(arquivo, 'r')  # Dataset is the class behavior to open the file
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
date1= dt.date(2020,1,1)
date2 = dt.date(2020,2,1)
date3 = dt.date(2020,3,1)
index1 = data_day(date1,dt_time)
index2 = data_day(date2,dt_time)
index3 = data_day(date3,dt_time)
date4= dt.date(2021,1,1)
date5 = dt.date(2021,2,1)
date6 = dt.date(2021,3,1)
index4 = data_day(date4,dt_time)
index5 = data_day(date5,dt_time)
index6 = data_day(date6,dt_time)
 	

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
	
media2020 = (air[index1,:,:]+air[index2,:,:]+air[index3,:,:])/3.0
media2021 = (air[index4,:,:]+air[index5,:,:]+air[index6,:,:])/3.0

#Média dos trimestres no intervalo de 1979 até 2022
media1 = np.mean(alljanuary,axis = 0)
media2 = np.mean(allfebruary,axis = 0)
media3 = np.mean(allmarch,axis = 0)
mediatotal = (media1+media2+media3)/3.0
#fig1 = plot_precip(mediatotal,lats,lons,'Quartely Precipitation Average 1979-2020','mediatri1979_2022')


#Anomalia 2020
anomalia = anom2(media2020,mediatotal)
fig2 = plot_temporal(anomalia,lats,lons,'Quartely Precipitation Average 2020','anomaliatrimestral2020')


#Anomalia 2021
anomalia2 = anom2(media2021,mediatotal)
fig3 = plot_anom(anomalia2,lats,lons,'Quartely Precipitation Average 2021','anomaliatrimestral2021')

plt.show()


