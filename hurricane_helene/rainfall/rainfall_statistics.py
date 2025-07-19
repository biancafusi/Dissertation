import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xskillscore as xs
import matplotlib

matplotlib.use("Agg")

'''
Com o xskillscore eu consigo calcular:
pearson_r
ets
'''

where_files_are = '/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/helene_rainfall_statistics/helene_acc_files/'

observation_data = xr.open_dataset(where_files_are+'GPM-IMERG_accumulated.nc')

print(observation_data.rainfall.values.max())

decimals = 1

obs = observation_data.assign_coords({
    "lon": np.round(observation_data.lon, decimals),
    "lat": np.round(observation_data.lat, decimals)
})

# todos tem que estar na mesma resolução se nao nao vai funcionar!!!!!
forecast_data_list = [
    ('ERA5', 'blue'),
    ('GSMaP', 'gray'),
    ('CP-ON', 'red'),
    ('CP-OFF', 'black'),
    ('CP-15km', 'magenta'),
    ('CP-1HD050', 'cyan'),
    ('CP-25', 'darkorange')
]

# para colocar o de 15km e 60km precisaria converter a resolução

thresholds = np.logspace(np.log10(0.01), np.log10(550), num=14)


# Inicializar um dicionário para guardar os ETS de cada experimento
ets_dict = {}
pearson_r_dict = {}

for experiment, color in forecast_data_list:
    print(f'Processing experiment {experiment}')

    forecast = xr.open_dataset(where_files_are+f'{experiment}_accumulated.nc')
    print(forecast.rainfall.values.max())
    # Arredondar lon e lat
    fct = forecast.assign_coords({
        "lon": np.round(forecast.lon, decimals),
        "lat": np.round(forecast.lat, decimals)
    })

    ets_values = [] 
    for th in thresholds:
        category_edges = np.array([0, th, np.inf])

        contingency = xs.Contingency(
            obs, fct, category_edges, category_edges, dim=["lat", "lon"]
        )
        ets = contingency.equit_threat_score()
        ets_values.append(ets['rainfall'].values)
    # Salvar no dicionário
    ets_dict[experiment] = ets_values

    # Calcular a correlação de Pearson entre as observações e a previsão
    r = xs.pearson_r(obs, fct, dim=["lat", "lon"])

    # Salvar o valor da correlação no dicionário (tirando a média para representar o experimento inteiro)
    pearson_r_dict[experiment] = r['rainfall'].values

print('\n ETS calculated, now plotting:')

# ============================================= PLOTAGEM ETS =====================================#

# Criar um dicionário de cores com base no forecast_data_list
color_map = {label: color for label, color in forecast_data_list}

# === Plotagem de todos os experimentos ===
plt.figure(figsize=(14, 6))


for experiment, ets_values in ets_dict.items():

    if experiment == 'CP-ON':
        linestyle = '-.'
    elif experiment == 'CP-OFF':
        linestyle = '--'
    else:
        linestyle = '-'
    
    plt.plot(
        thresholds,
        ets_values,
        marker='o',
        linestyle=linestyle,
        label=experiment,
        color=color_map.get(experiment)
    )

# Ajustes do gráfico
plt.xlabel("Rainfall Thresholds (mm)", fontsize=16)
plt.ylabel("Equitable Threat Score", fontsize=16)
plt.ylim(0, 0.7)

# Configurar escala logarítmica no eixo X
plt.xscale('log')
plt.minorticks_off()

# Definir explicitamente os ticks no eixo X como os valores dos thresholds
plt.xticks(thresholds, labels=np.round(thresholds,2))  # Ajusta a exibição dos ticks para os valores do threshold
plt.tick_params(axis='both', labelsize=16)

plt.legend(fontsize=10)
plt.grid()

# Ajustar o layout para evitar sobreposição
plt.tight_layout()

# Salvar a figura
plt.savefig('/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/helene_rainfall_statistics/helene_correlation/ets_all_helene.png', dpi=300)


# ======================== Gráfico de barras para correlação ============================#

# Preparando o gráfico de barras para as correlações de Pearson
plt.figure(figsize=(10, 8))

# Ordenando as correlações de Pearson em ordem decrescente
sorted_items = sorted(pearson_r_dict.items(), key=lambda x: x[1], reverse=True)
# Inverter para que o maior fique no topo
experiments = [item[0] for item in sorted_items][::-1]
correlations = [item[1] for item in sorted_items][::-1]

# Criando o gráfico de barras (invertido: horizontal)
plt.barh(experiments, correlations, color='gray')

# Ajustando o gráfico de barras
plt.xlabel("Pearson Correlation (r)", fontsize=16)
plt.xlim(0, 1)
plt.tick_params(axis='both', labelsize=16)
# Adicionar os valores de correlação na ponta de cada barra
for i, v in enumerate(correlations):
    plt.text(v + 0.01, i, f"{v:.2f}", va='center', fontsize=16)

# Melhorar layout
plt.tight_layout()

# Salvar o gráfico
plt.savefig('/mnt/beegfs/bianca.fusinato/monan/MASTERS_RESULTS/helene_rainfall_statistics/helene_correlation/pearson_correlation_helene.png', dpi=300)