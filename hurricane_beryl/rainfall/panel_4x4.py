import os
import numpy as np
import subprocess
from namelist_panels import *

# call module load imagemagick-7.0.8-7-gcc-11.2.0-46pk2go

def making_simple_panel(PATH_ERA5, PATH_GPM, PATH_CONTROL, PATH_EXPERIMENT, save_dir, save_name):
    command = [
            "montage", "-tile", "2x2", "-geometry", "+6+3",
            f'{PATH_ERA5}', f'{PATH_GPM}', f'{PATH_CONTROL}', f'{PATH_EXPERIMENT}', save_dir + save_name
        ]

    subprocess.run(command)

def making_an_animation(PATH_ERA5, PATH_GPM, PATH_CONTROL, PATH_CP_ON, number_of_days, save_dir, prefix_name):

    ERA5 = os.listdir(PATH_ERA5)
    ERA5.sort()
    GPM = os.listdir(PATH_GPM)
    GPM.sort()
    CONTROL = os.listdir(PATH_CONTROL)
    CONTROL.sort()
    CP_ON = os.listdir(PATH_CP_ON)
    CP_ON.sort()

    for i in  np.arange(0, number_of_days):

        each_ERA5 = PATH_ERA5 +  f'{ERA5[i]}'
        each_GPM = PATH_GPM +  f'{GPM[i]}'
        each_CONTROL = PATH_CONTROL +  f'{CONTROL[i]}'
        each_CP_ON = PATH_CP_ON +  f'{CP_ON[i]}'

        save_name =f'{prefix_name}{str(i).zfill(3)}'+'.png'
        
        command = [
            "montage", "-tile", "2x2", "-geometry", "+6+3",
            f'{each_ERA5}', f'{each_GPM}', f'{each_CONTROL}', f'{each_CP_ON}', save_dir + save_name
        ]

        subprocess.run(command)
    
    print('Done!')
    
def zoom_panel4x4(number_of_days):
    PATH_ERA5 = ERA5_images + 'zoom/rain/'
    PATH_GPM = GPM_images + 'zoom/rain/'
    PATH_CONTROL = CONTROL_images + 'zoom/rain/'
    PATH_CP_ON = CP_ON_images + 'zoom/rain/'
    
    save_dir = save_panel_dir + 'zoom/rain/'
    prefix_name = 'zoom_rain'

    making_an_animation(PATH_ERA5, PATH_GPM, PATH_CONTROL, PATH_CP_ON, number_of_days, save_dir,  prefix_name)
    

def panel4x4(number_of_days):
    PATH_ERA5 = ERA5_images + 'rain/'
    PATH_GPM = GPM_images + 'rain/'
    PATH_CONTROL = CONTROL_images + 'rain/'
    PATH_CP_ON = CP_ON_images + 'rain/'
    
    save_dir = save_panel_dir + 'rain/'
    prefix_name = 'rain'
    
    making_an_animation(PATH_ERA5, PATH_GPM, PATH_CONTROL, PATH_CP_ON, number_of_days, save_dir,  prefix_name)


making_simple_panel(PATH_ERA5, PATH_GPM, PATH_CONTROL, PATH_EXPERIMENT, save_panel_dir, save_name)