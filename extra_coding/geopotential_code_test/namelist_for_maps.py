'''
STATUS: currently working

LAST UPDATED: May 21 2025
'''

import numpy as np

# Beryl map:
lonW, lonE, latS, latN = -106, -50, 10, 40

NOAA_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/time_series/beryl.nc'

# initial_day = '2024-07-01T00'
initial_day = '2024-07-03T12'
final_day = '2024-07-09T00'

# NOAA_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/time_series/beryl.nc'
run_folder = '/mnt/beegfs/bianca.fusinato/monan/model/'

where_to_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/maps/geopotential_plus_tracking_files/'

data_information = [
    # ('ERA5', 'blue', '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/x1.655362.era5_moist.nc'),
    ('CP-ON', run_folder+'beryl_more_fieds_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ('CP-OFF', run_folder+'beryl_more_fieds_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    # # ('CP-1H', 'springgreen', run_folder+'beryl_cporg1_gustf1_sub3d0_TCP1H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    # ('CP-3H', 'orange', run_folder+'beryl_cporg1_gustf1_sub3d0_TCP3H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    # ('CP-D025', 'brown', run_folder+'beryl_cporg1_gustf1_sub3d0_DOW025_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    # ('CP-D050', 'pink', run_folder+'beryl_cporg1_gustf1_sub3d0_DOW050_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    # # ('CP-GFS', 'navy', '/mnt/beegfs/bianca.fusinato/monan/model/GFS_run/beryl_cporg1_gustf1_sub3d0_GFdef_GFS_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    # # ('CP-29', 'darkorange', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024062900/diag/all_diag_dc.2024-06-29_00.00.00.nc'),
    # # ('CP-02T12', 'olive', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070212/diag/all_diag_dc.2024-07-02_12.00.00.nc'),
    # ('CP-1HD050', 'silver', run_folder+'beryl_cporg1_gustf1_sub3d0_LT1HD050_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
]

