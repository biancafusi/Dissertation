import numpy as np

'''
Developed by Bianca Fusinato.
READ ME:
            lonW, lonE, latS, latN =        Insert the lat/lon numbers. Dont forget the minus sign when necessary
            initial_time =                  Insert the initial time of the experiment being at Y-M-DTH:M format
            final_time =                    Insert the final time of the experiment being at Y-M-DTH:M format
            label_experiment =              Str that contains the experiment label (ID). Will appears at the graph
            label_control =                 Str that contains the control label (ID). Will appears at the graph
            control_color =                 Str that contains the color for the control data. Will appears at the graph
            graph_title =                   Str that contains the graph title
            saving_name =                   Str that contains the file name for the plot. Insert .png at the end
            table_save_name =               Str that contains the file name for the table. The default output is .csv
            excel_spreadsheet_name =        Str that contains the file name for the table at 'xlsx' format
            data_location =                 Str that contains the location of the data. With doesnt apply, comment this line
            where_save =                    Str that contains the location for saving the plot
            NOAA_path =                     Str that contains the .nc file name for the NOAA data.
            ERA5_path =                     Str that contains the .nc file name for the ERA5 data.
            CONTROL_path =                  Str that contains the .nc file name for the Control data.
            EXPERIMENT_path =               Str that contains the .nc file name for the Experiment data.

Obs.: One could add another type of data, such as 'GPM_path'. If data_location is commented, insert at all data paths
the full data path name, for example 'home/Documents/Data/GPM/.

Obs.2: The functions defined here are being used only at 'making_tables.py' and 'making_tables_excel.py'

'''

lonW, lonE, latS, latN = -106, -70, 13, 37

# initial_day = '2024-07-01T00'
initial_day = '2024-07-03T00'
final_day = '2024-07-09T00'
# final_day = '2024-07-04T23'

label_control = 'CONTROL'
                # OPTIONS:
                # 'CP-OFF'
                # 'CONTROL'
                # 'CP-03'
                # 'CP-ERA5'
                # 'CP-30km'
                # 'CP-ERA5-1H'

label_experiment =  'CP-60km'
                    # OPTIONS:
                    # 'CP-ON'
                    # 'CP-1H'
                    # 'CP-3H'
                    # 'CP-6H'
                    # 'CP-D025'
                    # 'CP-D050'
                    # 'CPSS-ON'
                    # 'CP-29'
                    # 'CP-01'
                    # 'CP-02T12'
                    # 'CP-GFS'
                    # 'CP-15km'
                    # 'CP-GFS-1H'
                    # 'CP-60km'

convertion_to_180 = 'ON'
different_day = 'OFF'

################################################# GRAPHIC SETTINGS ##############################

saving_name = f'Beryl_{label_control}_{label_experiment}_init_{initial_day}.png'
graph_title = 'Minimum MSLP track by NOAA, ERA5 and Model'
# table_save_name = 'testing_table'
# excel_spreadsheet_name = 'testing_excel'


# # REFERENCE DATA PATH:

NOAA_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/time_series/beryl.nc'
ERA5_path= '/mnt/beegfs/bianca.fusinato/monan/comparison/ERA5/era5_dry.nc'
# ERA5_path_wind_100m = ''
# ERA5_path_wind_gf_instanteneous = ''

# # MODEL DATA PATH:

data_location = '/mnt/beegfs/bianca.fusinato/monan/model/'

if initial_day == '2024-07-01T00':

    where_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/pathing/outputs_spin_up/'

    if label_control == 'CP-OFF':

        control_color = 'black'
        experiment_color = 'red'

        CONTROL_path = data_location + 'beryl_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'
        EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'

    else:    
        control_color = 'red'
        experiment_color = 'purple'

        CONTROL_path = data_location + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'
        
        if label_experiment == 'CP-1H':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_TCP1H_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'

        elif label_experiment == 'CP-3H':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_TCP3H_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'

        elif label_experiment == 'CP-6H':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_TCP30MN_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'

        elif label_experiment == 'CP-D025':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_DOW025_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'

        elif label_experiment == 'CP-D050':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_DOW050_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'

        elif label_experiment == 'CPSS-ON':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf2_sub3d0_GFdef_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'
            

####################### JULY 3rd INITIALIZATION ########################################################

elif initial_day == '2024-07-03T00':
    
    where_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/pathing/output_10_march/'

    if label_control == 'CP-OFF':

        control_color = 'black'
        experiment_color = 'red'

        CONTROL_path = data_location + 'beryl_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'
        EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'
    
    elif label_control == 'CP-ERA5-1H':
        where_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/pathing/outputs_GFS/'
        control_color = 'red'
        experiment_color = 'purple'
        
        CONTROL_path = data_location + 'beryl_cporg1_gustf1_sub3d0_TCP1H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'
        EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_TCP1H_GFS_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'    
    
    elif label_control == 'CP-OFF-ERA5':
        where_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/pathing/outputs_GFS/'
        control_color = 'red'
        experiment_color = 'purple'

        CONTROL_path ='/mnt/beegfs/bianca.fusinato/monan/model/beryl_cporg0_gustf0_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'
        EXPERIMENT_path = '/mnt/beegfs/bianca.fusinato/monan/model/beryl_cporg0_gustf0_sub3d0_GFdef_GFS_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'
    # elif label_control == 'CP-ERA5':
    #     where_save = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/pathing/outputs_GFS/'
    #     control_color = 'red'
    #     experiment_color = 'purple'
        
    #     CONTROL_path = data_location + 'beryl_cporg1_gustf1_sub3d0_TCP1H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'
    #     EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_TCP1H_GFS_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'    

    else:

        control_color = 'red'
        experiment_color = 'purple'

        CONTROL_path = data_location + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

        if label_experiment == 'CP-1H':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_TCP1H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

        elif label_experiment == 'CP-3H':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_TCP3H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

        elif label_experiment == 'CP-6H':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_TCP6H_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

        elif label_experiment == 'CP-D025':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_DOW025_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

        elif label_experiment == 'CP-D050':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_DOW050_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

        elif label_experiment == 'CPSS-ON':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf2_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'
        
        elif label_experiment == 'CP-GFS':
            EXPERIMENT_path = '/mnt/beegfs/bianca.fusinato/monan/model/GFS_run/beryl_cporg1_gustf1_sub3d0_GFdef_GFS_x1.655362/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

        elif label_experiment == 'CP-15km':
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.2621442/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

        elif label_experiment == 'CP-60km':
            EXPERIMENT_path = data_location + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.163842/2024070300/diag/all_diag_dc.2024-07-03_00.00.00.nc'

        elif label_experiment == 'CP-29':
            new_day = '2024-06-29T00'
            graph_title = 'MSLP track by NOAA and two different IC'

            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024062900/diag/all_diag_dc.2024-06-29_00.00.00.nc'
        
        elif label_experiment == 'CP-01':
            new_day = '2024-07-01T00'
            graph_title = 'MSLP track by NOAA and two different IC'
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070100/diag/all_diag_dc.2024-07-01_00.00.00.nc'

        elif label_experiment == 'CP-02T12':
            new_day = '2024-07-02T12'
            graph_title = 'MSLP track by NOAA and two different IC'
            EXPERIMENT_path =  data_location + 'beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070212/diag/all_diag_dc.2024-07-02_12.00.00.nc'






