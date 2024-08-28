import numpy as np
from function import filename



def anom(index1,index2,air,lats,lons):
	anomalia=np.zeros((index2-index1,len(lats),len(lons)))
	anualmedia=np.mean(air[index1:index2,:,:],axis=0)
	j=0
	for i in range(index1,index2):
		anomalia[j,:,:] = air[i,:,:] - anualmedia[:,:]
		j=j+1
	return anomalia
	
def anom2(media,datatoanom):

	anomalia = datatoanom-media

	return anomalia
	
	#anomalia > 0 = chuva maior que a media
	#anomali < 0 = seca
	#
