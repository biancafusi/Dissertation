import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FuncFormatter
import os
import matplotlib
matplotlib.use("Agg")  # Evita abrir janela se rodando em servidor

# Diretório onde estão os arquivos
where_the_files_are = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/helene_rainfall_statistics/helene_rainfall_sliced/'

# Experimentos por linha
panels = [
    [  # Linha 1
        ('GPM-IMERG', 'indigo'),
        ('ERA5', 'blue'),
        ('GSMaP', 'green'),
        ('CP-ON', 'red'),
        ('CP-OFF', 'black'),
    ],
    [  # Linha 2
        ('CP-ON', 'red'),
        ('CP-OFF', 'black'),
        ('GSMaP', 'green'),
        ('CP-15km', 'magenta'),
        ('CP-25', 'darkorange'),
        ('CP-1HD050', 'cyan')
    ]
]


# Datas específicas
time_stamps = ['2024-09-26T09', '2024-09-27T00', '2024-09-27T13']
column_labels = ['(A)', '(B)', '(C)']

# Bins logarítmicos
thresholds = np.logspace(np.log10(0.1), np.log10(510), num=50)
bin_centers = 0.5 * (thresholds[:-1] + thresholds[1:])

# Definir os extents para cada coluna
extents = [
    [-89, -79, 21, 31],
    [-87, -77, 25, 35],    # (a) Day 04
    [-87, -77, 31, 41], # (b) Day 04
]

# Criar figura 3x3
# fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 14), sharex=True, sharey=True)
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 10))

for row_idx, data_group in enumerate(panels):
    for col_idx, timestamp in enumerate(time_stamps):
        ax = axes[row_idx, col_idx]
        legend_labels = []

        for file, color in data_group:
            print(f'{file}')
            if file == 'CP-15km':
                file_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/helene_rainfall_statistics/hourly_native_rainfall/CP-15km_hourly.nc'
                print('oi')
            else:
                file_path = os.path.join(where_the_files_are, f'{file}_hourly.nc')

            ds = xr.open_dataset(file_path)

            # Seleciona o dado para o tempo desejado
            ds_sel = ds.sel(time=timestamp)

            # Pega os limites da área para essa coluna
            lonW, lonE, latS, latN = extents[col_idx]

            # Recorta espacialmente
            rainfall = ds_sel['rainfall'].sel(lon=slice(lonW, lonE), lat=slice(latS, latN))

            # Flatten e filtra os dados positivos
            rain = rainfall.values.ravel()
            rain = rain[~np.isnan(rain)]
            rain = rain[rain > 0]

            # Cálculo da CDF
            count, _ = np.histogram(rain, bins=thresholds)
            pdf = count / np.sum(count) if np.sum(count) > 0 else np.zeros_like(count)
            cdf = np.cumsum(pdf)
            cdf_percent = cdf * 100

            linestyle = '-'
            if file == 'CP-ON':
                linestyle = '-.'
            elif file == 'CP-OFF':
                linestyle = '--'

            ax.plot(bin_centers, cdf_percent, label=file, color=color, linestyle=linestyle)

        # Configurações do gráfico
        ax.set_xscale('log')
        ax.set_xlim(1.15, max(thresholds))
        ax.set_ylim(85, 100)
        ax.set_yticks(np.arange(85, 101, 1))
        ax.xaxis.set_major_locator(LogLocator(base=10.0))
        ax.xaxis.set_major_formatter(FuncFormatter(
            lambda x, _: f'$10^{{{int(np.log10(x))}}}$' if x > 0 and np.isclose(np.log10(x) % 1, 0) else ''
        ))

        if col_idx == 0:
            ax.set_ylabel('Frequency (%)')
        if row_idx == 2:
            ax.set_xlabel('Hourly rainfall (mm/h)')
            
        if row_idx == 0:
            ax.set_title(f'{column_labels[col_idx]} {timestamp}')
            
        ax.legend(fontsize=8)

# Ajustar layout e salvar
plt.tight_layout()
output_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/helene_rainfall_statistics/helene_PDF_CDF/SNAPSHOTS_percentile_CDF_FINAL.png'
plt.savefig(output_path, dpi=300)
plt.close()
print(f"Figura salva como '{output_path}'")
