#Title: Veenkampen soil moisture formatter
#Date: 23-07-2020
#Author: Harro Jongen
#Formats the Veenkampen data into a single soil moisture timeseries

def FormatterVeenkampen(start, end):
    import pandas as pd
    import urllib.request
    import os
    
    #Create dataframe for timeseries including all dates
    df = pd.DataFrame(columns = ['date'])
    df['date'] = pd.date_range(start, end)
    df = df.set_index('date')
    
    #For every day
    for date in df.index:
        print('Extracting value for ' + str(date))
        #Define url and filepath
        url =   'https://met.wur.nl/veenkampen/data/' + str(date.year) + '/'\
                + str(date.strftime('%m'))  + '/hour_' + str(date.year)\
                + str(date.strftime('%m')) + str(date.strftime('%d')) + '.txt'
        filepath = 'Data/temp.txt'
        
        #Try to prevent a dead or non-existing link
        try:
            #Download one day of data
            urllib.request.urlretrieve(url, filepath)
        except:
            print('No file available for ' + str(date) + ' at given url')
        #Create dataframe of daily data
        if os.path.exists('Data/temp.txt'):
            df_day = pd.read_csv(filepath, header=None)
            df_day['date'] = pd.to_datetime(df_day[0])
            df_day = df_day.set_index('date')
            os.remove(filepath)
            
        #Calculate average of days
        df_day = df_day.groupby(df_day.index).mean()
        
        #Fill daily values into total dataframe
        df = df.combine_first(df_day)

        

        
    # Rename columns
    df.rename({72 : 'sm_grassA_065', 73 : 'sm_grassA_125', 74 : 'sm_grassA_250', 75 : 'sm_grassA_500',\
               76 : 'sm_grassB_065', 77 : 'sm_grassB_125', 78 : 'sm_grassB_250', 79 : 'sm_grassB_500',\
               80 : 'sm_soil_065'}, axis = 1, inplace = True)        
    
    #Save dataframe
    df.to_csv('Data/Veenkampen_SoilMoisture.csv', columns = (['sm_grassA_065', 'sm_grassA_125', 'sm_grassA_250',\
                                                              'sm_grassA_500', 'sm_grassB_065', 'sm_grassB_125',\
                                                                  'sm_grassB_250', 'sm_grassB_500', 'sm_soil_065']))

        
