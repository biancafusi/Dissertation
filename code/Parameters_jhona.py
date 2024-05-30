import xarray as xr
import os
import numpy as np

#from datetime import #datetime, timedelta

# Função para carregar arquivos NetCDF em um dataset combinado
def carregar_datasets(base_path, file_template, dates):
    datasets = []
    
    for date in dates:
        subdir = os.path.join(base_path, f"{date}-00")
        file_path = os.path.join(subdir, file_template.format(date))
        
        if os.path.exists(file_path):
            ds = xr.open_dataset(file_path, engine='netcdf4')
            #ds_filter = ds[(ds.dt.hour >= 9) & (ds.dt.hour <= 15)]
            #dp = ds[24:49, :, :, :, :]
            #datasets.append(dp)
            #print(ds[ds.time.dt.hour)
            #print(ds.sel(time=ds.time.dt.hour.isin([24])) )
            #print(ds.time.dt.day)
            day = ds.time.dt.day[24].values
            dp = ds.sel(time=ds.time.dt.day.isin([day])) 
            datasets.append(dp)
        else:
            print(f"Arquivo não encontrado: {filepath}")

    combined_dataset = xr.concat(datasets, dim='time')
    return combined_dataset

#CARREGA ERA5
def carregar_ERA5(filepath, dates):
    ds = xr.open_dataset(filepath, engine='netcdf4')
    time = ds.time
    filtered_ds = ds.sel(time=dates)
    return filtered_ds

# Função para gerar uma lista de datas no formato YYYY-MM-DD
def generate_date_list(start_date, end_date):
    from datetime import datetime, timedelta
    dates = []
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    
    return dates

def generate_ERA5dates_list(start_date, end_date):        
    # Calculate the time difference in hours
    time_delta = end_date - start_date
    num_hours = time_delta / np.timedelta64(1, 'h')
    
    # Create a range of hours (including start_date and end_date) and convert it to a list of datetime64 objects
    hourly_datetime64 = [
        start_date + np.timedelta64(i, 'h') for i in range(int(num_hours) + 1)
    ]

    return hourly_datetime64

#def generate_ERA5dates_list(start_date, end_date):
    # Generate the range of datetime64 values with one hour increments
#    datetimes = np.arange(start_date, end_date, np.timedelta64(1, 'h'))
#    print(datetimes.tolist())
#    for dt in datetimes.tolist():
#        print(dt, type(dt))

    # Convert the numpy array to a list
#    return datetimes.tolist()

# Diretório base onde os arquivos estão localizados
chuvosaCP_path    = '/mnt/beegfs/saulo.freitas/runs/goamz/dataout/POSPROCESS/artigo_ago2023/IOP1_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km/'
chuvosaOFF_path   = '/mnt/beegfs/saulo.freitas/runs/goamz/dataout/POSPROCESS/artigo_ago2023/IOP1_1_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km/'
secaCP_path   = '/mnt/beegfs/saulo.freitas/runs/goamz/dataout/POSPROCESS/artigo_ago2023/IOP2_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km/'
secaOFF_path  = '/mnt/beegfs/saulo.freitas/runs/goamz/dataout/POSPROCESS/artigo_ago2023/IOP2_1_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km/'
transitionCP_path    = '/mnt/beegfs/saulo.freitas/runs/goamz/dataout/POSPROCESS/artigo_ago2023/IOP2_4_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km/'
transitionOFF_path   = '/mnt/beegfs/saulo.freitas/runs/goamz/dataout/POSPROCESS/artigo_ago2023/IOP2_4_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km/'

# Modelos de nome de arquivo para cada categoria
file_template_chuvosaCP  = 'all_extIOP1_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km-{}.nc'
file_template_chuvosaOFF = 'all_extIOP1_1_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km-{}.nc' 
file_template_secaCP  = 'all_extIOP2_1_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km-{}.nc'
file_template_secaOFF = 'all_extIOP2_1_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km-{}.nc'
file_template_transicaoCP  = 'all_extIOP2_4_MP5_dc1_CNV00_E6.3_usem0_triggCIN2_Mx08km-{}.nc' 
file_template_transicaoOFF = 'all_extIOP2_4_MP5_dc1_CNV12_E6.3_usem0_triggCIN2_Mx08km-{}.nc'

# Dados ERA5
path_ERA5 = '/mnt/beegfs/bianca.fusinato/dados_mestrado/era5/era5_2014.nc'

# Períodos de interesse
dates_chuvosa = generate_date_list('2014-02-15', '2014-02-24')
dates_seca = generate_date_list('2014-09-01', '2014-09-10')
dates_transicao = generate_date_list('2014-10-01', '2014-10-10')

dates_ERA5chuvosa = generate_ERA5dates_list(np.datetime64('2014-02-15T00'), np.datetime64('2014-02-24T23'))
#dates_ERA5seca = generate_ERA5dates_list('2014-09-01T00:00', '2014-09-10T23:00')
#dates_ERA5transicao = generate_ERA5dates_list('2014-10-01T00:00', '2014-10-10T23:00')


# Carregar e combinar datasets para cada período
#ds_chuvosaCP = carregar_datasets(chuvosaCP_path, file_template_chuvosaCP, dates_chuvosa)

#ds_secaCP = carregar_datasets(secaCP_path, file_template_secaCP, dates_seca)

#ds_transicaoCP = carregar_datasets(transitionCP_path, file_template_transicaoCP, dates_transicao)

ds_ERA5chuvoso = carregar_ERA5(path_ERA5, dates_ERA5chuvosa)
# Imprimir informações dos datasets combinados
#print("Chuvosa:", ds_chuvosa)
#print("Seca:", ds_seca)
#print("Transição:", ds_transicao)

output = '~/dados'

# Salvar os datasets combinados (opcional)
#ds_chuvosaCP.to_netcdf(os.path.join(output, 'chuvosaCP_combined.nc'))
#ds_secaCP.to_netcdf(os.path.join(output, 'secaCP_combined.nc'))
#ds_transicaoCP.to_netcdf(os.path.join(output, 'transicaoCP_combined.nc'))
ds_ERA5chuvoso.to_netcdf(os.path.join(output, 'chuvosaERA5_combined.nc'))
