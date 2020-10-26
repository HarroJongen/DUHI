#Title: Soil moisture range map
#Date: 18-09-2020
#Author: Harro Jongen
#Builds a map with the range of soil moisture for every location

import numpy as np
import pandas as pd
import os.path
from netCDF4 import Dataset
import netCDF4 as nc
import datetime
import winsound
import math
from geopy.geocoders import Nominatim
from mpl_toolkits.basemap import Basemap

from Functions import SatelliteToTimeseries

filename = 'Data/SoilMoisture/SoilMoistureRanges.nc'

start = datetime.datetime(2017,1,2)
end = datetime.datetime(2019,12,31)

#%% Create NetCDF with  soil moisture range
 
ds = nc.Dataset(filename, 'w', format='NETCDF4') 

time = ds.createDimension('time', None)
lat = ds.createDimension('lat', 720)
lon = ds.createDimension('lon', 1440)

times = ds.createVariable('time', 'f4', ('time',))
lats = ds.createVariable('lat', 'f4', ('lat',))
lons = ds.createVariable('lon', 'f4', ('lon',))
sm_max = ds.createVariable('sm_max', 'f4', ('time', 'lat', 'lon',))
sm_min = ds.createVariable('sm_min', 'f4', ('time', 'lat', 'lon',))
sm_range = ds.createVariable('sm_range', 'f4', ('time', 'lat', 'lon',))
sm_max.units = 'Fraction [-]'
sm_min.units = 'Fraction [-]'
sm_range.units = 'Fraction [-]'

lats[:] = np.flip(np.arange(-90.0, 90.0, 0.25))
lons[:] = np.arange(-180.0, 180.0, 0.25)

filepath = ('Data/SoilMoisture/ESACCI-COMBINED/2017/ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-20170101000000-fv04.7.nc')      
nc = Dataset(filepath, 'r')
sm_day = nc.variables['sm']
sm = sm_day[0,:,:].data
sm[sm == -9999] = np.nan
sm_max[0, :, :] = sm
sm_min[0, :, :] = sm
nc.close()
      
#For every date
for date in pd.date_range(start, end):
    print('Extracting values for ' + str(date))
    #Define filepath
    filepath = ('Data/SoilMoisture/ESACCI-COMBINED/' + date.strftime('%Y') +\
                 '/ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-' + date.strftime('%Y')\
                     + date.strftime('%m') + date.strftime('%d') + '000000-fv04.7.nc')        
    #Check if file exists
    if os.path.isfile(filepath):
        #Open file
        nc = Dataset(filepath, 'r')
                  
        # Accessing the soil moisture data
        sm_day = nc.variables['sm']
        sm = sm_day[0,:,:].data
        sm[sm == -9999] = np.nan
        
        sm_max[0, :, :] = np.fmax(sm, sm_max[0, :, :])
        sm_min[0, :, :] = np.fmin(sm, sm_min[0, :, :])
        
        nc.close()
        
    else:
        print('No file available for ' + str(date))
        



sm_range[0,:,:] = sm_max[0, :, :] - sm_min[0, :, :]
ds.close()

winsound.Beep(440, 1500)



#%% Plot result
ds = nc.Dataset(filename, 'r') 
lats = ds.variables['lat'][:]
lons = ds.variables['lon'][:]
sm = ds.variables['sm_range'][:]
ds.close()
m = Basemap(projection='kav7',lon_0=0,resolution='i')
lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)
m.pcolor(xi,yi,np.squeeze(sm), cmap='gist_earth_r')
m.drawcountries()
m.drawcoastlines()
m.colorbar()

#%% Specific sites

#Create dataframe for 
df = pd.DataFrame(columns=['city', 'range_city', 'range_north', 'range_south', 'range_west', 'range_east'])
#Create agent to retrieve coordinates
geolocator = Nominatim(user_agent="DUHI")

#For every city
cities = ['Toulouse', 'Berlin', 'Hannover', 'Amsterdam', 'Rotterdam', 'London', 'Gent', 'Leuven', 'Boekarest', 'Enschede', 'Madrid', 'Barcelona', 'Rome', 'Milaan', 'Helsinki', 'Singapore']
# cities = ['Amsterdam', 'Rotterdam', 'Gent']
for city in cities:
    print('Extracting satellite soil moisture data for ' + city)
    #Define location
    location = geolocator.geocode(city)
    #Calculate the amount of degree per 30 km
    west_east = 30/(math.cos(math.radians(location.latitude)) * 111.321)
    
    #Build remote soil moisture time series for city and surroundings
    SatelliteToTimeseries.SatelliteToTimeseries(city, (location.latitude, location.longitude), start, end)
    SatelliteToTimeseries.SatelliteToTimeseries(city + '_North', (location.latitude+0.25, location.longitude), start, end)
    SatelliteToTimeseries.SatelliteToTimeseries(city + '_South', (location.latitude-0.25, location.longitude), start, end)
    SatelliteToTimeseries.SatelliteToTimeseries(city + '_West', (location.latitude, location.longitude+west_east), start, end)
    SatelliteToTimeseries.SatelliteToTimeseries(city + '_East', (location.latitude, location.longitude-west_east), start, end)
    
    #Read dataframe with soil moisture
    df_city = pd.read_csv('Data/' + city + '_rs_SoilMoisture.csv')
    df_north = pd.read_csv('Data/' + city + '_North' + '_rs_SoilMoisture.csv')
    df_south = pd.read_csv('Data/' + city + '_South' + '_rs_SoilMoisture.csv')
    df_west = pd.read_csv('Data/' + city + '_West' + '_rs_SoilMoisture.csv')
    df_east = pd.read_csv('Data/' + city + '_East' + '_rs_SoilMoisture.csv')
    #Calculate soil moisture range
    range_city = np.nanmax(df_city['sm']) - np.nanmin(df_city['sm'])
    range_north = np.nanmax(df_north['sm']) - np.nanmin(df_north['sm'])
    range_south = np.nanmax(df_south['sm']) - np.nanmin(df_south['sm'])
    range_west = np.nanmax(df_west['sm']) - np.nanmin(df_west['sm'])
    range_east = np.nanmax(df_east['sm']) - np.nanmin(df_east['sm'])
    df = df.append({'city': city, 'range_city': range_city, 'range_north' : range_north, 'range_south' : range_south, 'range_west' : range_west, 'range_east' : range_east}, ignore_index=True)
    winsound.Beep(440, 100)

df.to_csv('Data/temp.csv')

winsound.Beep(440, 1500)

