#Title: Cabauw soil moisture formatter
#Date: 23-07-2020
#Author: Harro Jongen
#Formats the Cabauw data into a single soil moisture timeseries

def FormatterCabauw(folderpath, start, end):
    import pandas as pd
    import numpy as np
    import os.path
    from netCDF4 import Dataset as NetCDFFile
    from calendar import monthrange
    import datetime

    
    #Create dataframe for timeseries including all dates
    df = pd.DataFrame(columns = ['date', 'month', 'sm03', 'sm05', 'sm08', 'sm019', 'sm20', 'sm33', 'sm40', 'sm56'])
    df['date'] = pd.date_range(start, end)
    df = df.set_index('date')
    df['month'] = df.index.to_period('M')

    #For every month
    for date in df.month.unique():
        #Define new filepath
        filepath =  folderpath + str(date.year) + '/' + str(date.strftime('%m'))\
                        + '/01/cesar_soil_water_lb1_t10_v1.1_' + str(date.year)\
                        + str(date.strftime('%m')) + '.nc'
        #Check if file exists
        if os.path.isfile(filepath):
            #Read file
            nc = NetCDFFile(filepath, 'r')
            
            #Create dataframe for month data with 10 minute intervals
            start_month = date.to_timestamp()
            end_month = start_month.replace(day = monthrange(date.year, date.month)[1], hour = 23, minute = 50)
            df_month = pd.DataFrame(columns = ['date', 'sm03', 'sm05', 'sm08', 'sm019', 'sm20', 'sm33', 'sm40', 'sm56'])
            df_month['date'] = pd.date_range(start=start_month, end=end_month , freq='10T')
            df_month = df_month.set_index('date')
            
            #Read variables
            df_month['sm_03'] = nc.variables['TH03'][:]
            df_month['sm_05'] = nc.variables['TH05'][:]
            df_month['sm_08'] = nc.variables['TH08'][:]
            df_month['sm_19'] = nc.variables['TH19'][:]
            df_month['sm_20'] = nc.variables['TH20'][:]
            df_month['sm_33'] = nc.variables['TH33'][:]
            df_month['sm_40'] = nc.variables['TH40'][:]
            df_month['sm_56'] = nc.variables['TH56'][:]
            
            #Close NetCDFFile
            nc.close()
            
            #Replace -9999 with NaN
            df_month = df_month.replace(-9999,np.NaN)
            
            #Resample to daily
            df_month = df_month.resample(datetime.timedelta(1)).mean()
            
            #Fill month values into total dataframe
            df = df.combine_first(df_month)
            
        else:
            print('No file available for ' + str(date))
    
    #Save dataframe
    df = df.drop(['month'], axis=1)
    df.to_csv('Data/Cabauw_SoilMoisture.csv', )
                
        