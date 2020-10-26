#Title: Rotterdam data format function
#Date: 30-06-2020
#Author: Harro Jongen
#Formats data of Rotterdam to csv

def FormatterRdam(start, end, file, overwrite = True):
    import pandas as pd
    import datetime
    import os.path

    #Read WOW file
    df = pd.read_csv(file, names = ['DateTime', 'Name', 'Battery_{Min}', 'LithiumBattery_{Min}',\
                                    'PanelTemp_{Max}', 'CS215Error_{Tot}', 'Tair_{Avg}', 'RH_{Avg}',\
                                    'e_{Avg}', 'e_{s, Avg}', 'WindSonicError_{Tot}', 'WindSpd_{Max}',\
                                    'WindSpd_{Std}', 'WindSpd_{Avg}', 'WindDir_{Avg}', 'WindDir_{Std}',\
                                    'WindDirError_{Tot}', 'Rain_{Tot}', 'SR01Up_{Avg}', 'SR01Dn_{Avg}',\
                                    'IR01Up_{Avg}', 'IR01Dn_{Avg}', 'Tir01_{Avg}', 'Tglobe_{Avg}', 'Mir01',\
                                    'T_{sky}', 'T_{surface}', 'NetRs', 'NetRl', 'NetR' ,'TotUp', 'TotDn', 'Albedo'], na_values='NAN')

    #Define saving filename
    filepath = 'Data/Rotterdam_' + df['Name'][0] + '_urban.csv'
    #Check whether file does not exists or whether it should be overwritten
    if overwrite or not os.path.isfile(filepath):    
    
        #Convert dates to datetime format
        df['date'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S')
        
        #Rename columns
        df.rename({'Tair_{Avg}' : 'T_urban', 'WindSpd_{Avg}' : 'u_urban', 'RH_{Avg}' : 'RH_urban'}, axis = 1, inplace = True)
        
        #Select period
        df = df[(df['date'] >= start) &(df['date'] <= end)]
        df = df.reset_index()
        
        #Check if data is available in given period
        if len(df) == 0 :
            print('No data available between ' + str(start) + ' and ' + str(end) + ' for Rotterdam location ' + file[22:-4])
            if os.path.isfile(filepath):
                os.remove(filepath)
        else:
            #Calculate rainfall intensity
            dt = df['date'][1] - df['date'][0]
            df['P_urban'] = df['Rain_{Tot}']*(datetime.timedelta(1/24)/dt)
                
            #Write to csv file
            df.to_csv(filepath, columns = (['date', 'T_urban', 'u_urban', 'P_urban', 'RH_urban']), index = False)
                