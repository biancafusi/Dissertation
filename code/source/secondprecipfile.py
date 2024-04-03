import pandas as pd
import os, sys
from netCDF4 import Dataset
from function import filename2,anom
import numpy as np
from concfunction import conc_func
import datetime as dt  
from plot import plot_own
from data_own import data_day
from variablesfunction import ncdump

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
print(dt_time)
#representação mensal (média de 3 meses)


date_start1= dt.date(2019,1,1)
date_finish1 = dt.date(2019,3,1)



plot_own(media,lats,lons,'Manual average Jan:Mar 19:21','Manual average Jan:Mar 19:21')
plt.savefig('Manual average Jan:Mar 19:21')

