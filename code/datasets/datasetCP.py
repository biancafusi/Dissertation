import xarray as xr
import os
import numpy as np
from datetime import datetime, timedelta

#CREATES A DATASET WITH DATA FROM BRAMS

# Função para carregar arquivos NetCDF em um dataset combinado
def carregar_datasets(base_path, file_template, dates):
    datasets = []
    
    for date in dates:
        subdir = os.path.join(base_path, f"{date}-00")
        file_path = os.path.join(subdir, file_template.format(date))
        
        if os.path.exists(file_path):
            ds = xr.open_dataset(file_path, engine='netcdf4')
            day = ds.time.dt.day[24].values
            dp = ds.sel(time=ds.time.dt.day.isin([day])) 
            datasets.append(dp)
        else:
            print(f"Arquivo não encontrado: {filepath}")

    combined_dataset = xr.concat(datasets, dim='time')
    return combined_dataset


# Função para gerar uma lista de datas no formato YYYY-MM-DD
def generate_date_list(start_date, end_date):
    dates = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    
    return dates

# Diretório base onde os arquivos estão localizados
chuvosaOFF_path    = '/mnt/beegfs/saulo.freitas/runs/goamz/dataout/POSPROCESS/artigo_ago2023/IOP1_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km/'
chuvosaCP_path   = '/mnt/beegfs/saulo.freitas/runs/goamz/dataout/POSPROCESS/artigo_ago2023/IOP1_1_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km/'
secaOFF_path   = '/mnt/beegfs/saulo.freitas/runs/goamz/dataout/POSPROCESS/artigo_ago2023/IOP2_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km/'
secaCP_path  = '/mnt/beegfs/saulo.freitas/runs/goamz/dataout/POSPROCESS/artigo_ago2023/IOP2_1_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km/'
transitionOFF_path    = '/mnt/beegfs/saulo.freitas/runs/goamz/dataout/POSPROCESS/artigo_ago2023/IOP2_4_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km/'
transitionCP_path   = '/mnt/beegfs/saulo.freitas/runs/goamz/dataout/POSPROCESS/artigo_ago2023/IOP2_4_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km/'

# Modelos de nome de arquivo para cada categoria
file_template_chuvosaOFF  = 'all_extIOP1_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km-{}.nc'
file_template_chuvosaCP = 'all_extIOP1_1_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km-{}.nc' 
file_template_secaOFF  = 'all_extIOP2_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km-{}.nc'
file_template_secaCP = 'all_extIOP2_1_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km-{}.nc'
file_template_transicaoOFF  = 'all_extIOP2_4_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km-{}.nc' 
file_template_transicaoCP = 'all_extIOP2_4_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km-{}.nc'

# Períodos de interesse
dates_chuvosa = generate_date_list('2014-02-15', '2014-02-24')
dates_seca = generate_date_list('2014-09-01', '2014-09-10')
dates_transicao = generate_date_list('2014-10-01', '2014-10-10')

# Carregar e combinar datasets para cada período
ds_chuvosaCP = carregar_datasets(chuvosaCP_path, file_template_chuvosaCP, dates_chuvosa)
ds_secaCP = carregar_datasets(secaCP_path, file_template_secaCP, dates_seca)
ds_transicaoCP = carregar_datasets(transitionCP_path, file_template_transicaoCP, dates_transicao)

ds_chuvosaOFF = carregar_datasets(chuvosaOFF_path, file_template_chuvosaOFF, dates_chuvosa)
ds_secaOFF = carregar_datasets(secaOFF_path, file_template_secaOFF, dates_seca)
ds_transicaoOFF = carregar_datasets(transitionOFF_path, file_template_transicaoOFF, dates_transicao)

# Criando novos datasets com as estacoes selecionadas
output = '~/dados'

# Salvar os datasets combinados
ds_chuvosaCP.to_netcdf(os.path.join(output, 'chuvosaCP_combined.nc'))
print('salvou chuvosaCP')
ds_secaCP.to_netcdf(os.path.join(output, 'secaCP_combined.nc'))
print('salvou secaCP')
ds_transicaoCP.to_netcdf(os.path.join(output, 'transicaoCP_combined.nc'))
print('salvou transicaoCP')

ds_chuvosaOFF.to_netcdf(os.path.join(output, 'chuvosaOFF_combined.nc'))
print('salvou chuvosaOFF')
ds_secaOFF.to_netcdf(os.path.join(output, 'secaOFF_combined.nc'))
print('salvou secaOFF')
ds_transicaoOFF.to_netcdf(os.path.join(output, 'transicaoOFF_combined.nc'))
print('salvou secaOFF')

