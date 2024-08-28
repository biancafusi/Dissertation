#################################
#PYTHON CODE TO PLOT DIFFERENS 
#MAPS PROJECTION USING THE 
#LIBRARY BASEMAP. 
#################################
#PYTHON CODE TO PLOT DIFFERENS 
# Data:13/04/22
#################################
# By: Jhonatan A. A Manco
#################################

import os, sys

import numpy as np

import datetime as dt  

import cftime

import matplotlib.pyplot as plt


# Function with the definition of differents projetions
from   source.plotprojection    import plot_own_cyli,plot_own_ortho, plot_own_robin,cartopy1

# own function to transform the data in data_time 
from   source.data_own          import data_day

# Own Functions, to read the data, make anomaly 
from   source.variablesfunction import ncdump

from   Parameters import z3



datei   = cftime.datetime(2010,1,16, calendar=u'360_day')
index1  = data_day(datei,z3.data)



#cartopy

fig1=cartopy1(z3.zg[index1,5,:,:],z3.lats[:],z3.lons[:],'cartopy','cartopy')


#Cylindrical projection 
#ok
fig1=plot_own_cyli(z3.zg[index1,5,:,:],z3.lats[:],z3.lons[:],'py','cylindrical_projection')

#Orthogonal  projection 
#ok
#fig2=plot_own_ortho(z3.zg[index1,5,:,:],z3.lats[:],z3.lons[:],'','orthogonal_projection')

#Robin projection 
#ok, mas nao funciona colocando o brasil no centro
#fig3=plot_own_robin(z3.zg[index1,5,:,:],z3.lats[:],z3.lons[:],'','robin_projection')

plt.show()





