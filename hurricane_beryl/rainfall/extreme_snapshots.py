import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FuncFormatter
import os
import matplotlib
matplotlib.use("Agg")  # Evita abrir janela se rodando em servidor

# Diretório onde estão os arquivos
# where_the_files_are = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/rainfall_sliced_data/'
where_the_files_are = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/sliced_rainfall_for_pdfs_cdfs/'

# Experimentos por linha
panels = [
    [  # Linha 1
        ('GPM-IMERG', 'indigo'),
        ('ERA5', 'blue'),
        ('GSMaP', 'gray'),
        ('CP-ON', 'red'),
        ('CP-OFF', 'black'),
    ],
    [  # Linha 2
        ('CP-ON', 'red'),
        ('CP-OFF', 'black'),
        ('GPM-IMERG', 'indigo'),
        ('CP-GFS', 'navy'),
        ('CP-15km', 'magenta'),
        ('CP-60km', 'lime'),
        ('CP-29', 'darkorange'),
        ('CP-02T12', 'olive'),
        ('CP-1HD050', 'silver')
    ],
    [  # Linha 3
        ('GPM-IMERG', 'indigo'),
        ('CP-ON', 'red'),
        ('CP-OFF', 'black'),
        ('CP-1H', 'springgreen'),
        ('CP-3H', 'orange'),
        ('CP-D025', 'brown'),
        ('CP-D050', 'pink')
    ]
]

# Datas específicas
time_stamps = ['2024-07-04T00', '2024-07-05T16', '2024-07-07T10']
column_labels = ['(A)', '(B)', '(C)']

# Bins logarítmicos
thresholds = np.logspace(np.log10(0.1), np.log10(250), num=60)
bin_centers = 0.5 * (thresholds[:-1] + thresholds[1:])

# Definir os extents para cada coluna
extents = [
    [-89, -69, 10, 30],     # Para 2024-07-04T00
    [-100, -80, 12.5, 32.5],  # Para 2024-07-05T16
    [-105, -85, 17.5, 37.5]   # Para 2024-07-07T10
]

# Criar figura 3x3
# fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 14), sharex=True, sharey=True)
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 14))

for row_idx, data_group in enumerate(panels):
    for col_idx, timestamp in enumerate(time_stamps):
        ax = axes[row_idx, col_idx]
        legend_labels = []

        for file, color in data_group:
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
output_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/pdf_cdf/SNAPSHOTS_percentile_CDF_FINAL_NATIVE_60_15.png'
plt.savefig(output_path, dpi=300)
plt.close()
print(f"Figura salva como '{output_path}'")
