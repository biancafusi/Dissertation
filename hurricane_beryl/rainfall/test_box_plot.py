# import matplotlib.pyplot as plt
# import matplotlib
# import numpy as np
# import xarray as xr

# matplotlib.use("Agg")  # Evita abrir janela se rodando em servidor

# data_to_be_plotted = [
#     ('GPM-IMERG', 'indigo'),
#     ('CP-ON', 'red'),
#     ('CP-OFF', 'black'),
# ]

# where_the_files_are = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/rainfall_sliced_data/'

# # Bins logarítmicos
# thresholds = np.logspace(np.log10(0.1), np.log10(90), num=35)
# bin_centers = 0.5 * (thresholds[:-1] + thresholds[1:])

# # Criar figuras
# fig, (ax_pdf, ax_cdf, ax_box) = plt.subplots(1, 3, figsize=(21, 6), gridspec_kw={'width_ratios': [1, 1, 0.7]}, sharex=False)

# box_data = []
# box_labels = []

# for file, color in data_to_be_plotted:
#     print(f'Processando: {file}')
    
#     ds = xr.open_dataset(where_the_files_are + f'{file}_hourly.nc')
#     rain = ds['rainfall'].values.ravel()
#     rain = rain[~np.isnan(rain)]
#     rain = rain[rain > 0]  # Apenas positivos
    
#     # Dados para o boxplot
#     box_data.append(rain)
#     box_labels.append(file)
    
#     # Histograma com densidade
#     count, _ = np.histogram(rain, bins=thresholds)
#     pdf = count / np.sum(count)
#     cdf = np.cumsum(pdf)

#     pdf_percent = pdf * 100
#     cdf_percent = cdf * 100

#     ax_pdf.plot(bin_centers, pdf_percent, label=file, color=color)
#     ax_cdf.plot(bin_centers, cdf_percent, label=file, color=color)

# # Formatação PDF/CDF
# for ax, title, ylabel in zip(
#         [ax_pdf, ax_cdf],
#         ['(a) Empirical PDF of accumulated rainfall', '(b) Empirical CDF of accumulated rainfall'],
#         ['Frequency (%)', 'Cumulative probability (%)']):

#     ax.set_xscale('log')
#     ax.set_xlabel('Hourly rainfall (mm/h)')
#     ax.set_ylabel(ylabel)
#     ax.set_title(title)
#     ax.grid(True, which='both', axis='y', linestyle='--', alpha=0.6)
#     ax.legend(fontsize=8)

# # Eixo X - ticks
# xticks_to_use = thresholds[::2]
# xtick_labels = [f'{t:.2f}' for t in xticks_to_use]
# for ax in [ax_pdf, ax_cdf]:
#     ax.set_xticks(xticks_to_use)
#     ax.set_xticklabels(xtick_labels, rotation=45)

#     for tick in xticks_to_use:
#         ax.axvline(x=tick, color='gray', linestyle=':', linewidth=1)

# ax_cdf.set_yticks(np.arange(0, 110, 10))
# ax_cdf.axhline(50, color='black', linestyle='--', linewidth=1)

# # ➕ Boxplot
# ax_box.boxplot(box_data, labels=box_labels, patch_artist=True)
# ax_box.set_title('(c) Rainfall distribution (boxplot)')
# ax_box.set_ylabel('Hourly rainfall (mm/h)')
# # ax_box.set_yscale('log')  # ← REMOVIDO para usar escala automática
# ax_box.grid(True, axis='y', linestyle='--', alpha=0.6)

# # Cores no boxplot (opcional)
# for patch, (_, color) in zip(ax_box.artists, data_to_be_plotted):
#     patch.set_facecolor(color)
#     patch.set_alpha(0.6)


# plt.tight_layout()
# plt.savefig('/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/pdf_cdf/pdf_cdf_boxplot.png', dpi=300)
# plt.close()
# print("Figura salva com boxplot como 'pdf_cdf_boxplot.png'")


import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib

matplotlib.use("Agg")  # Evita abrir janela se rodando em servidor

# Diretório dos arquivos
where_the_files_are = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/rainfall_sliced_data/'

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
        # ('CP-1H', 'springgreen'),
        # ('CP-3H', 'orange'),
        # ('CP-D025', 'brown'),
        # ('CP-D050', 'pink'),
    ]
]

# Bins logarítmicos
thresholds = np.logspace(np.log10(0.1), np.log10(90), num=40)
bin_centers = 0.5 * (thresholds[:-1] + thresholds[1:])

# Criar figura com 3 linhas e 2 colunas (PDF e CDF por linha)
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(14, 18), sharex=True)

# Letras para nomear os subplots
panel_labels = ['(A)', '(B)', '(C)', '(D)', '(E)', '(F)']

# Loop pelas linhas (painéis)
for i, data_to_be_plotted in enumerate(panels):
    ax_pdf = axes[i, 0]
    ax_cdf = axes[i, 1]

    for file, color in data_to_be_plotted:
        print(f'Processando: {file}')
        ds = xr.open_dataset(where_the_files_are + f'{file}_hourly.nc')
        rain = ds['rainfall'].values.ravel()
        rain = rain[~np.isnan(rain)]
        rain = rain[rain > 0]  # Apenas positivos

        count, _ = np.histogram(rain, bins=thresholds)
        pdf = count / np.sum(count)
        cdf = np.cumsum(pdf)

        pdf_percent = pdf * 100
        cdf_percent = cdf * 100

        ax_pdf.plot(bin_centers, pdf_percent, label=file, color=color)
        ax_cdf.plot(bin_centers, cdf_percent, label=file, color=color)

    # Configurações dos eixos
    for ax, title_suffix, ylabel in zip(
        [ax_pdf, ax_cdf],
        ['Empirical PDF of accumulated rainfall', 'Empirical CDF of accumulated rainfall'],
        ['Frequency (%)', 'Cumulative probability (%)']
    ):
        ax.set_xscale('log')
        ax.set_xlabel('Hourly rainfall (mm/h)')
        ax.set_ylabel(ylabel)
        ax.set_title(f'{panel_labels[i*2 + [0,1][ax==ax_cdf]]} {title_suffix}', loc='left')
        ax.grid(True, which='both', axis='y', linestyle='--', alpha=0.6)
        ax.legend(fontsize=8)

        # Marcar os thresholds no eixo x
        ax.set_xticks(thresholds[::2])
        ax.set_xticklabels([f'{t:.2f}' for t in thresholds[::2]], rotation=45)
        for tick in thresholds[::2]:
            ax.axvline(x=tick, color='gray', linestyle=':', linewidth=1)

    # Linha horizontal em 50% na CDF
    ax_cdf.set_yticks(np.arange(0, 110, 10))
    ax_cdf.axhline(50, color='black', linestyle='--', linewidth=1)

# Ajustar layout e salvar figura
plt.tight_layout()
output_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/pdf_cdf/painel_pdf_cdf_empirico_percentual.png'
plt.savefig(output_path, dpi=300)
plt.close()
print(f"Figura salva como '{output_path}'")
