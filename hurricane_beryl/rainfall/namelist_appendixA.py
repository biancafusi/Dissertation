

'''
READ ME:
            initial_day =           Str for the initial time of the experiment being at Y-M-DTH:M format
            final_day =             Str for initial time of the experiment being at Y-M-DTH:M format

'''

initial_day = '2024-09-25T12'
final_day = '2024-09-28T00'

lonW, lonE, latS, latN = -92, -69, 21, 49

NOAA_path = '/mnt/beegfs/bianca.fusinato/monan/comparison/Helene.nc'
run_folder = '/mnt/beegfs/bianca.fusinato/monan/model/'

data_information_MONAN = [
    ('NCEP', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/NWS/x1.655362.rainfall.nc' ),
    ('GPM-IMERG', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/new_imerg/x1.655362.3B-HHR.MS.MRG.3IMERG.2024092201_1hour.nc'),
    ('GSMaP', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/GSMaP/x1.655362.helene_gsmap.nc'),
]

data_information_native= [
    ('NCEP', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/NWS/rainfall.nc' ),
    ('GPM-IMERG', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/new_imerg/3B-HHR.MS.MRG.3IMERG.2024092201_1hour.nc4'),
    ('GSMaP', '/mnt/beegfs/bianca.fusinato/monan/comparison/helene/GSMaP/helene_gsmap.nc'),
]


where_to_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/accumulated/Appendix_A/'