#Title: Daily dataset builder
#Date: 14-07-2020
#Author: Harro Jongen
#Resamples the data set to daily calculating variables API, T_max, UHI_max and DTR

def DailyBuilder(file, k_API = 0.85):
    import pandas as pd
    import datetime
    from Functions import DTRCalculator
    import numpy as np
        
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
    
    #API calculation
    #For both urban and rural
    for item in ['P_urban', 'P_rural']:
        #Check for precipitation data
        if item in df.columns:
            #Create API column
            col = 'API' + item[-6:]
            df_sum[col] = np.nan
            #Calculate API based on formula: API_{d} = P_{d} + kP_{d-1} + k^{2}P_{d-2}+... upto 20 days
            for row in range(len(df_sum)):
                #Adapt formula to limited data for days before (at start of file)
                if row < 20:
                    df_sum[col][row] = 0
                    for number in range(row+1):
                        df_sum[col][row] += k_API**number * df_sum[item][row-number]
                else:
                    df_sum[col][row] = 0
                    for number in range(20):
                        df_sum[col][row] += k_API**number * df_sum[item][row-number]
    
    #Remove unnessary data and add all available variables to one dataframe
    df_daily = df_daily.drop(columns = ['u_urban', 'RH_urban', 'u_rural', 'P_rural', 'p_rural', 'RH_rural'])
    df_daily['DTR_urban'] = df_range['DTR_urban']
    df_daily['DTR_rural'] = df_range['DTR_rural']
    df_daily['UHI_int'] = df_sum['UHI_int']
    for key in ['API_rural', 'API_urban']:
        if key in df_sum.columns:
            df_daily[key] = df_sum[key]
    
    #Write dataframe to csv
    df_daily.to_csv(file[0:-9] + 'daily.csv')
