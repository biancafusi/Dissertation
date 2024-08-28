import os
import numpy as np
from   org_indices import *
import matplotlib.pyplot as plt
import logging
import Parameters as Pa

def call_funtion(part):

    logging.info("Thread %s: starting", part)
    f.indices_varying_rmax(Pa.data_era5, part,Pa.out_era5+'/%s'%part, prefix='ERA5')
    logging.info("Thread %s: finishing", part)

    return


def calculate_all_indices(cnv_idx_dir, part, output_file, prefix):


    """
    Calculates the indeces and saves as a .txt
    """
    rmax = 218  
    dxy = 1
    bin_w = 2*dxy
    bins = np.arange(0, rmax + bin_w * dxy, bin_w * dxy)


    with open(output_file, 'w') as f:
        #for idx in indices_range:
        
        print(int(part[1]))
        exit()
        for idx in range(int(part[0]),int(part[1])):
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

    return

def indices_varying_rmax(cnv_idx_dir, part, output_file, prefix):
    """
    Calculates the indices for varying rmax values and saves them as a .txt.
    """
    rmax = 218 
    dxy = 1
    bin_w = 2 * dxy

    result_matrix = []
    with open(output_file, 'w') as f:
        for idx in range(int(part[0]),int(part[1])): #loop  do tempo (so muda com meses)
            cnv_idx_path = os.path.join(cnv_idx_dir, f'cnv_{prefix}_{idx}.npy')
            
            if os.path.exists(cnv_idx_path):
                try:
                    cnv_idx = np.load(cnv_idx_path)
                    rmax_results = []
                    for rmax in range(0,rmax, 1):  # Loop sobre os valores de rmax
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
                    print('oi')

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

    return
