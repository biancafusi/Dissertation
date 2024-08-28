from function import filename2
import numpy as np

def conc_func(arquivo):
	lats, lons, air, time = filename2(arquivo[0])
	conctotal = np.zeros([len(arquivo),len(lats),len(lons)]) 
	tempototal = np.zeros([len(arquivo)])
	for i in range(0,len(arquivo)-1):
		lats2, lons2, air2, time2 = filename2(arquivo[i+1])
		conctotal = np.concatenate((air,air2),axis = 0)
		tempototal = np.concatenate((time,time2))
		air=conctotal  
		time = tempototal
	return conctotal, tempototal, lats, lons

	
