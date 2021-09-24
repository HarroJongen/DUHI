#Title: SatelliteToTimeseries
#Date: 23-07-2020
#Author: Harro Jongen
#Builds a timeseries for single location from a series of maps

def SatelliteToTimeseries(location, coordinates, start, end):
    import numpy as np
    import pandas as pd
    import os.path
    from netCDF4 import Dataset as NetCDFFile 

    #Create lat and lon variables
    lat, lon = coordinates
    
    #Create dataframe for timeseries including all dates
    df = pd.DataFrame(columns = ['date', 'sm'])
    df['date'] = pd.date_range(start, end)
    df = df.set_index('date')
    
    #For every date
    for date in df.index:
        print('Extracting value for ' + str(date))
        #Define filepath
        filepath = ('Data/SoilMoisture/ESACCI-COMBINED/' + date.strftime('%Y') +\
                     '/ESACCI-SOILMOISTURE-L3S-SSMV-COMBINED-' + date.strftime('%Y')\
                         + date.strftime('%m') + date.strftime('%d') + '000000-fv06.1.nc')        
        #Check if file exists
        if os.path.isfile(filepath):
            #Open file
            nc = NetCDFFile(filepath, 'r')
            
            #Store lat and lon variables
            lats = nc.variables['lat'][:]
            lons = nc.variables['lon'][:]
            
            #Squared difference between the specified lat,lon and the lat,lon of the netCDF 
            sq_diff_lat = (lat - lats)**2 
            sq_diff_lon = (lon - lons)**2
            
            # Identify the index of the min value for lat and lon
            min_index_lat = sq_diff_lat.argmin()
            min_index_lon = sq_diff_lon.argmin()
            
            # Accessing the average temparature data
            sm = nc.variables['sm']
            
            #Save value of closest location
            df.loc[date, 'sm'] = float(sm[0, min_index_lat, min_index_lon].data)
             
        else:
            print('No file available for ' + str(date))
            
    df = df.replace(0,np.NaN)
    
    df.to_csv('Data/' + location + '_rs_SoilMoisture.csv')



