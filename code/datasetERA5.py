import xarray as xr
import os
import numpy as np

# Carrega dataset vindos do ERA5

#CARREGA ERA5
def carregar_ERA5(filepath, dates):
    ds = xr.open_dataset(filepath, engine='netcdf4')
    time = ds.time
    filtered_ds = ds.sel(time=dates)
    return filtered_ds

def generate_ERA5dates_list(start_date, end_date):        
    # Calculate the time difference in hours
    time_delta = end_date - start_date
    num_hours = time_delta / np.timedelta64(1, 'h')
    
    # Create a range of hours (including start_date and end_date) and convert it to a list of datetime64 objects
    hourly_datetime64 = [
        start_date + np.timedelta64(i, 'h') for i in range(int(num_hours) + 1)
    ]

    return hourly_datetime64

# Dados ERA5
path_ERA5 = '/mnt/beegfs/bianca.fusinato/dados_mestrado/era5/era5_2014.nc'
path_ERA5temperature = '/mnt/beegfs/bianca.fusinato/dados_mestrado/era5/temperature.nc'

# Períodos de interesse
dates_ERA5chuvosa = generate_ERA5dates_list(np.datetime64('2014-02-16T00'), np.datetime64('2014-02-25T23'))
dates_ERA5seca = generate_ERA5dates_list(np.datetime64('2014-09-02T00:00'), np.datetime64('2014-09-11T23:00'))
dates_ERA5transicao = generate_ERA5dates_list(np.datetime64('2014-10-02T00:00'), np.datetime64('2014-11-10T23:00'))

# Carregar e combinar datasets para cada período
#ds_ERA5chuvoso = carregar_ERA5(path_ERA5, dates_ERA5chuvosa)
#ds_ERA5temperatureChuvoso = carregar_ERA5(path_ERA5temperature, dates_ERA5chuvosa)

ds_ERA5seca = carregar_ERA5(path_ERA5, dates_ERA5seca)
ds_ERA5temperatureSeca = carregar_ERA5(path_ERA5temperature, dates_ERA5seca)

#ds_ERA5transicao = carregar_ERA5(path_ERA5, dates_ERA5transicao)
#ds_ERA5temperatureTransicao = carregar_ERA5(path_ERA5temperature, dates_ERA5transicao)

output = '~/dados'

# Salvar os datasets combinados (opcional)
#ds_ERA5chuvoso.to_netcdf(os.path.join(output, 'chuvosaERA5_combined.nc'))
#ds_ERA5temperatureChuvoso.to_netcdf(os.path.join(output, 'chuvosaERA5temp_combined.nc'))
#print('ERA5 chuvoso carregado')

ds_ERA5seca.to_netcdf(os.path.join(output, 'secaERA5_combined.nc'))
ds_ERA5temperatureSeca.to_netcdf(os.path.join(output, 'secaERA5temp_combined.nc'))
print('ERA5 seco carregado')

#ds_ERA5transicao.to_netcdf(os.path.join(output, 'transicaoERA5_combined.nc'))
#ds_ERA5temperatureTransicao.to_netcdf(os.path.join(output, 'transicaoERA5temp_combined.nc'))
#print('ERA5 transicao carregado')
