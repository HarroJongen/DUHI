#Title: WOW-NL data format function
#Date: 30-06-2020
#Author: Harro Jongen
#Formats data of WOW-nl to csv

def WOWFormatter(city, station, start, end, file, rural = True, overwrite = True):
    import pandas as pd
    import numpy as np
    import os.path
    import datetime
    
    #Set right suffix for location and define  saving filename
    if rural:
        Loc = 'rural'
        filepath = 'Data/' + city + '_' + Loc + '.csv'
    else:
        Loc = 'urban'
        filepath = 'Data/' + city + '_' + station + '_' + Loc + '.csv'

    #Check whether file does not exists or whether it should be overwritten
    if overwrite or not os.path.isfile(filepath):
        
        #Read WOW file
        df = pd.read_csv(file, delimiter = ';')
                
        #Convert dates to datetime format
        df['date'] = pd.to_datetime(df['datum'], format='%Y-%m-%dT%H:%M:%S')
        #Convert time to UTC
        df['date'] = df['date'] - datetime.timedelta(hours=2)
        
        #Rename columns
        df.rename({'temperatuur (C) ['+ station +']' : 'T_' + Loc, 'neerslagintensiteit (mm/uur) ['+ station +']' : 'P_' + Loc, 'windsnelheid (m/s) ['+ station +']' : 'u_' + Loc, 'relatieve vochtigheid  (%) ['+ station +']' : 'RH_' + Loc, 'luchtdruk (hPa) ['+ station +']' : 'p_' + Loc}, axis = 1, inplace = True)
        
        #Select period
        df = df[(df['date'] > start) &(df['date'] < end)]
        
        #Check if data is available in given period
        if len(df) == 0 :
            print('No data available between ' + str(start) + ' and ' + str(end) + ' for ' + Loc + ' WOW location of ' + city)
            if os.path.isfile(filepath):
                os.remove(filepath)
        else:
            #Replace - with NA
            df = df.replace('-',np.NaN)
            
            #Write to csv file
            df.to_csv(filepath, columns = (['date', 'T_rural', 'u_rural', 'P_rural', 'p_rural', 'RH_rural']), index = False)
                