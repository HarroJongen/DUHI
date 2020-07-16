#Title: Summer in the City data format function
#Date: 30-06-2020
#Author: Harro Jongen
#Formats data of summer in the city project from multiple sheet excel file to csv

def SICFormatter(start, end, file):
    import pandas as pd
    import numpy as np
    
    #Read excel file and write to a dictionairy
    dfs = pd.read_excel(file, sheet_name = None)
    
    #Per station
    for item in dfs.items():
        station = item[1].copy()
        
        #Convert dates to datetime format
        station['date'] = pd.to_datetime(station['UTC'], format=' %d/%m/%Y %H:%M')
        
        #Rename columns
        station.rename({'T' : 'T_urban', 'u' : 'u_urban', 'h' : 'RH_urban'}, axis = 1, inplace = True)
        
        #Select period
        station = station[(station['date'] > start) &(station['date'] < end)]
        
        #Recalculate humidity to persentages
        station['RH_urban'] = station['RH_urban'] * 100
        
        #Replace NaN string with nan
        station = station.replace('    NaN',np.NaN)
        station = station.replace('    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN',np.NaN)
        
        #Write to csv file
        filepath = 'Data/Amsterdam_' + str(item[0]) + '_urban.csv'
        station.to_csv(filepath, columns = (['date', 'T_urban', 'u_urban', 'RH_urban']), index = False)
        