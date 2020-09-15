#Title: WOW-NL data format function
#Date: 30-06-2020
#Author: Harro Jongen
#Formats data of WOW-nl to csv

def FormatterWOW(city, number, start, end, file, location, rural = True, overwrite = True):
    import pandas as pd
    import numpy as np
    import os.path
    import datetime
    
    #Set right suffix for location and define  saving filename
    if rural == True:
        Loc = 'rural'
        filepath = 'Data/' + city + '_' + Loc + '.csv'
    else:
        Loc = 'urban'
        filepath = 'Data/' + city + '_' + location + '_' + Loc + '.csv'

    #Check whether file does not exists or whether it should be overwritten
    if overwrite or not os.path.isfile(filepath):
        
        #Read WOW file
        df = pd.read_csv(file, delimiter = ';')
                
        #Convert dates to datetime format
        df['date'] = pd.to_datetime(df['datum'], format='%Y-%m-%dT%H:%M:%S')
        #Convert time to UTC
        df['date'] = df['date'] - datetime.timedelta(hours=2)
        
        #Rename columns
        df.rename({'temperatuur (C) ['+ number +']' : 'T_' + Loc, 'neerslagintensiteit (mm/uur) ['+ number +']' : 'P_' + Loc, 'windsnelheid (m/s) ['+ number +']' : 'u_' + Loc, 'relatieve vochtigheid  (%) ['+ number +']' : 'RH_' + Loc, 'luchtdruk (hPa) ['+ number +']' : 'p_' + Loc}, axis = 1, inplace = True)
        
        #Select period
        df = df[(df['date'] >= start) &(df['date'] <= end)]
        
        #Check if data is available in given period
        if len(df) == 0 :
            print('No data available between ' + str(start) + ' and ' + str(end) + ' for ' + Loc + ' WOW location of ' + city)
            if os.path.isfile(filepath):
                os.remove(filepath)
        else:
            #Replace - with NA
            df = df.replace('-',np.NaN)
            
            #Write to csv file
            df.to_csv(filepath, columns = (['date', 'T_' + Loc, 'u_' + Loc, 'P_' + Loc, 'p_' + Loc, 'RH_' + Loc]), index = False)
                