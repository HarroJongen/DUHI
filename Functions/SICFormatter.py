#Title: Summer in the City data format function
#Date: 30-06-2020
#Author: Harro Jongen
#Formats data of summer in the city project from multiple sheet excel file to csv

def SICFormatter(start, end, file = "Data/5G0D2194(5G0D2194)-1554817879612.xlsx"):
    import pandas as pd
    
    #Read excel file and write to a dictionairy
    dfs = pd.read_excel(file, sheet_name = None)
    
    #Per station
    for item in dfs.items():
        station = item[1].copy()
        
        #Convert dates to datetime format
        station['date'] = pd.to_datetime(station['UTC'], format=' %d/%m/%Y %H:%M')
        
        #Recalculate humidity to persentages
        station['h'] = station['h'] * 100
        
        #Rename columns
        station.rename({'T' : 'T_urban (C)', 'u' : 'u_urban (m/s)', 'h' : 'RH_urban (%)'}, axis = 1, inplace = True)
        
        #Select period
        station = station[(station['date'] > start) &(station['date'] < end)]
        
        #Write to csv file
        filepath = 'Data/Amsterdam_' + str(item[0]) + '_urban.csv'
        station.to_csv(filepath, columns = (['date', 'T_urban (C)', 'u_urban (m/s)', 'RH_urban (%)']), index = False)
        