'''
STATUS: Currently working

LAST UPDATED: May 28 2025
'''
# initial_day = '2024-07-01T00'
initial_day = '2024-09-25T00' # deixei de fora as 12 horas de spin-up
final_day = '2024-09-28T00'
num_days = 3

lonW, lonE, latS, latN = -92, -69, 17, 48

NOAA_path = '/mnt/beegfs/bianca.fusinato/monan/comparison/Helene.nc'
run_folder = '/mnt/beegfs/bianca.fusinato/monan/model/'


data_information = [
#    ('ERA5', 'blue', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/era5/x1.655362.era5_helene_moist_native.nc.nc'),
    # ('CP-ON', 'red', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/all_diag_dc.2024-09-24_12.00.00.nc'),
    #('CP-OFF', 'black', run_folder+'helene_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/all_diag_dc.2024-09-24_12.00.00.nc'),
    #('CP-15km', 'magenta', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/cp-15/x1.655362.helene_15km.nc'),
    # ('CP-25', 'darkgreen', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092500/diag/all_diag_dc.2024-09-25_00.00.00.nc'),
    ('CP-1HD050', 'cyan', run_folder+'helene_cporg1_gustf1_sub3d0_LT1HD050_ERA5_x1.655362/2024092412/diag/all_diag_dc.2024-09-24_12.00.00.nc'),
]