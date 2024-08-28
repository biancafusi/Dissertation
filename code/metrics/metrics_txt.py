import numpy as np
import os
import matplotlib.pyplot as plt
from org_indices import *

'''
Made by: Bianca Fusinato
This code computes the organization indexes in .txt
in two different ways
'''

def calculate_all_indices(cnv_idx_dir, indices_range, output_file, prefix):
    """
    Calculates the indeces and saves as a .txt
    """
    rmax = 218  
    dxy = 1
    bin_w = 2*dxy
    bins = np.arange(0, rmax + bin_w * dxy, bin_w * dxy)


    with open(output_file, 'w') as f:
        for idx in indices_range:
            cnv_idx_path = os.path.join(cnv_idx_dir, f'cnv_{prefix}_{idx}.npy')
            
            
            if os.path.exists(cnv_idx_path):
                try:
                    cnv_idx = np.load(cnv_idx_path)

                    I_org, RI_org, L_org, NNCDF_theor, NNCDF_obs, Besag_theor, Besag_obs, OII = calculate_indices(
                        dxy=dxy, cnv_idx=cnv_idx, rmax=rmax, bins=bins, periodic_BCs=False,
                        periodic_zonal=False, clustering_algo=False, binomial_continuous=False,
                        binomial_discrete=True, edge_mode='besag'
                    )

                    print(f'Calculado índice {idx}')

                    f.write(f'Indice {idx}:\n')
                    f.write(f'I_org: {I_org}\n')
                    f.write(f'RI_org: {RI_org}\n')
                    f.write(f'L_org: {L_org}\n')
                    f.write(f'OII: {OII}\n')
                    f.write(f'Besag_obs: {Besag_obs}\n')
                    f.write(f'Besag_theor: {Besag_theor}\n')
                    f.write('\n')

                except Exception as e:
                    print(f'Erro ao processar índice {idx}: {str(e)}')
                    continue 

            else:
                print(f'Arquivo não encontrado para o índice {idx}')

    print(f'Resultados salvos!')

def indices_varying_rmax(cnv_idx_dir, indices_range, output_file, prefix):
    """
    Calculates the indices for varying rmax values and saves them as a .txt.
    """
    rmax = 218 
    dxy = 1
    bin_w = 2 * dxy

    result_matrix = []
    with open(output_file, 'w') as f:
        for idx in indices_range:
            cnv_idx_path = os.path.join(cnv_idx_dir, f'cnv_{prefix}_{idx}.npy')
            
            if os.path.exists(cnv_idx_path):
                try:
                    cnv_idx = np.load(cnv_idx_path)
                    rmax_results = []
                    for rmax in range(0,218, 1):  # Loop sobre os valores de rmax
                        rmax=rmax+.1
                        bins = np.arange(1, rmax + bin_w * dxy, bin_w * dxy)
                        
                        try:
                            I_org, RI_org, L_org, NNCDF_theor, NNCDF_obs, Besag_theor, Besag_obs, OII = calculate_indices(
                                dxy=dxy, cnv_idx=cnv_idx, rmax=rmax, bins=bins, periodic_BCs=False,
                                periodic_zonal=False, clustering_algo=False, binomial_continuous=False,
                                binomial_discrete=True, edge_mode='besag'
                            )
                        except ZeroDivisionError:
                            L_org = 0  # Tratar resultado como 0 se ocorrer divisão por zero

                        rmax_results.append(L_org)  

                    result_matrix.append(rmax_results)  

                    print(f'Calculado índice {idx}')

                    # Escreve os resultados para o índice atual
                    f.write(f'Time index {idx}:\n')
                    f.write(f'L_org = {rmax_results}\n')
                    f.write('\n')

                except Exception as e:
                    print(f'Erro ao processar índice {idx}: {str(e)}')
                    continue 

            else:
                print(f'Arquivo não encontrado para o índice {idx}')

    print(f'Resultados salvos!')

input_cnv_dict = {
    "january2013": "/home/bianca.fusinato/output/binary_matrix/january2013/",
    "january2014": "/home/bianca.fusinato/output/binary_matrix/january2014/",
    "january2015": "/home/bianca.fusinato/output/binary_matrix/january2015/",
    "february2013":'/home/bianca.fusinato/output/binary_matrix/february2013',
    "february2014":'/home/bianca.fusinato/output/binary_matrix/february2014',
    "february2015":'/home/bianca.fusinato/output/binary_matrix/february2015',
    "march2013": "/home/bianca.fusinato/output/binary_matrix/march2013/",
    "march2014": "/home/bianca.fusinato/output/binary_matrix/march2014/",
    "march2015": "/home/bianca.fusinato/output/binary_matrix/march2015/",
    "august2013": "/home/bianca.fusinato/output/binary_matrix/august2013/",
    "august2014": "/home/bianca.fusinato/output/binary_matrix/august2014/",
    "august2015": "/home/bianca.fusinato/output/binary_matrix/august2015/",
    "september2013": "/home/bianca.fusinato/output/binary_matrix/september2013/",
    "september2014": "/home/bianca.fusinato/output/binary_matrix/september2014/",
    "september2015": "/home/bianca.fusinato/output/binary_matrix/september2015/",
    "october2013": "/home/bianca.fusinato/output/binary_matrix/october2013/",
    "october2014": "/home/bianca.fusinato/output/binary_matrix/october2014/",
    "october2015": "/home/bianca.fusinato/output/binary_matrix/october2015/"
}

output_metric_dict = {
    "january2013": '/home/bianca.fusinato/output/metrics/2013january.txt',
    "january2014": '/home/bianca.fusinato/output/metrics/2014january.txt',
    "january2015": '/home/bianca.fusinato/output/metrics/2015january.txt',
    "february2013":'/home/bianca.fusinato/output/metrics/2013february.txt',
    "february2014":'/home/bianca.fusinato/output/metrics/2014february.txt',
    "february2015":'/home/bianca.fusinato/output/metrics/2015february.txt',
    "march2013": '/home/bianca.fusinato/output/metrics/2013march.txt',
    "march2014": '/home/bianca.fusinato/output/metrics/2014march.txt',
    "march2015": '/home/bianca.fusinato/output/metrics/2015march.txt',
    "august2013": '/home/bianca.fusinato/output/metrics/2013august.txt',
    "august2014": '/home/bianca.fusinato/output/metrics/2014august.txt',
    "august2015": '/home/bianca.fusinato/output/metrics/2015august.txt',
    "september2013": '/home/bianca.fusinato/output/metrics/2013september.txt',
    "september2014": '/home/bianca.fusinato/output/metrics/2014september.txt',
    "september2015": '/home/bianca.fusinato/output/metrics/2015september.txt',
    "october2013": '/home/bianca.fusinato/output/metrics/2013october.txt',
    "october2014": '/home/bianca.fusinato/output/metrics/2014october.txt',
    "october2015": '/home/bianca.fusinato/output/metrics/2015october.txt'
}

time_indices_dict = {
    "january": range(0, 744),
    "february": range(0, 672),
    "march": range(0, 744),
    "august": range(0, 744),
    "september": range(0, 720),
    "october": range(0, 744),
}

calculate_all_indices(input_cnv_dict["january2013"],time_indices_dict["january"],output_metric_dict["january2013"],prefix='ERA5')
calculate_all_indices(input_cnv_dict["january2014"],time_indices_dict["january"],output_metric_dict["january2014"],prefix='ERA5')
calculate_all_indices(input_cnv_dict["january2015"],time_indices_dict["january"],output_metric_dict["january2015"],prefix='ERA5')

calculate_all_indices(input_cnv_dict["february2013"],time_indices_dict["february"],output_metric_dict["february2013"],prefix='ERA5')
calculate_all_indices(input_cnv_dict["february2014"],time_indices_dict["february"],output_metric_dict["february2014"],prefix='ERA5')
calculate_all_indices(input_cnv_dict["february2015"],time_indices_dict["february"],output_metric_dict["february2015"],prefix='ERA5')

calculate_all_indices(input_cnv_dict["march2013"],time_indices_dict["march"],output_metric_dict["march2013"],prefix='ERA5')
calculate_all_indices(input_cnv_dict["march2014"],time_indices_dict["march"],output_metric_dict["march2014"],prefix='ERA5')
calculate_all_indices(input_cnv_dict["march2015"],time_indices_dict["march"],output_metric_dict["march2015"],prefix='ERA5')

calculate_all_indices(input_cnv_dict["august2013"],time_indices_dict["august"],output_metric_dict["august2013"],prefix='ERA5')
calculate_all_indices(input_cnv_dict["august2014"],time_indices_dict["august"],output_metric_dict["august2014"],prefix='ERA5')
calculate_all_indices(input_cnv_dict["august2015"],time_indices_dict["august"],output_metric_dict["august2015"],prefix='ERA5')

calculate_all_indices(input_cnv_dict["september2013"],time_indices_dict["september"],output_metric_dict["september2013"],prefix='ERA5')
calculate_all_indices(input_cnv_dict["september2014"],time_indices_dict["september"],output_metric_dict["september2014"],prefix='ERA5')
calculate_all_indices(input_cnv_dict["september2015"],time_indices_dict["september"],output_metric_dict["september2015"],prefix='ERA5')

calculate_all_indices(input_cnv_dict["october2013"],time_indices_dict["october"],output_metric_dict["october2013"],prefix='ERA5')
calculate_all_indices(input_cnv_dict["october2014"],time_indices_dict["october"],output_metric_dict["october2014"],prefix='ERA5')
calculate_all_indices(input_cnv_dict["october2015"],time_indices_dict["october"],output_metric_dict["october2015"],prefix='ERA5')