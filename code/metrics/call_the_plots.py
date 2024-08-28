from plot_metrics_txt import *
from percentile_data import *

time_indices_dict = {
    "january": range(0, 744),
    "february": range(0, 672),
    "march": range(0, 744),
    "august": range(0, 744),
    "september": range(0, 720),
    "october": range(0, 744),
}

# Diurnal Cycle
diurnal_cycle(rawprec_era_january_2013, time_indices_dict['january'], 'January', '2013', 'january2013_DC.png')
diurnal_cycle(rawprec_era_january_2014, time_indices_dict['january'], 'January', '2014', 'january2014_DC.png')
diurnal_cycle(rawprec_era_january_2015, time_indices_dict['january'], 'January', '2015', 'january2015_DC.png')

diurnal_cycle(rawprec_era_february_2013, time_indices_dict['february'], 'February', '2013', 'february2013_DC.png')
diurnal_cycle(rawprec_era_february_2014, time_indices_dict['february'], 'February', '2014', 'february2014_DC.png')
diurnal_cycle(rawprec_era_february_2015, time_indices_dict['february'], 'February', '2015', 'february2015_DC.png')

diurnal_cycle(rawprec_era_march_2013, time_indices_dict['march'], 'March', '2013', 'march2013_DC.png')
diurnal_cycle(rawprec_era_march_2014, time_indices_dict['march'], 'March', '2014', 'march2014_DC.png')
diurnal_cycle(rawprec_era_march_2015, time_indices_dict['march'], 'March', '2015', 'march2015_DC.png')

diurnal_cycle(rawprec_era_august_2013, time_indices_dict['august'], 'August', '2013', 'august2013_DC.png')
diurnal_cycle(rawprec_era_august_2014, time_indices_dict['august'], 'August', '2014', 'august2014_DC.png')
diurnal_cycle(rawprec_era_august_2015, time_indices_dict['august'], 'August', '2015', 'august2015_DC.png')

diurnal_cycle(rawprec_era_september_2013, time_indices_dict['september'], 'September', '2013', 'september2013_DC.png')
diurnal_cycle(rawprec_era_september_2014, time_indices_dict['september'], 'September', '2014', 'september2014_DC.png')
diurnal_cycle(rawprec_era_september_2015, time_indices_dict['september'], 'September', '2015', 'september2015_DC.png')

diurnal_cycle(rawprec_era_october_2013, time_indices_dict['october'], 'October', '2013', 'october2013_DC.png')
diurnal_cycle(rawprec_era_october_2014, time_indices_dict['october'], 'October', '2014', 'october2014_DC.png')
diurnal_cycle(rawprec_era_october_2015, time_indices_dict['october'], 'October', '2015', 'october2015_DC.png')

# Diurnal Cycle With the metric:
def process_diurnal_cycle(month, year):
    month_dict = {
        'january': 'January',
        'february': 'February',
        'march': 'March',
        'august': 'August',
        'september': 'September',
        'october': 'October'
    }
    file_ERA5 = f'/home/bianca.fusinato/output/metrics/{year}{month}.txt'
    L_org_ERA5 = ler_matriz(file_ERA5)
    ciclo_diurno = calcular_ciclo_diurno(L_org_ERA5)
    rawprec_var = f'rawprec_era_{month}_{year}'
    diurnal_cycle_Lorg(globals()[rawprec_var], ciclo_diurno, time_indices_dict[month], month_dict[month], year, f'{month}{year}_DCLORG.png')
    
def process_diurnal_cycle_panel(month1, year1, month2, year2, month3, year3):
    month_dict = {
        'january': 'January',
        'february': 'February',
        'march': 'March',
        'august': 'August',
        'september': 'September',
        'october': 'October'
    }
    
    data_info_list = []
    
    for month, year in zip([month1, month2, month3], [year1, year2, year3]):
        file_ERA5 = f'/home/bianca.fusinato/output/metrics/{year}{month}.txt'
        L_org_ERA5 = ler_matriz(file_ERA5)
        ciclo_diurno = calcular_ciclo_diurno(L_org_ERA5)
        rawprec_var = f'rawprec_era_{month}_{year}'
        
        data_info_list.append((
            globals()[rawprec_var], 
            ciclo_diurno, 
            time_indices_dict[month], 
            month_dict[month], 
            year, 
            f'{month}{year}_DCLORG.png'
        ))
    
    diurnal_cycle_Lorg_panel(data_info_list, f'{month1}_{year1}_{month2}_{year2}_{month3}_{year3}_panel.png')

def process_time_series_panel(month1, year1, month2, year2, month3, year3):
    month_dict = {
        'january': 'January',
        'february': 'February',
        'march': 'March',
        'august': 'August',
        'september': 'September',
        'october': 'October'
    }
    
    # Dicionário para mapear a combinação de mês e ano para as variáveis `rawprec_era`
    rawprec_era_dict = {
        ('january', '2013'): rawprec_era_january_2013,
        ('february', '2013'): rawprec_era_february_2013,
        ('march', '2013'): rawprec_era_march_2013,
        ('august', '2013'): rawprec_era_august_2013,
        ('september', '2013'): rawprec_era_september_2013,
        ('october', '2013'): rawprec_era_october_2013,
        ('january', '2014'): rawprec_era_january_2014,
        ('february', '2014'): rawprec_era_february_2014,
        ('march', '2014'): rawprec_era_march_2014,
        ('august', '2014'): rawprec_era_august_2014,
        ('september', '2014'): rawprec_era_september_2014,
        ('october', '2014'): rawprec_era_october_2014,
        ('january', '2015'): rawprec_era_january_2015,
        ('february', '2015'): rawprec_era_february_2015,
        ('march', '2015'): rawprec_era_march_2015,
        ('august', '2015'): rawprec_era_august_2015,
        ('september', '2015'): rawprec_era_september_2015,
        ('october', '2015'): rawprec_era_october_2015
    }
    
    data_info_list = []
    
    for month, year in zip([month1, month2, month3], [year1, year2, year3]):
        file_ERA5 = f'/home/bianca.fusinato/output/metrics/{year}{month}.txt'
        L_org_ERA5 = ler_matriz(file_ERA5)
        
        # Recupera o rawprec_var correto do dicionário
        rawprec_var = rawprec_era_dict[(month.lower(), year)]
        
        data_info_list.append((L_org_ERA5, rawprec_var, month_dict[month.lower()], year))
    
    L_org_list = [info[0] for info in data_info_list]
    rawprec_era_month_list = [info[1] for info in data_info_list]
    months = [info[2] for info in data_info_list]
    years = [info[3] for info in data_info_list]
    save_name = f'{month1}_{year1}_{month2}_{year2}_{month3}_{year3}_TSpanel.png'
    
    # Passa as listas e save_name para a função de plotagem
    plot_TimeSeries_L_org_precip_panel(L_org_list, rawprec_era_month_list, months, years, save_name)

# Chamada da função
months = ['january', 'february', 'march', 'august', 'september', 'october']
years = ['2013', '2014', '2015']

# Time Series:
for month in months:
    process_time_series_panel(month, '2013', month, '2014', month, '2015')


#for year in years:
#    for month in months:
#        process_diurnal_cycle(month, year)

#for month in months:
#    process_diurnal_cycle_panel(month, '2013', month, '2014', month, '2015')

'''

dir_base = '/home/bianca.fusinato/output/metrics/'
anos = [2013, 2014, 2015]
#meses = ['january', 'february', 'march', 'august', 'september', 'october']
meses = ['january']
nome_arquivo = '{ano}{mes}.txt'

plot_multi_timeseries(dir_base, anos, meses, nome_arquivo, rawprec_era_month)            


plot_TimeSeries_L_org_precip(L_org_ERA5_january2013, rawprec_era_january_2013, 'January', '2013', 'plot_january2013.png')
'''
'''
file_ERA5 = '/home/bianca.fusinato/output/metrics/2014january.txt'
L_org_ERA5 =  ler_matriz(file_ERA5)
plot_TimeSeries_L_org(L_org_ERA5, 'time_series_january2014.png', 'Janeiro 2014')

file_ERA5 = '/home/bianca.fusinato/output/metrics/2015january.txt'
L_org_ERA5 =  ler_matriz(file_ERA5)
plot_TimeSeries_L_org(L_org_ERA5, 'time_series_january2015.png', 'Janeiro 2015')
'''