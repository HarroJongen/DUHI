#Title: NormalizerUHI
#Date: 03-09-2020
#Author: Harro Jongen
#Normalizes UHI_max based on the diagnostic formula by Theeuwes et al. 2015

def NormalizerUHI(start, end, file):
    import pandas as pd
    
    from Functions import DTRCalculator
    
    df = pd.read_csv(file, header = 14)
    
    #Transform temperature to whole degrees
    df['T'] = df['T'] / 10
    
    #Transform wind to m/s
    df['FH'] = df['FH'] / 10
    
    #Transform global radiation to Km/s
    df['Q'] = df['Q'] /3600 * 10000 / (1.225 * 1.00467)
    
    #Select Amsterdam
    df_Adam = df.loc[df['STN'] == 240].copy()
    
    #Add date as index
    df_Adam['HH'] -= 1
    df_Adam['date'] = df_Adam['YYYYMMDD'] * 100 + df_Adam['HH']
    df_Adam['date'] = pd.to_datetime(df_Adam['date'], format='%Y%m%d%H')
    df_Adam = df_Adam.set_index('date')
    #Select period of interest
    df_Adam = df_Adam[(df_Adam.index >= start) &(df_Adam.index <= end)]
    
    #Take range for DTR, mean for wind and sum for global radiation
    df_Adam_range = df_Adam.resample('D').apply(DTRCalculator.DTRCalculator)
    df_Adam_mean = df_Adam.resample('D').mean()
    df_Adam_sum = df_Adam.resample('D').sum()
    #Calculate normalization value
    df_Adam['Norm'] = ((df_Adam_range['T']**3*df_Adam_sum['Q'])/df_Adam_mean['FH'])**0.25
    #Drop all rows without data to get daily data set
    df_Adam = df_Adam.dropna()
    
    #Save dataframe
    df_Adam.to_csv('Data/UHI_Norms_Amsterdam.csv', columns = ['Norm'])
    
    #Select Rotterdam
    df_Rdam = df.loc[df['STN'] == 344].copy()
    
    #Add date as index
    df_Rdam['HH'] -= 1
    df_Rdam['date'] = df_Rdam['YYYYMMDD'] * 100 + df_Rdam['HH']
    df_Rdam['date'] = pd.to_datetime(df_Rdam['date'], format='%Y%m%d%H')
    df_Rdam = df_Rdam.set_index('date')
    #Select period of interest
    df_Rdam = df_Rdam[(df_Rdam.index >= start) &(df_Rdam.index <= end)]
    
    #Take range for DTR, mean for wind and sum for global radiation
    df_Rdam_range = df_Rdam.resample('D').apply(DTRCalculator.DTRCalculator)
    df_Rdam_mean = df_Rdam.resample('D').mean()
    df_Rdam_sum = df_Rdam.resample('D').sum()
    #Calculate normalization value
    df_Rdam['Norm'] = ((df_Rdam_range['T']**3*df_Rdam_sum['Q'])/df_Rdam_mean['FH'])**0.25    
    #Drop all rows without data to get daily data set
    df_Rdam = df_Rdam.dropna()
    
    #Save dataframe
    df_Rdam.to_csv('Data/UHI_Norms_Rotterdam.csv', columns = ['Norm'])
    
