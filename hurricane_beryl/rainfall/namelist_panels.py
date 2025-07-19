# namelist file in other to change only the paths instead of panels.py files

initial_day = '2024-07-03T00'

# initial_day = '2024-07-01T00'
final_day = '2024-07-09T00'

label_data_era5 = 'ERA5'
label_data_gpm = 'GPM'
label_data_control = 'CP-ON'
label_data_experiment = 'CP-02T12'

# 'CP-ON'
# 'CP-OFF'
# 'CP-1H'
# 'CP-3H'
# 'CP-6H'
# 'CP-D025'
# 'CP-D050'
# 'CPSS-ON'
# 'CP-15km'
# 'CP-60km'
# 'CP-GFS'
# 'CP-01'
# 'CP-29'
# 'CP-02T12'

maps_location = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/plots_accumulated/single_march_10/'

# REFERENCE DATA:
PATH_ERA5 = maps_location+ f'Accumulated_Precipitation{label_data_era5}_{initial_day}_{final_day}.png'
PATH_GPM = maps_location + f'Accumulated_Precipitation{label_data_gpm}_{initial_day}_{final_day}.png'
    
PATH_CONTROL = maps_location+ f'Accumulated_Precipitation{label_data_control}_{initial_day}_{final_day}.png'
PATH_EXPERIMENT = maps_location+ f'Accumulated_Precipitation{label_data_experiment}_{initial_day}_{final_day}.png'

save_panel_dir = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/plots_accumulated/panels_march_10/'
save_name = f'Acc_{label_data_experiment}_{label_data_control}_{initial_day}_{final_day}.png'