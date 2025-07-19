import os
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import numpy as np

from namelist_for_maps import *

# Caminhos
where_sliced_data_are = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/maps/geopotential_plus_tracking_files/'
sliced_data_information = [
    ('CP-ON', where_sliced_data_are + 'CP-ON_GEO+TRACKING_hourly.nc'),
    ('CP-OFF', where_sliced_data_are + 'CP-OFF_GEO+TRACKING_hourly.nc')
]

noaa_ds = xr.open_dataset(NOAA_path)

# Saída dos frames
output_folder = 'frames_anim_panel'
os.makedirs(output_folder, exist_ok=True)

# Configurações gerais
level = '700'
title_level = f'{level}hPa'

# Abrir datasets
datasets = [xr.open_dataset(path) for _, path in sliced_data_information]
times = datasets[0].time
n_frames = len(times)

# Início da geração de quadros
for t in range(n_frames):
    print(f'Gerando frame {t+1}/{n_frames}...')

    fig, axes = plt.subplots(nrows=2, figsize=(12, 12), subplot_kw={'projection': ccrs.PlateCarree()})
    plt.subplots_adjust(hspace=0.3)

    for i, (label, _) in enumerate(sliced_data_information):
        dataset = datasets[i]
        lat = dataset.lat
        lon = dataset.lon
        geopotential = dataset[f'geoph{level}'].isel(time=t)

        ax = axes[i]
        ax.set_extent([lonW, lonE, latS, latN], crs=ccrs.PlateCarree())

        ax.add_feature(cf.COASTLINE, alpha=0.4, linewidth=0.4)
        ax.add_feature(cf.BORDERS, alpha=0.4, linewidth=0.4)
        ax.add_feature(cf.LAND, alpha=0.4)
        ax.add_feature(cf.STATES, alpha=0.4, linewidth=0.2)
        ax.add_feature(cf.OCEAN, alpha=0.4)

        contour = ax.contourf(lon, lat, geopotential, levels=20, cmap='RdBu_r', transform=ccrs.PlateCarree())
        contour_lines = ax.contour(lon, lat, geopotential, levels=20, colors='white', linewidths=0.5, transform=ccrs.PlateCarree())
        ax.clabel(contour_lines, fmt='%i', fontsize=10)

        ax.set_title(f'{title_level} Geopotential Height - {label} - {str(times[t].values)[:16]}')

        # TRACKING LOCAL
        time_geo = dataset.time.isel(time=t).values
        time_track = dataset.time_track.values
        diff = np.abs(time_track - time_geo)
        current_idx = diff.argmin()
        start_idx = max(current_idx - 6, 0)
        end_idx = min(current_idx + 6, len(time_track) - 1)
        track_lat_slice = dataset.lat_track.isel(time_track=slice(start_idx, end_idx + 1))
        track_lon_slice = dataset.lon_track.isel(time_track=slice(start_idx, end_idx + 1))

        ax.plot(track_lon_slice, track_lat_slice, color='black', linewidth=1.5, marker='o', markersize=4,
                transform=ccrs.PlateCarree(), label='Tracking')

        # TRACK NOAA
        noaa_time = noaa_ds.time.values
        track_time_slice = time_track[start_idx:end_idx + 1]
        max_diff_seconds = 3600
        track_times_np = track_time_slice.astype('datetime64[s]')
        noaa_times_np = noaa_time.astype('datetime64[s]')
        indices_noaa = []
        for i_noaa, t_noaa in enumerate(noaa_times_np):
            diffs = np.abs(track_times_np - t_noaa).astype('timedelta64[s]').astype(int)
            if np.any(diffs <= max_diff_seconds):
                indices_noaa.append(i_noaa)

        noaa_lats_sel = noaa_ds.lat.isel(time=indices_noaa)
        noaa_lons_sel = noaa_ds.lon.isel(time=indices_noaa)

        ax.plot(noaa_lons_sel, noaa_lats_sel, color='red', linewidth=1.5, marker='x', markersize=6,
                transform=ccrs.PlateCarree(), label='NOAA Track')

        ax.legend()

    # Colorbar única
    cbar_ax = fig.add_axes([0.2, 0.08, 0.6, 0.02])
    fig.colorbar(contour, cax=cbar_ax, orientation='horizontal', label='Geopotential Height (m)')

    # Salvar frame
    frame_path = os.path.join(output_folder, f'frame_{t:03d}.png')
    plt.savefig(frame_path, dpi=150)
    plt.close(fig)

print("Todos os frames foram salvos.")
print("Agora rode este comando no terminal para criar a animação GIF:")
print(f"\nconvert -delay 20 -loop 0 {output_folder}/frame_*.png painel_animado_{title_level}.gif\n")
