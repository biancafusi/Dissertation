'''
WORKING
'''

lonW, lonE, latS, latN = -106, -50, 10, 40

initial_day = '2024-07-03T00'
final_day = '2024-07-09T00'

output_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/sst/'

title_prefix  =  'ERA5'
                # OPTIONS:
                # 'ERA5'
                # 'CP-ON'
                # 'CP-1H'
                # 'CP-3H'
                # 'CP-6H'
                # 'CP-D025'
                # 'CP-D050'
                # 'CPSS-ON'
                # 'CP-29'
                # 'CP-GFS'
                # 'CP-15km'
                # 'CP-GFS-1H'

data_location = '/mnt/beegfs/bianca.fusinato/monan/model/'

if title_prefix == 'ERA5':
    data_path = '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/era5_dry.nc'

elif title_prefix == 'NOAA':
    print('not ready yet ...')

elif title_prefix == 'CP-OFF':
    data_path = data_location + 'beryl_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_2d.nc'

elif title_prefix == 'CP-ON':
    data_path = data_location + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_2d.nc' 