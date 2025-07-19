import numpy as np

'''
READ ME: Please insert the values of the following parameters:

    lonW, lonE, latS, latN: The study region of interest
    initial_time:           Must be in 'Y-M-D' format
    final_time:             Must be in 'Y-M-D' format
    label_experiment:       You choose, it will appears at the graph's legend
    label_control:          You choose, it will appears at the graph's legend
    control_color:          You choose, it will appears at the graph
    graph_title:            You choose, it will appears at the graph
    saving_name:            This is the file name that will be saved
    type_timeSeries:        Can be MSLP or WSPD 
    data_location:          Folder path that contains all data, if it exists. If doesnt, comment the line and insert full path on the file's names
    where_save:             Path where to save the plot
    NOAA_path:              In this program logic, it will be NOAA's file name, Its mandatory!
    ERA5_path:              In this program logic, it will be ERA5's file name
    GPM_path:               In this program logic, it will be GPM's file name, Its configured with lon [0,360]!
    CONTROL_path:           In this program logic, it will be CONTROL's file name
    EXPERIMENT_path:        In this program logic, it will be EXPERIMENT's file name

    Obs.: The wind is the maximum value within a 0.25/0.25 lat/lon box

'''

def calc_wspd(dataset):
    mag_wind = dataset.wspd
    return mag_wind*3.6

def calc_wind(dataset):
    zonal = dataset.u10
    meridian = dataset.v10
    mag_wind = np.sqrt(zonal**2+meridian**2)
    return mag_wind*3.6

def calc_wind_gustfront(dataset):
    zonal = dataset.u_gustfront
    meridian = dataset.v_gustfront
    mag_wind = np.sqrt(zonal**2+meridian**2)
    return mag_wind*3.6

lonW, lonE, latS, latN = -106, -50, 10, 40

initial_time = '2024-07-01'
final_time = '2024-07-11'

different_day = 'OFF'
new_day = '2024-06-29'

label_experiment = 'CP-ON'
label_control = 'CP-OFF'

control_color = 'black'
experiment_color = 'red'

# type_timeSeries = 'WSPD' 
type_timeSeries = 'MSLP' 

saving_name = f'Beryl_CPOFF_Control_{type_timeSeries}_1st_july.png'
graph_title = f'{type_timeSeries}, tracked by NOAA, ERA5 and Model'

data_location = '/mnt/beegfs/bianca.fusinato/monan/model/'
where_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/time_series/outputs_July_1st/'

NOAA_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/pathing/beryl.nc'

convertion_to_180 = 'ON'
ERA5_path = '/mnt/beegfs/bianca.fusinato/monan/comparison/era5_dry.nc'

CONTROL_path =  data_location + 'beryl_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'
EXPERIMENT_path = data_location + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'

