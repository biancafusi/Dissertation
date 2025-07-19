import os
import numpy as np
import subprocess

# call module load imagemagick-7.0.8-7-gcc-11.2.0-46pk2go

def making_a_animation(initial_step, final_step, PATH_GPM, PATH_CONTROL, PATH_EXPERIMENT, save_dir, prefix_name):

    GPM = os.listdir(PATH_GPM)
    GPM.sort()
    CONTROL = os.listdir(PATH_CONTROL)
    CONTROL.sort()
    EXPERIMENT = os.listdir(PATH_EXPERIMENT)
    EXPERIMENT.sort()

    for i in  np.arange(initial_step,final_step, 1):
        each_GPM = PATH_GPM +  f'{GPM[i]}'
        each_CONTROL = PATH_CONTROL +  f'{CONTROL[i]}'
        each_EXPERIMENT = PATH_EXPERIMENT +  f'{EXPERIMENT[i]}'

        save_name = f'{prefix_name}{str(i).zfill(3)}'+'.png'

        command =[
            "montage", "-tile", "1x3", "-geometry", "+6+3", 
            f'{each_GPM}', f'{each_CONTROL}', f'{each_EXPERIMENT}', save_dir+save_name
        ]

        subprocess.run(command)
    
    print('Done!')

def making_simple_panel(PATH_GPM, PATH_CONTROL, PATH_EXP1, PATH_EXP2, save_dir, save_name):
    command = [
            "montage", "-tile", "2x2", "-geometry", "+6+3",
            f'{PATH_GPM}', f'{PATH_CONTROL}', f'{PATH_EXP1}', f'{PATH_EXP2}', save_dir + save_name
        ]

    subprocess.run(command)

def making_diff_panel(PATH_rain, PATH_wspd, PATH_heat, save_dir, save_name):
    command = [
        "montage",
        "-tile", "1x3",
        "-geometry", "1600x1200!+2+2",  # Força todas as imagens a terem 800x600 pixels com 2 pixels de espaçamento
        f'{PATH_rain}', f'{PATH_wspd}', f'{PATH_heat}', 
        save_dir + save_name
    ]
    subprocess.run(command)

# ======================== PANEL 01 NAMELIST ================================================ #

# making_a_animation(44, 81,
#                    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_01/GPM/',
#                    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_01/CP-OFF/',
#                    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_01/CP-ON/',
#                    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_01/montage/',
#                    'panel01_')

# ======================== PANEL 02 NAMELIST ================================================ #

# making_simple_panel(
#     '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_01/GPM/rain043.png',
#     '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_01/CP-ON/rain043.png',
#     '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_02/CP-60km/rain043.png',
#     '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_02/CP-15km/rain043.png',
#     '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_02/',
#     'panel02.png'
# )

# ======================== PANEL 03 NAMELIST ================================================ #

making_diff_panel(
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_01/CP-OFF/rain043.png',
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_03/CP-OFF_WSPD/rain043.png',
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_03/CP-OFF_HEAT/rain043.png',
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_03/',
    'CP_OFF_panel3.png'
)

making_diff_panel(
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_03/DIFF_RAIN/rain043.png',
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_03/DIFF_WSPD/rain043.png',
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_03/DIFF_HEAT/rain043.png',
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_03/',
    'DIFF_ON_panel3.png'
)

# ======================== PANEL 04 NAMELIST ================================================ #

making_diff_panel(
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_01/CP-ON/rain043.png',
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_04/CP-ON_WSPD/rain043.png',
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_04/CP-ON_HEAT/rain043.png',
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_04/',
    'CP_ON_panel4.png'
)

making_diff_panel(
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_04/DIFF_RAIN/rain043.png',
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_04/DIFF_WSPD/rain043.png',
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_04/DIFF_HEAT/rain043.png',
    '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/final_panels_morphology/panel_04/',
    'DIFF_SS_panel4.png'
)