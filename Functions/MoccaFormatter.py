#Title: Mocca data format function
#Date: 30-06-2020
#Author: Harro Jongen
#Formats data of Mocca to csv

def MoccaFormatter(start, end, overwrite = True):
    import pandas as pd
    import os.path
    import glob
    import numpy as np

   
 

    #For every location
    for loc in ['grm', 'slp', 'bas', 'snz', 'hap', 'doc']:
        #Define saving filename
        if loc == 'doc':
            filepath = 'Data/Gent_rural.csv'
            land = 'rural'
        else:
            filepath = 'Data/Gent_' + loc + '_urban.csv'
            land = 'urban'
            
        #Check whether file does not exists or whether it should be overwritten
        if overwrite or not os.path.isfile(filepath):
            #Create dataframe for timeseries including all timestamps
            df = pd.DataFrame(columns = ['date', 'T_' + land, 'u_' + land, 'P_' + land, 'RH_' + land])
            df['date'] = pd.date_range(start, end, freq='H')
            df.set_index('date', inplace=True)
            df = df.resample('H').sum()
            df = df.replace(0, np.NaN)
            
            #For every date
            Timeline =  pd.date_range(start, end, freq='M')
            for month, year in zip(Timeline.strftime('%m'), Timeline.year):
                print('Extracting values for ' + str(month) + '-' + str(year))
                
                #Define filepaths
                Files = glob.glob('Data/Gent/' + str(year) + '/' + str(month) + '/' + '*_' + loc + '.dat')
                
                #For every file
                for file in Files:
                    df_day = pd.read_csv(file, names=['number', 'T_' + land, 'T_pas', 'RH_' + land, 'u_max', 'u_' + land, 'u_dir', 'u_var', 'P_' + land, 'freq', 'battery'], na_values='NAN')
                    
                    if len(df_day) != 0:
                        #RH to %
                        df_day['RH_' + land] = df_day['RH_' + land] * 100
                        
                        #Resample to hourly data
                        df_day.index = pd.to_datetime(df_day.index)
                        df_day.index = df_day.index.rename('date')
                        df_day = df_day.apply(pd.to_numeric)
                        df_sum = df_day.resample('H').sum()
                        df_mean = df_day.resample('H').mean()
                        
                        df_day = df_mean.drop(['number', 'T_pas', 'u_max', 'u_dir', 'u_var', 'P_' + land, 'freq', 'battery'], axis=1)
                        df_day['P_' + land] = df_sum['P_' + land]
                        
                        #Save value of closest location
                        df.loc[(df.index >= df_day.index[0]) & (df.index <= df_day.index[-1])] = df_day
            
            #Write to csv file
            if land == 'urban':
                df.to_csv(filepath, columns = (['T_' + land, 'u_' + land, 'P_' + land, 'RH_' + land]), index = True)
            else:
                df['p_' + land] = np.nan
                df.to_csv(filepath, columns = (['T_' + land, 'u_' + land, 'P_' + land, 'p_' + land, 'RH_' + land]), index = True)
