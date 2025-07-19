'''
STATUS: currently working

LAST UPDATED: June 14 2025
'''

import numpy as np

def calc_wspd(dataset):
    mag_wind = dataset.wspd
    return mag_wind*3.6

def calc_wind_gf_era5(dataset):
    mag_wind = dataset.i10fg 
    return mag_wind*3.6

def calc_wind_100(dataset):
    zonal = dataset.u100
    meridian = dataset.v100
    mag_wind = np.sqrt(zonal**2+meridian**2)
    return mag_wind*3.6

def calc_wind_gustfront(dataset):
    zonal = dataset.u_gustfront
    meridian = dataset.v_gustfront
    mag_wind = np.sqrt(zonal**2+meridian**2)
    return mag_wind*3.6


lonW, lonE, latS, latN = -92, -69, 17, 49

initial_day = '2024-09-25T00'
final_day = '2024-09-28T00'

NOAA_path = '/mnt/beegfs/bianca.fusinato/monan/comparison/Helene.nc'
run_folder = '/mnt/beegfs/bianca.fusinato/monan/model/'

saving_excel_folder = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/statistical_metrics/helene_final/'

where_to_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/statistical_metrics/helene_final/'

# dataset in 30km except 15km run
data_information = [
    ('ERA5', 'blue', '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/x1.655362.era5_moist.nc'),
    ('CP-ON', 'red', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/all_diag_dc.2024-09-24_12.00.00.nc'),
    ('CP-OFF', 'black', run_folder+'helene_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/all_diag_dc.2024-09-24_12.00.00.nc'),
    ('CP-15km', 'magenta', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.2621442/2024092412/diag/all_diag_dc.2024-09-24_12.00.00.nc'),
    ('CP-25', 'darkorange', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092500/diag/all_diag_dc.2024-09-25_00.00.00.nc'),
    ('CP-1HD050', 'cyan', run_folder+'helene_cporg1_gustf1_sub3d0_LT1HD050_ERA5_x1.655362/2024092412/diag/all_diag_dc.2024-09-24_12.00.00.nc'),
]

ax_label = 'Hours after 09-25T00'