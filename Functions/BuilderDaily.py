#Title: Daily dataset builder
#Date: 14-07-2020
#Author: Harro Jongen
#Resamples the data set to daily calculating variables API, T_max, UHI_max and DTR

def BuilderDaily(file, k_API = [0.85]):
    import pandas as pd
    import datetime
    from Functions import DTRCalculator
    import numpy as np
    import re
    import os.path
    
    print('Creating daily dataset for ' + file)
    
    #Read csv to dataframe
    df = pd.read_csv(file)
    #Set date to datetime format and make it index
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    #Define timestep as 1 day
    dt = datetime.timedelta(1)
        
    #Resample to daily using the maximum for T_max and UHI_max
    df_daily = df.resample(dt).max()
    df_daily = df_daily.rename(columns = {'T_urban' : 'T_max_urban', 'T_rural' : 'T_max_rural', 'UHI' : 'UHI_max'})
    
    #Resample to daily using the data range for DTR
    df_range = df.resample(dt).apply(DTRCalculator.DTRCalculator)
    df_range = df_range.rename(columns = {'T_urban' : 'DTR_urban', 'T_rural' : 'DTR_rural'})
    
    #Resample to daily using the sum for UHI_int API
    df_sum = df.resample(dt).sum()
    df_sum = df_sum.rename(columns = {'UHI' : 'UHI_int'})
    
    #Normalized UHI_max 
    #Define for which city the data needs to be loaded
    regex = re.compile(r'Data[\\/]([A-Za-z]+)_?[0-9]*_[A-Za-z0-9]+_total.csv')
    City = regex.search(file).group(1)
    #Load data for normalization
    if os.path.exists('Data/UHI_Norms_' + City + '.csv'):
        UHI_norms = pd.read_csv('Data/UHI_Norms_' + City + '.csv')
        UHI_norms = UHI_norms.set_index('date')
        #Perform calculation
        df_daily['Norm'] = UHI_norms['Norm']
    else:
        df_daily['Norm'] = np.nan
    
    #API calculation
    cols = []
    #For all k_API
    for k in k_API:
        #For both urban and rural
        for item in ['P_urban', 'P_rural']:
            #Check for precipitation data
            if item in df.columns:
                #Create API column
                col = 'API' + str(k) + item[-6:]
                cols += [col]
                df_sum[col] = np.nan
                #Calculate API based on formula: API_{d} = P_{d} + kP_{d-1} + k^{2}P_{d-2}+... upto 20 days
                for row in range(len(df_sum)):
                    #Adapt formula to limited data for days before (at start of file)
                    if row > 19:
                        df_sum[col][row] = 0
                        for number in range(20):
                            df_sum[col][row] += k**number * df_sum[item][row-number]
    
  
    #Remove unnessary data and add all available variables to one dataframe
    df_daily = df_daily.drop(columns = ['u_urban', 'RH_urban', 'u_rural', 'P_rural', 'p_rural', 'RH_rural'])
    df_daily['DTR_urban'] = df_range['DTR_urban']
    df_daily['DTR_rural'] = df_range['DTR_rural']
    df_daily['UHI_int'] = df_sum['UHI_int']
    df_daily['UHI_int'] = df_daily['UHI_int'].replace('0',np.NaN)
    for key in cols:
        if key in df_sum.columns:
            df_daily[key] = df_sum[key]
    
    #Write dataframe to csv
    df_daily.to_csv(file[0:-9] + 'daily.csv')
