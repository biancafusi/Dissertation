import uxarray as ux
import numpy
import geoviews.feature as gf
import cartopy.crs as ccrs
import holoviews as hv
import hvplot.pandas
import numpy as np

hv.extension("matplotlib")

import matplotlib

matplotlib.use("Agg")  # Evita abrir janela se rodando em servidor

# Abrir os arquivos
data_path = '/mnt/beegfs/bianca.fusinato/monan/model/beryl_cporg1_gustf1_sub3d0_GFdef_ERA5_x1.655362/2024070300/diag/backup/diag.2024-07-04_12.00.00.nc'
grid_path = '/mnt/beegfs/bianca.fusinato/monan/model/mesh/30km/x1.655362.grid.nc'

mpas_ds = ux.open_mfdataset(grid_path, data_path, concat_dim="Time", combine="nested")

# Subconjunto espacial
lon_bounds = (-106, -89)
lat_bounds = (20, 40)
rain_sub = mpas_ds["rainnc"].subset.bounding_box(lon_bounds, lat_bounds)
rain_sub_plot = rain_sub.isel(Time=0)
rain_sub_plot.name = "Rainfall [mm]"

# Limites de cores (veja os valores reais)
min_val = float(rain_sub.isel(Time=0).values.min())
max_val = float(rain_sub.isel(Time=0).values.max())
print(f"Chuva acumulada varia entre {min_val:.2f} e {max_val:.2f} mm")

# # Ajustar os limites conforme necessidade
clim = (0, 20)  # Força pelo menos até 10 mm se os valores forem muito baixos
# clim = np.log(0,50)
# Features geográficos
features = (
    gf.coastline(scale="10m", projection=ccrs.PlateCarree())
    * gf.borders(scale="10m", projection=ccrs.PlateCarree())
    * gf.states(scale="10m", projection=ccrs.PlateCarree())
)

# Plotagem
plot = (
    rain_sub_plot.plot.rasterize(
        method="polygon",
        backend="matplotlib",
        title="Accumulated Non-Convective Rainfall (mm) \n from 07-03T00 until 07-04T12",
        cmap="Blues",
        pixel_ratio=2.0,
        fig_inches=(12, 8),
        clim=clim,
        colorbar_opts={"label": "Rainfall [mm]"},

    )
    * features
)

import matplotlib.pyplot as plt
renderer = hv.renderer('matplotlib')
fig = renderer.get_plot(plot).state
fig.savefig('rain_plot.png', dpi=300, bbox_inches='tight')
