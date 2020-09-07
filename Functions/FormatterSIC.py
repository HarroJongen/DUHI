#Title: Summer in the City data format function
#Date: 30-06-2020
#Author: Harro Jongen
#Formats data of summer in the city project from multiple sheet excel file to csv

def FormatterSIC(start, end, file, overwrite = True):
    import pandas as pd
    import numpy as np
    import os.path
    import pickle
    
    #Read pickle file as dictionairy
    infile = open(file,'rb')
    dfs = pickle.load(infile)
    infile.close()
    
    #Per station
    for item in dfs.items():
        
        #Define saving filename
        filepath = 'Data/Amsterdam_' + str(item[0]) + '_urban.csv'
        #Check whether file does not exists or whether it should be overwritten
        if overwrite or not os.path.isfile(filepath):
        
            df = item[1].copy()
            
            #Convert dates to datetime format
            df['date'] = pd.to_datetime(df['UTC'], format=' %d/%m/%Y %H:%M')
            
            #Rename columns
            df.rename({'T' : 'T_urban', 'u' : 'u_urban', 'h' : 'RH_urban'}, axis = 1, inplace = True)
            
            #Select period
            df = df[(df['date'] >= start) &(df['date'] <= end)]
            
            #Check if data is available in given period
            if len(df) == 0 :
                print('No data available between ' + str(start) + ' and ' + str(end) + ' for Amsterdam location ' + str(item[0]))
            else:
                #Recalculate humidity to persentages
                df['RH_urban'] = df['RH_urban'] * 100
                
                #Replace NaN string and -40 with nan
                df = df.replace(-40,np.NaN)
                df = df.replace('    NaN',np.NaN)
                df = df.replace('    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN    NaN',np.NaN)
                
                #Write to csv file
                df.to_csv(filepath, columns = (['date', 'T_urban', 'u_urban', 'RH_urban']), index = False)
                