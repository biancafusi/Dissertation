'''
READ ME:
            initial_day =           Str for the initial time of the experiment being at Y-M-DTH:M format
            final_day =             Str for initial time of the experiment being at Y-M-DTH:M format

'''

initial_day = '2024-07-03T12'
final_day = '2024-07-09T00'

lonW, lonE, latS, latN = -106, -50, 10, 41

label_data = 'CP-01'
# label_data = 'GPM'
# label_data = 'CP-ON'
# label_data = 'CP-OFF'
# label_data = 'CP-1H'
# label_data = 'CP-3H'
# label_data = 'CP-6H'
# label_data = 'CP-D025'
# label_data = 'CP-D050'
# label_data = 'CPSS-ON'
# label_data = 'CP-15km'
# label_data = 'CP-60km'
# label_data = 'CP-GFS'
# label_data = 'CP-01'
# label_data = 'CP-02T12'
# label_data = 'CP-29'

NOAA_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/time_series/beryl.nc'
run_folder = '/mnt/beegfs/bianca.fusinato/monan/model/'

if initial_day == '2024-07-03T12':
    
    if label_data == 'ERA5':

        name_file_prec = '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/era5_moist.nc'
        name_file_dry = '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/era5_dry.nc'

    elif label_data == 'GPM':
        name_file_prec = '/mnt/beegfs/bianca.fusinato/monan/comparison/GPM/x1.655362.3B-HHR.MS.MRG.3IMERG.2024_01Z2906_24Z0909_1hour.nc'
        
    elif label_data == 'CP-ON':
        name_file_prec = run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

    elif label_data == 'CP-OFF':
        name_file_prec = run_folder+'beryl_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'
        
    elif label_data == 'CP-1H':
        name_file_prec = run_folder+'beryl_cporg1_gustf1_sub3d0_TCP1H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

    elif label_data == 'CP-3H':
        name_file_prec = run_folder+'beryl_cporg1_gustf1_sub3d0_TCP3H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

    elif label_data == 'CP-6H':
        name_file_prec = run_folder+'beryl_cporg1_gustf1_sub3d0_TCP6H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

    elif label_data == 'CP-D025':
        name_file_prec = run_folder+'beryl_cporg1_gustf1_sub3d0_DOW025_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

    elif label_data == 'CP-D050':
        name_file_prec = run_folder+'beryl_cporg1_gustf1_sub3d0_DOW050_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

    elif label_data == 'CPSS-ON':
        name_file_prec = run_folder+'beryl_cporg1_gustf2_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

    elif label_data == 'CP-15km':
        name_file_prec = run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.2621442/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'
    
    elif label_data == 'CP-60km':
        name_file_prec = run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.163842/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

    elif label_data == 'CP-GFS':
        name_file_prec = '/mnt/beegfs/bianca.fusinato/monan/model/GFS_run/beryl_cporg1_gustf1_sub3d0_GFdef_GFS_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

    elif label_data == 'CP-29':
        name_file_prec = run_folder + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024062900/diag/all_diag_dc.2024-06-29_00.00.00.nc'

    elif label_data == 'CP-01':
        name_file_prec = run_folder + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'

    elif label_data == 'CP-02T12':
        name_file_prec = run_folder + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070212/diag/all_diag_dc.2024-07-02_12.00.00.nc'