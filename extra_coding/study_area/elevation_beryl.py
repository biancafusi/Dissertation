import rioxarray as rxr
import matplotlib.pyplot as plt

# Caminho para o arquivo ETOPO1 baixado
# (ajuste para onde você salvar)
file_path = 'ETOPO1_Ice_g_gmt4.grd'  # exemplo, pode ser .tif também

# Abre o arquivo com rioxarray
dem = rxr.open_rasterio(file_path, masked=True).squeeze()

# Define limites da região
lonW, lonE = -106, -50
latS, latN = 5, 41

# Recorta a região desejada
dem_clip = dem.sel(x=slice(lonW, lonE), y=slice(latN, latS))  # lat invertido

# Normaliza os dados (oceano = 0 -> branco)
dem_data = dem_clip.data
dem_data = dem_data.astype(float)
dem_data[dem_data < 0] = 0
dem_data /= dem_data.max()
dem_data = 1 - dem_data  # invertendo para preto = maior relevo

# Plota
plt.figure(figsize=(10,8))
plt.imshow(dem_data, cmap='gray', extent=[lonW, lonE, latS, latN], origin='upper')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Mapa de relevo (ETOPO1) - Região')
plt.colorbar(label='Relevo (branco = nível do mar)')
plt.show()
