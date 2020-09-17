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
with rasterio.open('Data/Maps/LCZ_Netherlands_lcz2_clip.tif') as src:
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
PopStat100 = gpd.read_file('Data/Maps/Population/CBS_VK100_2018_v1.shp')
PopStat100 = PopStat100.replace(-99997,np.NaN)
#If coordinate reference systems are equal
if PopStat100.crs == gdf.crs:
    #Join attributes of the population statistics to the points of the measurement stations
    join = gpd.sjoin(gdf, PopStat100, how="left", op="within")

    #Add the colums of interest to the dataframe
    df.loc[df['City'] != 'Gent', 'Inhabitants100'] = join.loc[join['City'] != 'Gent', 'INWONER']
    df.loc[df['City'] != 'Gent', 'Popdens100'] = df.loc[df['City'] != 'Gent', 'Inhabitants100']/0.01

#Read shapefile with populaiton statistics 500m square
PopStat500 = gpd.read_file('Data/Maps/Population/CBS_VK500_2018_v1.shp')
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
Soil = gpd.read_file('Data/Maps/Soil/Soil_map.shp')
Soil = Soil.rename(columns={'map_area_i': 'map_area_id'})
Soil_info = pd.read_csv('Data/Maps/Soil/Soil_info.txt')
Soil_codes = pd.read_csv('Data/Maps/Soil/Soil_codes.txt')

#Join tables to the shapefile
Soil = Soil.set_index('map_area_id').join(Soil_info.set_index('map_area_id'))
Soil = Soil.set_index('soil_unit_code').join(Soil_codes.set_index('code'))

#If coordinate reference systems are equal
if Soil.crs == gdf.crs:
    #Join attributes of the soil map to the points of the measurement stations
    join = gpd.sjoin(gdf, Soil, how="left", op="within")
    join = join.drop_duplicates(subset = ['Locations', 'City'])
    df.loc[df['City'] != 'Gent', 'Soil'] = join.loc[join['City'] != 'Gent', 'main_soil_classification']
    
#%%Seepage

#Read seepage raster data
with rasterio.open('Data/Maps/KEA/Seepage.tif') as src:
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

Surface = gpd.read_file('Data/Maps/KEA/Neighbourhoods.shp')
#If coordinate reference systems are equal
if Surface.crs == gdf.crs:
    #Join attributes of the sealed fraction map to the points of the measurement stations
    join = gpd.sjoin(gdf, Surface, how="left", op="within")
    df.loc[df['City'] != 'Gent', 'P_sealed'] = join.loc[join['City'] != 'Gent', 'P_verhard']
    df.loc[df['City'] != 'Gent', 'P_green'] = 100 - join.loc[join['City'] != 'Gent', 'P_verhard'] - join.loc[join['City'] != 'Gent', 'p_water']
  
    

#%%
#SVF
Mapindex = gpd.read_file('Data/Maps/SVF/Kaartbladen.shp')

if Mapindex.crs == gdf.crs:
    #Join attributes of the svf map to the points of the measurement stations
    join = gpd.sjoin(gdf, Mapindex, how="left", op="within")
    ls = sorted(join['Kaartblad'].unique()[~pd.isnull(join['Kaartblad'].unique())])
    
    print('Download and put in the folder Data/Maps/SVF the SVF data from https://dataplatform.knmi.nl/catalog/datasets/index.html?x-dataset=SVF_NL&x-dataset-version=3 for the mapindices: ')
    print(*ls, sep = "\t")
    
    download = input("Have you downloaded all files? [y/n] ")
    while download != 'y':
        download = input("Have you downloaded all files? [y/n] ")
    for item in range(len(df)):
        try:
            if np.isnan(df.iloc[item]['SVF']) and ~np.isnan(df.iloc[item]['Lat_urban']) and df.iloc[item]['City'] != 'Gent':
                with rasterio.open('Data/Maps/SVF/SVF_r'+ join['Kaartblad'][item] +'.tif') as src:
                    SVF = src.read(1)
                    #Determine the corresponding row and column in raster
                    row, col = src.index(gdf.iloc[item]['RD_Lon_urban'], gdf.iloc[item]['RD_Lat_urban'])
                    df.at[item, 'SVF'] = SVF[row, col]
        except:
            print('Data/Maps/SVF/SVF_r'+ join['Kaartblad'][item] +'.tif is not available.')
        
        
df.loc[df['SVF']>1, 'SVF'] = df.loc[df['SVF']>1, 'SVF'] / 100
df = df.replace(-3.4000000000000003e+38,np.NaN)

#%%
#Save update metadata
df.to_csv('Data/Metadata/Locations.csv', index=False)
    
gdf.to_csv('Data/Metadata/Locations_rd.csv', index=False)


#%%
###VISUALIZATION###

#Make a map of LCZ and locations
fig, ax = plt.subplots(figsize=(10, 10))
Mapindex.plot(ax=ax, color='blue')
show(src)
Soil.plot(ax=ax, color='blue')
Surface.plot(ax=ax, color='blue')
PopStat100.plot(ax=ax, color='blue')
gdf.plot(ax=ax, markersize=5, color='red')
plt.show()
    
