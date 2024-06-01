import xarray as xr
import os
import numpy as np
from datetime import datetime, timedelta

# Cria dataset com os dados vindos do GPM-IMERG

def generate_GPMdate_list(start_date, end_date):
    dates = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current_date <= end_date:
        for hour in range(24):
            for minute in [0, 30]:
                date_str = current_date.strftime('%Y%m%d')
                hour_str = f'S{hour:02d}{minute:02d}00'
                dates.append(f'{date_str}-{hour_str}')
        current_date += timedelta(days=1)
    
    return dates #OK

# Função para encontrar o arquivo completo com base no prefixo
def encontrar_arquivo_completo(base_path, prefix):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.startswith(prefix):
                return os.path.join(root, file)
    return None #OK

def carregar_GPM(base_path, file_template, dates):
    datasets = []
    
    for i in range(0, len(dates), 2):
        date1 = dates[i]
        date2 = dates[i + 1]
        
        prefix1 = file_template.format(date1)
        prefix2 = file_template.format(date2)
        
        file_path1 = encontrar_arquivo_completo(base_path, prefix1)
        #print(f'o caminho do primeiro eh: {file_path1}')
        file_path2 = encontrar_arquivo_completo(base_path, prefix2)
        #print(f'o caminho do segundo eh: {file_path2}')
        #print('  ')
        #exit()
        if os.path.exists(file_path1) and os.path.exists(file_path2):
            ds1 = xr.open_dataset(file_path1, engine='netcdf4')
            ds2 = xr.open_dataset(file_path2, engine='netcdf4')
            
            # Calcula o acumulado e a média de precipitação
            precip_acumulado = ds1.precipitation[0,:,:] + ds2.precipitation[0,:,:]
            
            #print(f'dados acumulado:{precip_acumulado}')
            #print(f'tipo do dado acumulado:{type(precip_acumulado)}')
            #exit()
            precip_media = precip_acumulado[:,:] / 2
            
            # Cria um novo dataset para armazenar os resultados
            ds_result = xr.Dataset(
            
                {
                    'precip_acumulado': precip_acumulado[:,:],
                    'precip_media': precip_media[:,:]
                },
                coords=ds1.coords
            )
            datasets.append(ds_result)
        else:
            if not os.path.exists(file_path1):
                print(f"Arquivo não encontrado: {file_path1}")
            if not os.path.exists(file_path2):
                print(f"Arquivo não encontrado: {file_path2}")

    combined_dataset = xr.concat(datasets, dim='time')
    return combined_dataset

# Diretório GPM
path_GPM = '/mnt/beegfs/bianca.fusinato/dados_mestrado/gpm-imerg'
file_template_GPM = '3B-HHR.MS.MRG.3IMERG.{}'

# Períodos de interesseSOMEI 24 HR PRA COMPARAR COM BRAMS
dates_chuvosa = generate_GPMdate_list('2014-02-16', '2014-02-25')
dates_seca = generate_GPMdate_list('2014-09-02', '2014-09-11')
dates_transicao = generate_GPMdate_list('2014-10-02', '2014-10-11')

# Carrega e processa os dados
ds_GPMchuvoso = carregar_GPM(path_GPM, file_template_GPM, dates_chuvosa)
ds_GPMseco = carregar_GPM(path_GPM, file_template_GPM, dates_seca)
ds_GPMtransicao = carregar_GPM(path_GPM, file_template_GPM, dates_transicao)

# Salva os resultados
output_path = '~/dados/'

ds_GPMchuvoso.to_netcdf(os.path.join(output_path, 'chuvosaGPM_combined.nc'))
print('carregou a chuvosa')

ds_GPMseco.to_netcdf(os.path.join(output_path, 'secaGPM_combined.nc'))
print('carregou a seca')

ds_GPMtransicao.to_netcdf(os.path.join(output_path, 'transicaoGPM_combined.nc'))
print('carregou a transicao')



