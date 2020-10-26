#Title: GlobalMapSoilMoisture
#Date: 23-07-2020
#Author: Harro Jongen
#Draws a global map of the soil moisture for a given filepath

def GlobalMapSoilMoisture(filepath):
    from netCDF4 import Dataset as NetCDFFile 
    import numpy as np
    from mpl_toolkits.basemap import Basemap
    
    nc = NetCDFFile(filepath)
    lats = nc.variables['lat'][:]
    lons = nc.variables['lon'][:]
    sm = nc.variables['sm_range'][:]
    nc.close()
    m = Basemap(projection='kav7',lon_0=0,resolution='l')
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)
    m.pcolor(xi,yi,np.squeeze(sm))
    m.drawcountries()
    m.drawcoastlines()
    m.colorbar()

    