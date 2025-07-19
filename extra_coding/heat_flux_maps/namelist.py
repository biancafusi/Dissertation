'''
STATUS: WORKING!

LAST UPDATED: March 25 2025
'''

panels =[
    'Panel 01', 'Panel 02', 'Panel 03', 'Panel 04'
]

initial_day = '2024-07-03T00'
final_day = '2024-07-09T00'

lonW, lonE, latS, latN = -99, -63, 10, 30

run_folder = '/mnt/beegfs/bianca.fusinato/monan/model/'

data_information_rain = [
    ('GPM', '/mnt/beegfs/bianca.fusinato/monan/comparison/GPM/x1.655362.3B-HHR.MS.MRG.3IMERG.2024_01Z2906_24Z0909_1hour.nc'),
    ('CP-ON',  run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'),
    ('CP-OFF',  run_folder+'beryl_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'),
    ('CP-60km',  run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.163842/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'),
    ('CP-15km',  run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.2621442/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc'),
    ('CPSS-ON',  run_folder+'beryl_cporg1_gustf2_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/only_precip_diag_dc.2024-07-03_00.00.00.nc')
]

data_information_dry = [
    ('CP-ON',  run_folder+'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ('CP-OFF',  run_folder+'beryl_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
    ('CPSS-ON',  run_folder+'beryl_cporg1_gustf2_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'),
]

saving_paths_dict = {
    'GPM': '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_01/GPM/',
    'CP-ON': '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_01/CP-ON/',
    'CP-OFF': '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_01/CP-OFF/',
    'CP-15km': '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_02/CP-15km/',
    'CP-60km': '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_02/CP-60km/'
}