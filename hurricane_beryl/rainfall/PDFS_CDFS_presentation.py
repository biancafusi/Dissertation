# import xarray as xr
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import stats
# import matplotlib

# matplotlib.use("Agg")  # Evita abrir janela se rodando em servidor

# data_to_be_plotted = [
#     ('GPM-IMERG', 'indigo'),
#     # ('ERA5', 'blue'),
#     # ('GSMaP', 'gray'),
#     ('CP-ON', 'red'),
#     ('CP-OFF', 'black'),
#     # ('CP-1H', 'springgreen'),
#     # ('CP-3H', 'orange'),
#     # ('CP-D025', 'brown'),
#     # ('CP-D050', 'pink'),
#     # ('CPSS-ON', 'cyan'),
#     # ('CP-GFS', 'navy'),
#     # ('CP-15km', 'magenta'),
#     # ('CP-60km', 'lime'),
#     # ('CP-29', 'darkorange'),
#     # ('CP-02T12', 'olive'),
#     # ('CP-1HD050', 'silver')
# ]

# where_the_files_are = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/rainfall_sliced_data/'

# # Bins logarítmicos
# thresholds = np.logspace(np.log10(0.1), np.log10(90), num=40)
# # thresholds = np.array([0.1, 0.15, 0.2, 0.25, 0.45, 0.65, 1, 2, 4, 8, 16, 24, 40, 50, 60, 70, 80, 90])

# bin_centers = 0.5 * (thresholds[:-1] + thresholds[1:])

# # Criar figuras
# fig, (ax_pdf, ax_cdf) = plt.subplots(1, 2, figsize=(14, 6), sharex=True)

# for file, color in data_to_be_plotted:
#     print(f'Processando: {file}')
    
#     ds = xr.open_dataset(where_the_files_are + f'{file}_hourly.nc')
#     rain = ds['rainfall'].values.ravel()
#     rain = rain[~np.isnan(rain)]
#     print(rain.max())
#     rain = rain[rain > 0]  # Apenas positivos

#     # Histograma com densidade
#     count, _ = np.histogram(rain, bins=thresholds)
#     pdf = count / np.sum(count)           # Frequência relativa
#     cdf = np.cumsum(pdf)                  # Acumulada

#     # Convertendo para porcentagem
#     pdf_percent = pdf * 100
#     cdf_percent = cdf * 100

#     # Plotar
#     ax_pdf.plot(bin_centers, pdf_percent, label=file, color=color)
#     ax_cdf.plot(bin_centers, cdf_percent, label=file, color=color)


# # Formatting the plots
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

# # Adjust x-axis ticks
# xticks_to_use = thresholds[::2]
# xtick_labels = [f'{t:.2f}' for t in xticks_to_use]
# for ax in [ax_pdf, ax_cdf]:
#     ax.set_xticks(xticks_to_use)
#     ax.set_xticklabels(xtick_labels, rotation=45)

# # Adding vertical lines on (a) PDF at the x-ticks
# for tick in xticks_to_use:
#     ax_pdf.axvline(x=tick, color='gray', linestyle=':', linewidth=1) 
    
#     ax_cdf.axvline(x=tick, color='gray', linestyle=':', linewidth=1) # Vertical line for each threshold tick


# # Formatting the y-axis for CDF
# ax_cdf.set_yticks(np.arange(0, 110, 10))  # Y-axis ticks from 0 to 100 in steps of 10
# ax_cdf.axhline(50, color='black', linestyle='--', linewidth=1)  # Add a horizontal line at 50%

# plt.tight_layout()
# plt.savefig('/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/pdf_cdf/pdf_cdf_test.png', dpi=300)
# plt.close()
# print("Figura salva como 'painel_pdf_cdf_empirico_percentual.png'")

# # =================================== ZOOM ON THE EXTREMES ============================= #
# # data_to_be_plotted = [
# #     ('GPM-IMERG', 'indigo'),
# #     ('ERA5', 'blue'),
# #     ('GSMap', 'gray'),
# #     ('CP-ON', 'red'),
# #     ('CP-OFF', 'black'),
# #     ('CP-1H', 'springgreen'),
# #     ('CP-3H', 'orange'),
# #     ('CP-D025', 'brown'),
# #     ('CP-D050', 'pink'),
# #     ('CPSS-ON', 'cyan'),
# #     ('CP-GFS', 'navy'),
# #     ('CP-15km', 'magenta'),
# #     ('CP-60km', 'lime'),
# #     ('CP-29', 'darkorange'),
# #     ('CP-02T12', 'olive'),
# #     ('CP-1HD050', 'silver')
# # ]

# # where_the_files_are = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/'

# # thresholds = np.linspace(0.01, 350, num=500)

# # fig, ax_cdf_zoom = plt.subplots(figsize=(8, 6))

# # for file, color in data_to_be_plotted:
# #     print(f'Processing: {file}')
    
# #     ds = xr.open_dataset(where_the_files_are + f'{file}.nc')
# #     rain = ds['rainfall'].values.ravel()
# #     rain = rain[~np.isnan(rain)]
# #     rain = rain[rain > 0]

# #     # Fit and compute CDF
# #     loc, scale = stats.expon.fit(rain)
# #     cdf_expon = stats.expon.cdf(thresholds, loc=loc, scale=scale) * 100  # Convert to percentage

# #     # Filter to show only CDF >= 85%
# #     mask = cdf_expon >= 85
# #     thresholds_zoom = thresholds[mask]
# #     cdf_zoom = cdf_expon[mask]

# #     if len(thresholds_zoom) > 0:
# #         ax_cdf_zoom.plot(thresholds_zoom, cdf_zoom, label=file, color=color)

# # # Formatting
# # ax_cdf_zoom.set_xscale('log')
# # ax_cdf_zoom.set_xlabel('Accumulated rainfall (mm)')
# # ax_cdf_zoom.set_ylabel('Cumulative probability (%)')
# # ax_cdf_zoom.set_title('Empirical CDF above 85%')
# # ax_cdf_zoom.set_yticks(np.arange(85, 101, 1))
# # ax_cdf_zoom.set_ylim(85, 100)
# # ax_cdf_zoom.grid(True, which='both', axis='y', linestyle='--', alpha=0.6)
# # ax_cdf_zoom.legend(fontsize=8)


# # # Seleciona apenas os thresholds > 42 mm e espaça a cada 25 valores
# # xticks_to_use = thresholds[thresholds > 35][::25]
# # xtick_labels = [f'{t:.1f}' for t in xticks_to_use]

# # # Adiciona linhas verticais para cada tick
# # for x in xticks_to_use:
# #     ax_cdf_zoom.axvline(x=x, color='gray', linestyle=':', linewidth=1)

# # # Configura os ticks do eixo x
# # ax_cdf_zoom.set_xticks(xticks_to_use)
# # ax_cdf_zoom.set_xticklabels(xtick_labels, rotation=45)

# # plt.tight_layout()
# # plt.savefig('empirical_cdf_above_85_percent.png', dpi=300)
# # plt.close()

# # print("Zoomed CDF figure saved as 'empirical_cdf_above_85_percent.png'")
##############################################################################################
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib
from matplotlib.ticker import LogLocator, FuncFormatter

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
        ('CP-15km', 'magenta'),
        ('CP-1HD050', 'cyan'),
        ('CP-1H', 'springgreen'),
    ],
    # [  # Linha 2
    #     ('CP-ON', 'red'),
    #     ('CP-OFF', 'black'),
    #     ('GPM-IMERG', 'indigo'),
    #     ('CP-GFS', 'navy'),
    #     ('CP-15km', 'magenta'),
    #     ('CP-60km', 'lime'),
    #     ('CP-29', 'darkorange'),
    #     ('CP-02T12', 'olive'),
    #     ('CP-1HD050', 'silver')
    # ],
    # [  # Linha 3
    #     ('GPM-IMERG', 'indigo'),
    #     ('CP-ON', 'red'),
    #     ('CP-OFF', 'black'),
    #     ('CP-1H', 'springgreen'),
    #     ('CP-3H', 'orange'),
    #     ('CP-D025', 'brown'),
    #     ('CP-D050', 'pink')
    # ]
]

# Bins logarítmicos
thresholds = np.logspace(np.log10(0.1), np.log10(250), num=60)
bin_centers = 0.5 * (thresholds[:-1] + thresholds[1:])

# Criar figura com 3 linhas e 2 colunas (PDF e CDF por linha)
# fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(14, 18), sharex=True) aqui é para ter a ultima linha com o eixo x
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

# Letras para nomear os subplots
# panel_labels = ['(A)', '(B)', '(C)', '(D)', '(E)', '(F)']
panel_labels = ['(A)', '(B)']

# Loop pelas linhas (painéis)
for i, data_to_be_plotted in enumerate(panels):
    ax_pdf = axes[0]
    ax_cdf = axes[1]

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

        if file == 'CP-ON':
            linestyle = '-.'
        elif file == 'CP-OFF':
            linestyle = '--'
        else:
            linestyle = '-'

        ax_pdf.plot(bin_centers, pdf_percent, label=file, color=color,linestyle=linestyle)
        ax_cdf.plot(bin_centers, cdf_percent, label=file, color=color,linestyle=linestyle)

    # Configurações dos eixos PDF e CDF
    for ax, ylabel in zip([ax_pdf, ax_cdf], ['Frequency', 'Frequency (%)']):
        ax.set_xscale('log')
        ax.set_xlabel('Hourly rainfall (mm/h)')
        ax.set_ylabel(ylabel)

        # Ticks logarítmicos formatados como potências de 10 no eixo x
        ax.xaxis.set_major_locator(LogLocator(base=10.0))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'$10^{{{int(np.log10(x))}}}$' if x > 0 and np.isclose(np.log10(x) % 1, 0) else ''))

        # Linhas verticais nos ticks principais do eixo x
        # for tick in thresholds:
        #     if np.log10(tick).is_integer():
        #         ax.axvline(x=tick, color='gray', linestyle=':', linewidth=1)

        # Ajustes adicionais por tipo de gráfico
        if ax == ax_pdf:
            ax.set_yscale('log')
            ax.yaxis.set_major_locator(LogLocator(base=10.0))
            ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'$10^{{{int(np.log10(y))}}}$' if y > 0 and np.isclose(np.log10(y) % 1, 0) else ''))
            # ax.grid(True, which='both', axis='both', linestyle='--', alpha=0.6)
        else:
            ax.set_yticks(np.arange(0, 110, 10))
            x_min, x_max = ax.get_xlim()

            # Limites desejados em escala log
            x_start = 0.1  # 10⁻¹
            x_end = 3    # 10⁰

            y_level = 50   # Altura da linha horizontal

            # Desenha a linha horizontal limitada
            x_min, x_max = ax.get_xlim()
            xmin_rel = (np.log10(x_start) - np.log10(x_min)) / (np.log10(x_max) - np.log10(x_min))
            xmax_rel = (np.log10(x_end) - np.log10(x_min)) / (np.log10(x_max) - np.log10(x_min))

            ax.axhline(y_level, color='black', linestyle='--', linewidth=1, xmin=xmin_rel, xmax=xmax_rel)

            # Desenha as barrinhas verticais (tipo "|") nas extremidades
            ax.vlines(x_start, y_level - 1.5, y_level + 1.5, color='black', linewidth=1)  # início
            ax.vlines(x_end, y_level - 1.5, y_level + 1.5, color='black', linewidth=1)    # fim

        ax.set_title(f'{panel_labels[i*2 + [0,1][ax==ax_cdf]]}', loc='center')
        ax.legend(fontsize=8)

# Ajustar layout e salvar figura
plt.tight_layout()
# output_path = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/rainfall_analysis/pdf_cdf/painel_pdf_cdf_FINAL_PRESENTATION.png'
output_path = 'painel_pdf_cdf_FINAL_PRESENTATION.png'

plt.savefig(output_path, dpi=300)
plt.close()
print(f"Figura salva como '{output_path}'")


