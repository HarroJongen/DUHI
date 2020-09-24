#Title: Period builder
#Date: 16-06-2020
#Author: Harro Jongen
#Function that creates all possible periods for DUHI

def BuilderPeriods(start, end):
    import pandas as pd
    import datetime
    
    dct = {}
    ls = ['Year', 'Summer', 'Heatwave']
    for i in ls: 
        dct[i] = []
    
    Heatwaves = pd.read_csv('Data/Metadata/HeatwavePeriods.csv')
    Heatwaves['Start'] = pd.to_datetime(Heatwaves['Start'], format='%m/%d/%Y')
    Heatwaves['End'] = pd.to_datetime(Heatwaves['End'], format='%m/%d/%Y')

    for year in range(start.year, end.year+1):
        dct['Year'] += [(datetime.datetime(year, 1, 1), datetime.datetime(year, 12, 31))]
        dct['Summer'] += [(datetime.datetime(year, 6, 1), datetime.datetime(year, 8, 31))]
        for wave in range(len(Heatwaves)):
            if Heatwaves.loc[wave, 'Start'].year == year:
                dct['Heatwave'] += [(Heatwaves.loc[wave, 'Start'], Heatwaves.loc[wave, 'End'])]
    
    return(dct)


