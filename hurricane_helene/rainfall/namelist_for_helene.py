

'''
READ ME:
            initial_day =           Str for the initial time of the experiment being at Y-M-DTH:M format
            final_day =             Str for initial time of the experiment being at Y-M-DTH:M format

'''

initial_day = '2024-09-25T00'
final_day = '2024-09-28T00'
# final_day = '2024-09-29T00'

lonW, lonE, latS, latN = -92, -69, 17, 49

NOAA_path = '/mnt/beegfs/bianca.fusinato/monan/comparison/Helene.nc'
run_folder = '/mnt/beegfs/bianca.fusinato/monan/model/'

# data information for accumulated panels: (model resolution)
# data_information = [
#     ('ERA5', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/era5/x1.655362.era5_helene_moist_native.nc.nc'),
#     ('GPM-IMERG', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/new_imerg/x1.655362.3B-HHR.MS.MRG.3IMERG.2024092201_1hour.nc'),
#     ('NWS', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/NWS/x1.655362.rainfall.nc'),
#     ('GSMaP', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/GSMaP/x1.655362.helene_gsmap.nc'),
#     # ('CP-ON', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/all_diag_dc.2024-09-24_12.00.00.nc'),
#     # ('CP-OFF', run_folder+'helene_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/all_diag_dc.2024-09-24_12.00.00.nc'),
#     # ('CP-15km', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/cp-15/x1.655362.helene_15km.nc'),
#     # ('CP-1HD050', run_folder+'helene_cporg1_gustf1_sub3d0_LT1HD050_ERA5_x1.655362/2024092412/diag/all_diag_dc.2024-09-24_12.00.00.nc'),
#     # ('CP-25', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092500/diag/all_diag_dc.2024-09-25_00.00.00.nc')
# ]
# # aqui eu estou usando os all_diag, então só preciso selecionar o dia ref ao final day

# #data information for hourly precipitation (MODELS RESOLUTION (EXCEPT CP15km)):
data_information = [
    ('ERA5', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/era5/x1.655362.era5_helene_moist_native.nc.nc'),
    ('GPM-IMERG', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/new_imerg/x1.655362.3B-HHR.MS.MRG.3IMERG.2024092201_1hour.nc'),
    ('GSMaP', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/GSMaP/x1.655362.helene_gsmap.nc'),
    ('CP-ON', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
    ('CP-OFF', run_folder+'helene_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
    ('CP-15km', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.2621442/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
    ('CP-1HD050', run_folder+'helene_cporg1_gustf1_sub3d0_LT1HD050_ERA5_x1.655362/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
    ('CP-25', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092500/diag/only_precip_diag_dc.2024-09-25_00.00.00.nc')
]

#data information for hourly precipitation native:
# data_information = [
#     ('ERA5', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/era5/era5_helene_moist_native.nc'),
#     ('GPM-IMERG', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/IMERG/imerg_helene_native.nc'),
#     ('GSMaP', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/GSMaP/helene_gsmap.nc'),
#     ('CP-30km', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
#     ('CP-15km', run_folder+'helene_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.2621442/2024092412/diag/only_precip_diag_dc.2024-09-24_12.00.00.nc'),
# ]

