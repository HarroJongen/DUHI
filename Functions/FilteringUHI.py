#Title: Filtering weather out of UHI
#Date: 04-09-2020
#Author: Harro Jongen
#Filtering function to exclude non urban effects on UHI

def FilteringUHI(dataframe_day, dataframe_hour):
    import pandas as pd
    import numpy as np
    
    df_d = pd.read_csv(dataframe_day)
    df_d['date'] = pd.to_datetime(df_d['date'])
    df_d.set_index('date', inplace=True)
    
    df_h = pd.read_csv(dataframe_hour)
    df_h['date'] = pd.to_datetime(df_h['date'])
    df_h.set_index('date', inplace=True)    
    
    #Filtering rain events
    df_sum = df_h.resample('D').sum()
    Filter_rain = df_sum['P_rural']<0.3

    #Filtering sudden wind changes
    df_h['change'] =  df_h['u_rural'] - df_h['u_rural'].shift(1)
    df_max = df_h.resample('D').max()
    Filter_wind = df_max['change']<2
    
    #Filtering fog
    df_mean = df_h.resample('D').mean()
    Filter_fog = df_mean['RH_rural']<80

    #Total filter
    Filters = pd.concat([Filter_fog, Filter_rain, Filter_wind], axis=1)
    Filters['Filter'] = np.nan
    Filters['Filter'] = Filters.loc[(Filters['RH_rural']) & (Filters['P_rural']) & (Filters['change']), 'Filter']
    Filters.loc[Filters['Filter']!=True, 'Filter'] = False
    
    #Filtering
    df_d[Filters['Filter']==False] = np.nan
    df_h[Filters['Filter'].resample('H').pad()[df_h.index]==False] = np.nan

    #Save file
    df_d.to_csv('Data/Amsterdam_2194_daily.csv')
    df_h.to_csv('Data/Amsterdam_2194_total.csv')
    