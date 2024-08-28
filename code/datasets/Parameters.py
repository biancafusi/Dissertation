# Function to load the ncfiles
import xarray as xr

##import  source.var_load_era5 as e5 

path='/mnt/beegfs/bianca.fusinato/dados_mestrado'
path2='/mnt/beegfs/bianca.fusinato/dados_mestrado/era5/era5_2014.nc'


#febquv   = '%s/day/quv_levs.grib'%(path)
#fquv     =  xr.open_dataset(febquv)

'''
DATA NAME INFORMATION:

Chuvosa s/ CP - IOP1_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km - all_extIOP1_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km-2014-02-15.nc
Chuvosa c/ CP - IOP1_1_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km
Seca s/ CP - IOP2_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km
Seca c/ CP - IOP2_1_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km
Transicao s/ CP - IOP2_4_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km
Transicao c/ CP - IOP2_4_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km

CHUVOSA:
2014-02-15-00 ate 2014-02-24-00
SECA:
2014-09-01-00 ate 2014-09-10-00
Trasicao:
2014-10-01-00  ate 2014-10-10-00
'''

d1   = '%s/all_extIOP1_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km-2014-02-15.nc'%(path)
b1   =  xr.open_dataset(d1)

era5 = path2
b2   = xr.open_dataset(era5,  engine='netcdf4')

#out_folder='/home/jhona/repositories/robin/bloking/document/bloking/figs/' 
out_fig='/mnt/beegfs/bianca.fusinato/dados_mestrado/python_plots/Dissertation/results/'

