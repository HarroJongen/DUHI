#Title: Filtering weather out of UHI
#Date: 04-09-2020
#Author: Harro Jongen
#Filtering function to exclude non urban effects on UHI

def FilteringUHI(dataframe_day, dataframe_hour):
    import pandas as pd
    import numpy as np
    
   
    #Filtering rain events
    df_sum = dataframe_hour.resample('D').sum()
    Filter_rain = df_sum['P_rural']<0.3

    #Filtering sudden wind changes
    dataframe_hour['change'] =  dataframe_hour['u_rural'] - dataframe_hour['u_rural'].shift(1)
    df_max = dataframe_hour.resample('D').max()
    Filter_wind = df_max['change']<2
    dataframe_hour = dataframe_hour.drop(['change'], axis=1)    

    #Filtering fog
    df_mean = dataframe_hour.resample('D').mean()
    Filter_fog = df_mean['RH_rural']<80

    #Total filter
    Filters = pd.concat([Filter_fog, Filter_rain, Filter_wind], axis=1)
    Filters['Filter'] = np.nan
    Filters['Filter'] = Filters.loc[(Filters['RH_rural']) & (Filters['P_rural']) & (Filters['change'])]
    Filters.loc[Filters['Filter']!=True, 'Filter'] = False
    
    #Filtering
    dataframe_day.loc[Filters['Filter']==False, ['T_max_urban', 'P_urban', 'T_max_rural', 'UHI_max', 'Norm', 'DTR_urban', 'DTR_rural', 'UHI_int', 'API0.85_urban', 'API0.85_rural', 'sm']] = np.nan
    dataframe_hour.loc[Filters['Filter'].resample('H').pad()[dataframe_hour.index]==False, ['T_urban', 'u_urban', 'P_urban', 'RH_urban', 'T_rural', 'u_rural', 'P_rural', 'p_rural', 'RH_rural', 'UHI']] = np.nan

    #Save file
    return(dataframe_day, dataframe_hour)
    