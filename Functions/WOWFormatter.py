#Title: WOW-NL data format function
#Date: 30-06-2020
#Author: Harro Jongen
#Formats data of WOW-nl to csv

def WOWFormatter(city, start, end, file, rural = True):
    import pandas as pd
    import numpy as np
    
    #Read WOW file
    df = pd.read_csv(file, delimiter = ';')
    
    #Set right suffix for location
    if rural:
        Loc = 'rural'
    else:
        Loc = 'urban'
    
    #Convert dates to datetime format
    df['date'] = pd.to_datetime(df['datum'], format='%Y-%m-%dT%H:%M:%S')
    
    #Rename columns
    df.rename({'temperatuur (C) [916696001]' : 'T_' + Loc, 'neerslagintensiteit (mm/uur) [916696001]' : 'P_' + Loc, 'windsnelheid (m/s) [916696001]' : 'u_' + Loc, 'relatieve vochtigheid  (%) [916696001]' : 'RH_' + Loc, 'luchtdruk (hPa) [916696001]' : 'p_' + Loc}, axis = 1, inplace = True)
    
    #Select period
    df = df[(df['date'] > start) &(df['date'] < end)]
    
    #Replace - with NA
    df = df.replace('-',np.NaN)
    
    #Write to csv file
    filepath = 'Data/' + city + '_' + Loc + '.csv'
    df.to_csv(filepath, columns = (['date', 'T_rural', 'u_rural', 'P_rural', 'p_rural', 'RH_rural']), index = False)
        