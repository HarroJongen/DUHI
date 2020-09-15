#Title: Beijum data format function
#Date: 14-09-2020
#Author: Harro Jongen
#Formats data of Beijum amateur to csv

def FormatterBeijum(start, end, file, overwrite = True):
    import pandas as pd
    import numpy as np
    import os.path
    
    #Define saving filename
    filepath = 'Data/Groningen_Beijum_urban.csv'

    #Check whether file does not exists or whether it should be overwritten
    if overwrite or not os.path.isfile(filepath):
        
        #Read WOW file
        df = pd.read_csv(file, delimiter = '\t', header = 2, names = ['Date', 'Time', 'Temp_out', 'Temp_hi', 'Temp_lo', 'Hum_out', 'DewPt', 'WindSpeed', 'WindDir', 'WindRun', 'WindSpeed_hi', 'WindChill', 'HeatIndex', 'THWIndex', 'AirPressure', 'Rain', 'Heat', 'Cool', 'Temp_in', 'Hum_in', 'Dew_in', 'Heat_in', 'Arc'])
                
        #Convert dates to datetime format
        df['date'] = pd.to_datetime(df['Date']) + pd.to_timedelta(df['Time'] + ':00')
        
        #Rename columns
        df.rename({'Temp_out' : 'T_urban', 'Rain' : 'P_urban', 'WindSpeed' : 'u_urban', 'Hum_out' : 'RH_urban', 'AirPressure' : 'p_urban'}, axis = 1, inplace = True)
        
        #Select period
        df = df[(df['date'] >= start) &(df['date'] <= end)]
        
        #Check if data is available in given period
        if len(df) == 0 :
            print('No data available between ' + str(start) + ' and ' + str(end) + ' for Beijum, Groningen')
            if os.path.isfile(filepath):
                os.remove(filepath)
        else:
            #Replace - with NA
            df = df.replace('---',np.NaN)
            df['P_urban'] = np.NaN
            
            #Write to csv file
            df.to_csv(filepath, columns = (['date', 'T_urban', 'u_urban', 'P_urban', 'p_urban', 'RH_urban']), index = False)
                