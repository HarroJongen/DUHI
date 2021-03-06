#Title: UrbanRuralCombiner
#Date: 10-07-2020
#Author: Harro Jongen
#Builds a dataframe containing all filenames for the combination of rural and urban stations

def UrbanRuralCombiner():
    import glob
    import re
    import pandas as pd
    import os.path
    
    #Initialize empty dataframe for rural and urban station combinations
    Locations = pd.DataFrame(columns = ['City', 'Location', 'UrbanFile', 'RuralFile', 'TotalFile', 'DailyFile'])
    #Read all filenames for rural and urban sites
    UrbanFiles = glob.glob('Data/*_urban.csv')
    
    #Create regular expression to scan filenames for city names
    regex_city = re.compile(r'Data\\([A-Za-z]+)_\w+.csv')
    regex_loc = re.compile('Data\\\\\w+?_([_A-Za-z0-9]+)_\w+?.csv')
    
    #For every urban file
    for item in range(len(UrbanFiles)):
        UrbanFile = UrbanFiles[item]
        City = regex_city.findall(UrbanFiles[item])
        Location = regex_loc.findall(UrbanFiles[item])
        RuralFile = 'Data\\' + City[0] + '_rural.csv'
        TotalFile = UrbanFiles[item][0:-9] + 'total.csv'
        DailyFile = UrbanFiles[item][0:-9] + 'daily.csv'
        
        #Check whether rural file is available
        if os.path.isfile(RuralFile):
            #Add combination to the dataframe
            Locations.loc[item] = [City[0]] + [Location[0]] + [UrbanFile] + [RuralFile] + [TotalFile] + [DailyFile]
    
    #Write dataframe to csv
    Locations.to_csv('Data\\UrbanRuralCombinations.csv', index = False)
