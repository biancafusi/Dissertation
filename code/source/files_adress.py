# Function to load the ncfiles
import   var_load_geo   as geo  

#Data: precipitation from 1970 to 2021 
zg_325 ='./data/zg_u-bh325_Mon.nc'
z3= geo.ncload(zg_325)

##pr_u-bh325_Mon.nc
##pr_u-cf544_Mon.nc
##ua_u-bh325_Mon.nc
##ua_u-cf544_Mon.nc
##va_u-bh325_Mon.nc 


#Out folder to save the fig

out_folder='/home/jhona/repositories/robin/' 
