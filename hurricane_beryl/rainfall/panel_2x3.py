import os
import numpy as np
import subprocess
from namelist_panels import *

def making_simple_panel(PATH_GPM, PATH_OFF, PATH_ON, PATH_1H, PATH_D025, PATH_CPSS, save_dir, save_name):
    command = [
            "montage", "-tile", "3x2", "-geometry", "+6+3",
           f'{PATH_GPM}', f'{PATH_OFF}', f'{PATH_ON}',
                f'{PATH_1H}', f'{PATH_D025}', f'{PATH_CPSS}',
              save_dir + save_name
        ]

    subprocess.run(command)


def making_a_animation(number_of_days, PATH_ERA5, PATH_CONTROL, PATH_CP_ON, save_dir, prefix_name):

    ERA5 = os.listdir(PATH_ERA5)
    ERA5.sort()
    CONTROL = os.listdir(PATH_CONTROL)
    CONTROL.sort()
    CP_ON = os.listdir(PATH_CP_ON)
    CP_ON.sort()

    for i in  np.arange(0,number_of_days):
        each_ERA5 = PATH_ERA5 +  f'{ERA5[i]}'
        each_CONTROL = PATH_CONTROL +  f'{CONTROL[i]}'
        each_CP_ON = PATH_CP_ON +  f'{CP_ON[i]}'

        save_name = f'{prefix_name}{str(i).zfill(3)}'+'.png'

        command =[
            "montage", "-tile", "1x3", "-geometry", "+6+3", 
            f'{each_ERA5}', f'{each_CONTROL}', f'{each_CP_ON}', save_dir+save_name
        ]

        subprocess.run(command)
    
    print('Done!')

def zoom_panels(variable, number_of_days, gust_front_on=None):

    if variable=='Wind':
        if gust_front_on==False:
            PATH_ERA5 = ERA5_images + 'zoom/wind/'
            PATH_CONTROL = CONTROL_images + 'zoom/wind/'
            PATH_CP_ON = CP_ON_images + 'zoom/wind/'
            
            save_dir= save_panel_dir + 'zoom/wind/'
            prefix_name = 'zoom_wind'

            making_a_animation(number_of_days, PATH_ERA5, PATH_CONTROL, PATH_CP_ON, save_dir, prefix_name)
        else:
            PATH_ERA5 = ERA5_images + 'zoom/wind/'
            PATH_CONTROL = CONTROL_images + 'zoom/wind/'
            PATH_CP_ON = CP_ON_images + 'zoom/wind_gf/'
            
            save_dir= save_panel_dir + 'zoom/wind_gf/'
            prefix_name = 'zoom_wind_gf'

            making_a_animation(number_of_days, PATH_ERA5, PATH_CONTROL, PATH_CP_ON, save_dir, prefix_name)
    
    if variable=='MSLP':
        PATH_ERA5 = ERA5_images + 'zoom/mslp/'
        PATH_CONTROL = CONTROL_images + 'zoom/mslp/'
        PATH_CP_ON = CP_ON_images + 'zoom/mslp/'
        
        save_dir= save_panel_dir + 'zoom/mslp/'
        prefix_name = 'zoom_mslp'            
        
        making_a_animation(number_of_days, PATH_ERA5, PATH_CONTROL, PATH_CP_ON, save_dir, prefix_name)

def simple_panels(variable, number_of_days, gust_front_on=None):
    
    if variable=='Wind':
        
        if gust_front_on==False:
            PATH_ERA5 = ERA5_images + 'wind/'
            PATH_CONTROL = CONTROL_images + 'wind/'
            PATH_CP_ON = CP_ON_images + 'wind/'
            
            save_dir= save_panel_dir + 'wind/'
            prefix_name = 'wind'

            making_a_animation(number_of_days, PATH_ERA5, PATH_CONTROL, PATH_CP_ON, save_dir, prefix_name)
        else:
            PATH_ERA5 = ERA5_images + 'wind/'
            PATH_CONTROL = CONTROL_images + 'wind/'
            PATH_CP_ON = CP_ON_images + 'wind_gf/'
            
            save_dir= save_panel_dir + 'wind_gf/'
            prefix_name = 'wind_gf'

            making_a_animation(number_of_days, PATH_ERA5, PATH_CONTROL, PATH_CP_ON, save_dir, prefix_name)
    
    if variable=='MSLP':
        PATH_ERA5 = ERA5_images + 'mslp/'
        PATH_CONTROL = CONTROL_images + 'mslp/'
        PATH_CP_ON = CP_ON_images + 'mslp/'
        
        save_dir= save_panel_dir + 'mslp/'
        prefix_name = 'mslp'            
        
        making_a_animation(number_of_days, PATH_ERA5, PATH_CONTROL, PATH_CP_ON, save_dir, prefix_name)

# to call the  gif (com ImageMagick): convert -delay 50  -loop  0 *.png -quality 300 gif_mslp.gif

making_simple_panel('/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/plots_accumulated/single/Accumulated_PrecipitationGPM_2024-07-03T00_2024-07-09T00.png',
                    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/plots_accumulated/single/Accumulated_PrecipitationCP-OFF_2024-07-03T00_2024-07-09T00.png',
                    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/plots_accumulated/single/Accumulated_PrecipitationCP-ON_2024-07-03T00_2024-07-09T00.png',
                    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/plots_accumulated/single/Accumulated_PrecipitationCP-1H_2024-07-03T00_2024-07-09T00.png',
                    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/plots_accumulated/single/Accumulated_PrecipitationCP-D025_2024-07-03T00_2024-07-09T00.png',
                    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/plots_accumulated/single/Accumulated_PrecipitationCPSS-ON_2024-07-03T00_2024-07-09T00.png',
                    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/accumulated/',
                    'panel_meeting_march.png')