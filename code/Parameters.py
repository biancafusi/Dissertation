# Function to load the ncfiles
import xarray as xr

##import  source.var_load_era5 as e5 

path='/mnt/beegfs/bianca.fusinato/dados_mestrado'


#febquv   = '%s/day/quv_levs.grib'%(path)
#fquv     =  xr.open_dataset(febquv)

d1   = '%s/all_extIOP1_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km-2014-02-15.nc'%(path)
b1   =  xr.open_dataset(d1)


#out_folder='/home/jhona/repositories/robin/bloking/document/bloking/figs/' 
out_fig='/mnt/beegfs/bianca.fusinato/dados_mestrado/python_plots/'

