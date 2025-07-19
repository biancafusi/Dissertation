import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib
from matplotlib.ticker import LogLocator, FuncFormatter


matplotlib.use("Agg")  # Evita abrir janela se rodando em servidor

# =============================== EXTREMES ============================== #

# # Diretório dos arquivos
# where_the_files_are = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/rainfall_sliced_data/'
where_the_files_are = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/sliced_rainfall_for_pdfs_cdfs/'

# Experimentos divididos em 3 linhas
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

# Bins logarítmicos
thresholds = np.logspace(np.log10(0.1), np.log10(250), num=60)
bin_centers = 0.5 * (thresholds[:-1] + thresholds[1:])

# Criar figura com 3 linhas e 2 colunas (PDF e CDF por linha)
# fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(14, 18), sharex=True) aqui é para ter a ultima linha com o eixo x
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(7, 14))

# Letras para nomear os subplots
panel_labels = ['(B)','(D)', '(F)']

for i, data_to_be_plotted in enumerate(panels):
    ax_cdf = axes[i]
    legend_labels = []  # Lista para armazenar legendas personalizadas

    for file, color in data_to_be_plotted:
        print(f'Processando: {file}')
        ds = xr.open_dataset(where_the_files_are + f'{file}_hourly.nc')
        rain = ds['rainfall'].values.ravel()
        rain = rain[~np.isnan(rain)]
        rain = rain[rain > 0]  # Apenas positivos

        count, _ = np.histogram(rain, bins=thresholds)
        pdf = count / np.sum(count)
        cdf = np.cumsum(pdf)
        cdf_percent = cdf * 100

        if file == 'CP-ON':
            linestyle = '-.'
        elif file == 'CP-OFF':
            linestyle = '--'
        else:
            linestyle = '-'

        ax_cdf.plot(bin_centers, cdf_percent, label=file, color=color, linestyle=linestyle)

        # Se for GPM-IMERG, calcular ponto de 95% e plotar
        if file == 'GPM-IMERG':
            # Interpolar x onde y=95
            if np.any(cdf_percent >= 95):
                x_95 = np.interp(95, cdf_percent, bin_centers)

                # Linha vertical
                ax_cdf.axvline(x_95, color=color, linestyle=':', linewidth=2)

                # Caixa com flecha
                ax_cdf.annotate(
                    f'{x_95:.1f} mm/h',
                    xy=(x_95, 95),
                    xytext=(x_95 * 1.4, 93),
                    textcoords='data',
                    arrowprops=dict(facecolor=color, arrowstyle='->', lw=1.5),
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=color, lw=1),
                    fontsize=12,
                    color=color,  # Cor do texto
                    ha='left'
                )

        # Agora para as outras curvas, calcular a frequência para 5.5 mm/h
        if file != 'GPM-IMERG':
            # Encontrar a frequência para 5.5 mm/h
            if np.any(bin_centers >= 5.5):
                x_5_5 = np.interp(5.5, bin_centers, cdf_percent)

                # Adicionar essa informação ao texto da legenda
                freq_at_5_5 = x_5_5  # Frequência correspondente a 5.5 mm/h
                legend_labels.append(f'{file}: {freq_at_5_5:.1f}%')

    # Adicionar o texto com as frequências abaixo da legenda, mas dentro do gráfico
    ax_cdf.legend(fontsize=8)

    # Agora ajustando o texto para aparecer dentro do gráfico
    ax_cdf.text(
        0.88, 0.45,  # Ajustar posição do texto (0.5 para centralizar, -0.1 para posicionar abaixo da área de plotagem)
        '\n'.join(legend_labels), 
        transform=ax_cdf.transAxes,  # Usando coordenadas relativas ao eixo
        fontsize=10, 
        verticalalignment='top', 
        horizontalalignment='center',
        bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.3')
    )

    # Configurações dos eixos
    for ax, ylabel in zip(
        [ax_cdf],
        ['Frequency (%)']
    ):
        ax.set_xscale('log')
        ax.set_xlabel('Hourly rainfall (mm/h)')
        ax.set_ylabel(ylabel)
        ax.set_ylim(85, 100)

        ax.xaxis.set_major_locator(LogLocator(base=10.0))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'$10^{{{int(np.log10(x))}}}$' if x > 0 and np.isclose(np.log10(x) % 1, 0) else ''))

        ax.set_title(f'{panel_labels[i]}', loc='center')

        ax.legend(fontsize=8)

        ax.set_xlim(1.15, max(thresholds))  # Limite inferior no eixo x em 1.15

    # Linha horizontal em 50% na CDF
    ax_cdf.set_yticks(np.arange(85, 101, 1))
    ax_cdf.axhline(50, color='black', linestyle='--', linewidth=1)

# Ajustar layout e salvar figura
plt.tight_layout()
output_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/pdf_cdf/85_percentile_CDF_FINAL_60_15_NATIVE.png'
plt.savefig(output_path, dpi=300)
plt.close()
print(f"Figura salva como '{output_path}'")

