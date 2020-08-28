#Title: Metadata collector
#Date: 23-07-2020
#Author: Harro Jongen
#Script for gathering metadata based on coordinates

#%%
###IMPORTING###

import pandas as pd
import numpy as np
import rasterio
import geopandas as gpd
import matplotlib.pyplot as plt
from rasterio.plot import show

#%%
###FORMATTING DATA###

#Read metadata and create point features for the locations
df = pd.read_csv('Data/Metadata/Locations.csv')
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Lon_urban'], df['Lat_urban']))
gdf.crs = "EPSG:4326"
gdf = gdf.to_crs({'init': 'epsg:28992'})
for item in range(len(gdf)):
    gdf.loc[item, 'RD_Lat_urban'] = gdf['geometry'][item].coords[0][1]
    gdf.loc[item, 'RD_Lon_urban'] = gdf['geometry'][item].coords[0][0]

#%%
#LCZ
#Read LCZ raster data
with rasterio.open('Data/LCZ/LCZ_Netherlands_lcz2_clip.tif') as src:
    LCZ = src.read(1)
    
    #For every location
    for item in range(len(df)):
        #If LCZ is unknown and location is known
        if np.isnan(df.iloc[item]['LCZ']) & ~np.isnan(df.iloc[item]['Lat_urban']):
            #Determine the corresponding row and column in raster
            row, col = src.index(df.iloc[item]['Lon_urban'], df.iloc[item]['Lat_urban'])
            df.at[item, 'LCZ'] = LCZ[row, col]

#%%
#Populations statistics
#Read shapefile with populaiton statistics 100m square
PopStat100 = gpd.read_file('Data/Population/CBS_VK100_2018_v1.shp')
PopStat100 = PopStat.replace(-99997,np.NaN)
#If coordinate reference systems are equal
if PopStat100.crs == gdf.crs:
    #Join attributes of the population statistics to the points of the measurement stations
    join = gpd.sjoin(gdf, PopStat100, how="left", op="within")

    #Add the colums of interest to the dataframe
    df.loc[df['City'] != 'Gent', 'Inhabitants100'] = join.loc[join['City'] != 'Gent', 'INWONER']
    df.loc[df['City'] != 'Gent', 'Popdens100'] = df.loc[df['City'] != 'Gent', 'Inhabitants100']/0.01

#Read shapefile with populaiton statistics 500m square
PopStat500 = gpd.read_file('Data/Population/CBS_VK500_2018_v1.shp')
PopStat500 = PopStat500.replace(-99997,np.NaN)
#If coordinate reference systems are equal
if PopStat500.crs == gdf.crs:
    #Join attributes of the population statistics to the points of the measurement stations
    join = gpd.sjoin(gdf, PopStat500, how="left", op="within")
    df.loc[df['City'] != 'Gent', 'Inhabitants500'] = join.loc[join['City'] != 'Gent', 'INWONER']
    df.loc[df['City'] != 'Gent', 'Popdens500'] = df.loc[df['City'] != 'Gent', 'Inhabitants500']/0.25

#%%
#Soil
#Read shapefile and tables
Soil = gpd.read_file('Data/Soil/Soil_map.shp')
Soil = Soil.rename(columns={'map_area_i': 'map_area_id'})
Soil_info = pd.read_csv('Data/Soil/Soil_info.txt')
Soil_codes = pd.read_csv('Data/Soil/Soil_codes.txt')

#Join tables to the shapefile
Soil = Soil.set_index('map_area_id').join(Soil_info.set_index('map_area_id'))
Soil = Soil.set_index('soil_unit_code').join(Soil_codes.set_index('code'))

#If coordinate reference systems are equal
if Soil.crs == gdf.crs:
    #Join attributes of the soilo map to the points of the measurement stations
    join = gpd.sjoin(gdf, Soil, how="left", op="within")
    df.loc[df['City'] != 'Gent', 'Soil'] = join.loc[join['City'] != 'Gent', 'main_soil_classification']
    
#%%Seepage

#Read LCZ raster data
with rasterio.open('Data/KEA/Seepage.tif') as src:
    Seepage = src.read(1)
    
    #For every location
    for item in range(len(df)):
        #If LCZ is unknown and location is known and locations is in The Netherlands
        if np.isnan(df.iloc[item]['Seepage']) and ~np.isnan(df.iloc[item]['Lat_urban']) and df.iloc[item]['City'] != 'Gent':
            #Determine the corresponding row and column in raster
            row, col = src.index(gdf.iloc[item]['RD_Lon_urban'], gdf.iloc[item]['RD_Lat_urban'])
            df.at[item, 'Seepage'] = Seepage[row, col]
        
        
#%%
#Sealed fraction

Sealed = gpd.read_file('Data/KEA/groen.gdb',layer='buurt_groen_water_nodata')
#If coordinate reference systems are equal
if Sealed.crs == gdf.crs:
    #Join attributes of the soilo map to the points of the measurement stations
    join = gpd.sjoin(gdf, Sealed, how="left", op="within")
    df.loc[df['City'] != 'Gent', 'P_sealed'] = join.loc[join['City'] != 'Gent', 'P_verhard']
    
#%%
#Save update metadata
df.to_csv('Data/Metadata/Locations.csv', index=False)
    
gdf.to_csv('Data/Metadata/Locations_rd.csv', index=False)


#%%
###VISUALIZATION###

#Make a map of LCZ and locations
fig, ax = plt.subplots(figsize=(10, 10))
Soil.plot(ax=ax, color='blue')
PopStat.plot(ax=ax, color='blue')
gdf.plot(ax=ax, markersize=5, color='red')
plt.show()
    
