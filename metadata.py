#Title: Metadata collector
#Date: 23-07-2020
#Author: Harro Jongen
#Script for gathering metadata based on coordinates


###IMPORTING###

import pandas as pd
import numpy as np
import rasterio
import geopandas as gpd
from rasterio.plot import show
import matplotlib.pyplot as plt

###FORMATTING DATA###

#Read metadata and create point features for the locations
df = pd.read_csv('Data/Metadata/Locations.csv')
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Lon_urban'], df['Lat_urban']))
gdf.crs = "EPSG:4326"
gdf = gdf.to_crs({'init': 'epsg:28992'})



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

#Populations statistics
#Read shapefile with populaiton statistics
PopStat = gpd.read_file('Data/Population/bevolkingskern_2011.shp')
#If coordinate reference systems are equal
if PopStat.crs == gdf.crs:
    #Join attributes of the 'bevolkingskernen' to the points of the measurement stations
    join = gpd.sjoin(gdf, PopStat, how="left", op="within")

#Add the colums of interest to the dataframe
df.loc[df['City'] != 'Gent', 'Inhabitants'] = join.loc[join['City'] != 'Gent', 'BEV11TOT']
df.loc[df['City'] != 'Gent', 'Area'] = join.loc[join['City'] != 'Gent', 'OPPTOT']
df.loc[df['City'] != 'Gent', 'Popdens'] = join.loc[join['City'] != 'Gent', 'BEV11TOT']/join.loc[join['City'] != 'Gent', 'OPPTOT']*100

#Save update metadata
df.to_csv('Data/Metadata/Locations.csv', index=False)
for item in range(len(gdf)):
    gdf.loc[item, 'Lat_urban'] = gdf['geometry'][item].coords[0][1]
    gdf.loc[item, 'Lon_urban'] = gdf['geometry'][item].coords[0][0]
    
gdf.to_csv('Data/Metadata/Locations_rd.csv', index=False)

###VISUALIZATION###

#Make a map of LCZ and locations
fig, ax = plt.subplots(figsize=(10, 10))
PopStat.plot(ax=ax, color='blue')
gdf.plot(ax=ax, markersize=5, color='red')
plt.show()
    
