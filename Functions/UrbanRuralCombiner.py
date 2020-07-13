#Title: UrbanRuralCombiner
#Date: 10-07-2020
#Author: Harro Jongen
#Builds a dataframe containing all filenames for the combination of rural and urban stations

def UrbanRuralCombiner():
    import glob
    import re
    import pandas as pd
    #Initialize empty dataframe for rural and urban station combinations
    Locations = pd.DataFrame(columns = ['City', 'UrbanFile', 'RuralFile'])
    #Read all filenames for rural and urban sites
    UrbanFiles = glob.glob('Data/*_urban.csv')
    RuralFiles = glob.glob('Data/*_rural.csv')
    
    #Create regular expression to scan filenames for city names
    regex_city = re.compile(r'Data\\([A-Za-z]+)_\w+.csv')
    #For every urban file
    for item in range(len(UrbanFiles)):
        UrbanFile = UrbanFiles[item]
        City = regex_city.findall(UrbanFiles[item])
        RuralFile = 'Data\\' + City[0] + '_rural.csv'
        Locations.loc[item] = [City[0]] + [UrbanFile] + [RuralFile]
    
    #Write dataframe to csv
    Locations.to_csv('Data\\UrbanRuralCombinations.csv', index = False)
