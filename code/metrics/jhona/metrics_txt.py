'''
This code calculates the organization indexes in .txt
'''

import f_metrix as f

data          = '/home/bianca.fusinato/output/binary_matrix/era5J/'
out_file      = '/mnt/beegfs/bianca.fusinato/dados_mestrado/python_plots/Dissertation/code/metrics/jhona/output/teste.txt'

indices_range = range(0,745)

part01 = range(0,10)
part02 = range(186,372)
part03 = range(372,558)
part04 = range(558,744)

f.indices_varying_rmax(data, part01, out_file, prefix='ERA5')
