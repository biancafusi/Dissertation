'''
STATUS: Currently working

LAST UPDATED: March 24 2025
'''
# initial_day = '2024-07-01T00'
initial_day = '2024-07-03T00'
final_day = '2024-07-09T00'
num_days = 6

lonW, lonE, latS, latN = -106, -50, 10, 41

NOAA_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/time_series/beryl.nc'
run_folder = '/mnt/beegfs/bianca.fusinato/monan/model/'

folder_60km = '/mnt/beegfs/bianca.fusinato/monan/model/beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.163842/2024070300/diag/'
folder_gfs = '/mnt/beegfs/bianca.fusinato/monan/model/GFS_run/beryl_cporg1_gustf1_sub3d0_GFdef_GFS_x1.655362/2024070300/diag/'

data_information = [
    ('ERA5', 'blue', '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/x1.655362.era5_moist.nc'),
    ('CP-ON', 'red', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ('CP-OFF', 'black', run_folder+'beryl_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ('CP-1H', 'springgreen', run_folder+'beryl_cporg1_gustf1_sub3d0_TCP1H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ('CP-3H', 'orange', run_folder+'beryl_cporg1_gustf1_sub3d0_TCP3H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ## ('CP-6H', 'purple', run_folder+'beryl_cporg1_gustf1_sub3d0_TCP6H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ('CP-D025', 'brown', run_folder+'beryl_cporg1_gustf1_sub3d0_DOW025_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ('CP-D050', 'pink', run_folder+'beryl_cporg1_gustf1_sub3d0_DOW050_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ## ('CPSS-ON', 'cyan', run_folder+'beryl_cporg1_gustf2_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ## ('CPSS-02', 'steelblue', run_folder+'beryl_cporg1_gustf2_sub3d0_GFdef_ERA5_x1.655362/2024070200/diag/all_diag_dc.2024-07-02_00.00.00.nc'),
    ('CP-15km', 'magenta', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.2621442/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ('CP-60km', 'lime', folder_60km +'all_diag_dc.2024-07-03_00.nc'),
    ('CP-GFS', 'navy', folder_gfs+'all_diag_dc.2024-07-03_00.00.00.nc'),
    ('CP-29', 'darkorange', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024062900/diag/all_diag_dc.2024-06-29_00.00.00.nc'),
    #('CP-01', 'teal', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'),
    ('CP-02T12', 'olive', run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070212/diag/all_diag_dc.2024-07-02_12.00.00.nc'),
    ('CP-1HD050', 'cyan', run_folder+'beryl_cporg1_gustf1_sub3d0_LT1HD050_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ## ('CP-1HD05015km', 'violet', run_folder+'beryl_cporg1_gustf1_sub3d0_LT1HD050_ERA5_x1.2621442/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc')
]

