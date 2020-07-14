#Title: WOW-NL data format function
#Date: 30-06-2020
#Author: Harro Jongen
#Formats data of WOW-nl to csv

def WOWFormatter(city, start, end, file = "Data/export_916696001.csv"):
    import pandas as pd
    import numpy as np
    
    #Read WOW file
    df = pd.read_csv(file, delimiter = ';')
    
    
    #Convert dates to datetime format ####FORMAT WRONG#####
    df['date'] = pd.to_datetime(df['datum'], format='%Y-%m-%dT%H:%M:%S')
    
    #Rename columns
    df.rename({'temperatuur (C) [916696001]' : 'T_rural', 'neerslagintensiteit (mm/uur) [916696001]' : 'P_rural', 'windsnelheid (m/s) [916696001]' : 'u_rural', 'relatieve vochtigheid  (%) [916696001]' : 'RH_rural', 'luchtdruk (hPa) [916696001]' : 'p_rural'}, axis = 1, inplace = True)
    
    #Select period
    df = df[(df['date'] > start) &(df['date'] < end)]
    
    #Replace - with NA
    df = df.replace('-',np.NaN)
    
    #Write to csv file
    filepath = 'Data/' + city + '_rural.csv'
    df.to_csv(filepath, columns = (['date', 'T_rural', 'u_rural', 'P_rural', 'p_rural', 'RH_rural']), index = False)
        