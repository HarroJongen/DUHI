#Title: NormalizerUHI
#Date: 03-09-2020
#Author: Harro Jongen
#Normalizes UHI_max based on the diagnostic formula by Theeuwes et al. 2015

def NormalizerUHI(start, end, stations, file):
    import pandas as pd
    import numpy as np
    
    from Functions import DTRCalculator
    
    #Define dictionairy with station number and name
    dct = {209 : 'IJmond', 210 : 'Valkenburg', 215 : 'Voorschoten', 225 : 'IJmuiden',\
           235 : 'De Kooy', 240 : 'Schiphol', 242 : 'Vlieland', 248 : 'Wijdenes',\
           249 : 'Berkhout', 251 : 'Hoorn (Terschelling)', 257 : 'Wijk aan Zee',\
           258 : 'Houtribdijk', 260 : 'De Bilt', 265 : 'Soesterberg', 267 : 'Stavoren',\
           269 : 'Lelystad', 270 : 'Leeuwarden', 273 : 'Marknesse', 275 : 'Deelen',\
           277 : 'Lauwersoog', 278 : 'Heino', 279 : 'Hoogeveen', 280 : 'Eelde',\
           283 : 'Hupsel', 285 : 'Huibertgat', 286 : 'Nieuw Beerta', 290 : 'Twenthe',\
           308 : 'Cadzand', 310 : 'Vlissingen', 311 : 'Hoofdplaat', 312 : 'Oosterschelde',\
           313 : 'Vlakte v.d. Raan', 315 : 'Hansweert', 316 : 'Schaar', 319 : 'Westdorpe',\
           323 : 'Wilhelminadorp', 324 : 'Stavenisse', 330 : 'Hoek van Holland',\
           331 : 'Tholen', 340 : 'Woensdrecht', 343 : 'Rotterdam-Geulhaven', 344 : 'Rotterdam',\
           348 : 'Cabauw', 350 : 'Gilze-Rijen', 356 : 'Herwijnen', 370 : 'Eindhoven',\
           375 : 'Volkel', 377 : 'Ell', 380 : 'Maastricht', 391 : 'Arcen'}
    
    #Read file downloaded at http://projects.knmi.nl/klimatologie/uurgegevens/selectie.cgi
    df = pd.read_csv(file, header = 12 + stations, skiprows = [13 + stations], names = ['STN', 'YYYYMMDD', 'HH', 'FH', 'T', 'Q'])
    
    #Transform temperature to whole degrees
    df['T'] = df['T'] / 10
    
    #Transform wind to m/s
    df['FH'] = df['FH'] / 10
    
    #Transform global radiation to Km/s
    df['Q'] = df['Q'] /3600 * 10000 / (1.225 * 1.00467)
    
    
    for Loc in df['STN'].unique():
        #Select Amsterdam
        df_select = df.loc[df['STN'] == Loc].copy()
        
        #Add date as index
        df_select['HH'] -= 1
        df_select['date'] = df_select['YYYYMMDD'] * 100 + df_select['HH']
        df_select['date'] = pd.to_datetime(df_select['date'], format='%Y%m%d%H')
        df_select = df_select.set_index('date')
        #Select period of interest
        df_select = df_select[(df_select.index >= start) &(df_select.index <= end)]
        
        #Take range for DTR, mean for wind and sum for global radiation
        df_select_range = df_select.resample('D').apply(DTRCalculator.DTRCalculator)
        df_select_mean = df_select.resample('D').mean()
        df_select_sum = df_select.resample('D').sum()
        #Calculate normalization value
        df_select['Norm'] = ((df_select_range['T']**3*df_select_sum['Q'])/df_select_mean['FH'])**0.25
        #Drop all rows without data to get daily data set
        df_select = df_select.dropna()
        #All zeros na
        df_select = df_select.replace(0, np.nan)
        
        #Save dataframe
        if Loc == 240:
            df_select.to_csv('Data/UHI_Norms_Amsterdam.csv', columns = ['Norm'])        
        elif Loc == 278:
            df_select.to_csv('Data/UHI_Norms_Zwolle.csv', columns = ['Norm'])    
        elif Loc == 280:
            df_select.to_csv('Data/UHI_Norms_Groningen.csv', columns = ['Norm'])
        elif Loc == 290:
            df_select.to_csv('Data/UHI_Norms_Enschede.csv', columns = ['Norm'])
            df_select.to_csv('Data/UHI_Norms_Hengelo.csv', columns = ['Norm'])
            df_select.to_csv('Data/UHI_Norms_Oldenzaal.csv', columns = ['Norm'])
        else:
            df_select.to_csv('Data/UHI_Norms_' + dct[Loc] + '.csv', columns = ['Norm'])

    
