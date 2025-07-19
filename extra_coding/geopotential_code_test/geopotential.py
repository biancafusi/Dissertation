import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib
import numpy as np
from matplotlib import cm
from matplotlib.colors import BoundaryNorm, TwoSlopeNorm, ListedColormap
from matplotlib.ticker import LogLocator, FuncFormatter, MaxNLocator, LinearLocator

from namelist_for_maps import *
matplotlib.use("Agg")

where_sliced_data_are = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/maps/geopotential_plus_tracking_files/'

sliced_data_information =[
    ('CP-ON', where_sliced_data_are+'CP-ON_GEO+TRACKING_hourly.nc'),
    ('CP-OFF', where_sliced_data_are+'CP-OFF_GEO+TRACKING_hourly.nc')
]

noaa_ds = xr.open_dataset(NOAA_path)


for label, data_path in sliced_data_information:

    dataset = xr.open_dataset(data_path)

    lat = dataset.lat
    lon = dataset.lon

    # definição do geopotencial (em metros):
    geopotential = dataset.geoph700.isel(time=60)

    plt.figure(figsize=(12,6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree()) #lonW lonE latS latN

    ax.add_feature(cf.COASTLINE,alpha=0.4,linewidth=0.4,edgecolor='black')
    ax.add_feature(cf.BORDERS,alpha=0.4,linewidth=0.4)
    ax.add_feature(cf.LAND,alpha=0.4,linewidth=0.4)
    ax.add_feature(cf.STATES,alpha=0.4,linewidth=0.2)
    ax.add_feature(cf.OCEAN,alpha=0.4,linewidth=0.3)

    contour = plt.contourf(lon, lat, geopotential, levels=20, cmap='RdBu_r', transform=ccrs.PlateCarree())

    contour_lines = plt.contour(lon, lat, geopotential, levels=20, colors='white', linewidths=0.5, transform=ccrs.PlateCarree())
    plt.clabel(contour_lines, fmt='%i', fontsize=10)

    plt.title(f'700 hPa Geopotential Height of - {label}')
    plt.colorbar(contour, orientation='horizontal', pad=0.05, label='Geopotential Height m')

    time = dataset.time_track
    # Inicializa listas
    track_lats = []
    track_lons = []

    # Extrai lat/lon do tracking direto (se for variável separada)
    tracking_lat = dataset.lat_track # ou outra variável do tipo
    tracking_lon = dataset.lon_track

    # Tempo do geopotential (exemplo índice 66)
    time_geo = dataset.time.isel(time=66).values

    # Array dos tempos do track
    time_track = dataset.time_track.values

    # Calcular a diferença absoluta entre time_geo e todos os tempos do track
    diff = np.abs(time_track - time_geo)

    # Achar o índice do tempo do track mais próximo
    current_idx = diff.argmin()

    print(f'Índice do time_track mais próximo ao time_geo: {current_idx}')

    # Define os limites para pegar 6 pontos antes e 6 depois, evitando estourar índice
    start_idx = max(current_idx - 6, 0)
    end_idx = min(current_idx + 6, len(time_track) - 1)
    
    # Fatiando o track
    track_lat_slice = dataset.lat_track.isel(time_track=slice(start_idx, end_idx + 1))
    track_lon_slice = dataset.lon_track.isel(time_track=slice(start_idx, end_idx + 1))

    # Plotando só esses pontos
    ax.plot(track_lon_slice, track_lat_slice, color='black', linewidth=1.5, marker='o', markersize=4,
            transform=ccrs.PlateCarree(), label='Tracking')

    # Track NOAA: vamos filtrar para os tempos próximos
    # Aqui assumo que noaa_ds tem variáveis lat e lon e uma coordenada time
    noaa_time = noaa_ds.time.values

    # Selecionar índices NOAA cujos tempos estejam dentro do intervalo dos track time_slice
    track_time_slice = time_track[start_idx:end_idx + 1]

    # Criar um mask booleano para selecionar os tempos NOAA que estejam próximos (vamos aceitar diferença máxima, por exemplo, 1 hora)
    max_diff_seconds = 3600  # 1 hora em segundos

    # Convertendo para np.datetime64 para facilitar comparação
    track_times_np = track_time_slice.astype('datetime64[s]')
    noaa_times_np = noaa_time.astype('datetime64[s]')

    # Filtra os índices NOAA para os tempos que batem com algum tempo do intervalo track_times_np dentro de max_diff_seconds
    indices_noaa = []
    for i, t_noaa in enumerate(noaa_times_np):
        diffs = np.abs(track_times_np - t_noaa).astype('timedelta64[s]').astype(int)
        if np.any(diffs <= max_diff_seconds):
            indices_noaa.append(i)

    # Selecionar lat/lon NOAA desses índices
    noaa_lats_sel = noaa_ds.lat.isel(time=indices_noaa)
    noaa_lons_sel = noaa_ds.lon.isel(time=indices_noaa)

    # Plotar track NOAA em vermelho
    ax.plot(noaa_lons_sel, noaa_lats_sel, color='red', linewidth=1.5, marker='x', markersize=6,
            transform=ccrs.PlateCarree(), label='NOAA Track')

    plt.legend()
    plt.savefig(f'test2_{label}_with_NOAA.png')
    print(f'Saved test2_{label}_with_NOAA.png')
