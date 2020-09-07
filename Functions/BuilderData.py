#Title: Dataset builder
#Date: 16-06-2020
#Author: Harro Jongen
#Function that extracts data from all datasets to build the datasets for analysis in DUHI

def BuilderData(start, end, data_periodtype, k_API = [0.85]):
    import datetime
    import pandas as pd
    import glob
    from geopy.geocoders import Nominatim
    import pickle

    #Import functions
    from Functions import FormatterSIC, FormatterMocca, FormatterWOW, FormatterRdam, UrbanRuralCombiner, FormatterUrbanRural, BuilderDaily, SatelliteToTimeseries, NormalizerUHI
    
    #%%###SETTINGS DATA###
    print('Loading settings')
    
    #Add 20 extra days foe API calculation
    start_analysis = start
    start = start - datetime.timedelta(days=20)
     
    
    #%%###FORMATTING DATA###
    
    #Format external data sources
    #Amsterdam data from Summer in the City
    print('Formatting data for Amsterdam')
    FormatterSIC.FormatterSIC(start, end, file = "Data/Cities/Amsterdam/AllStations")
    #WOW-NL data
    print('Formatting data form WOW-NL')
    FormatterWOW.FormatterWOW('Amsterdam', '916696001', start, end , file = "Data/Cities/Amsterdam/export_916696001.csv", rural=True)
    FormatterWOW.FormatterWOW('Rotterdam', '915096001', start, end , file = "Data/Cities/Rotterdam/Rural/export_915096001.csv", rural=True)
    #Rotterdam data
    print('Formatting data for Rotterdam')
    Files = glob.glob('Data/Cities/Rotterdam/*.csv')
    for file in Files:
        FormatterRdam.FormatterRdam(start, end, file)
    #Gent data
    print('Formatting data for Gent')
    FormatterMocca.FormatterMocca(start, end)
    
    
    #Combine datasets for locations
    #Create csv with filepaths for rural and urban station combinations
    print('Combining rural and urban locations')
    UrbanRuralCombiner.UrbanRuralCombiner()
    Combinations = pd.read_csv('Data/UrbanRuralCombinations.csv')
    #Create combined datasets
    for item in range(len(Combinations)):
        FormatterUrbanRural.FormatterUrbanRural(Combinations['City'][item], Combinations['UrbanFile'][item],\
                                                Combinations['RuralFile'][item])
            
    #Calculate metrics on daily basis
    print('Creating daily datasets')
    #Calculate normalization values
    NormalizerUHI.NormalizerUHI(start, end, file = 'Data/Cities/KNMI_20200901_hourly.txt')
    #Calculate metrics per location
    for file in Combinations['TotalFile']:
        BuilderDaily.BuilderDaily(file, k_API = k_API)
        
    #Add remote sensed soil moisture
    #Create agent to retrieve coordinates
    geolocator = Nominatim(user_agent="DUHI")
    #For every city
    for city in Combinations['City'].unique():
        print('Extracting satellite soil moisture data for ' + city)
        #Define location
        location = geolocator.geocode(city)
        #Build remote soil moisture time series
        SatelliteToTimeseries.SatelliteToTimeseries(city, (location.latitude, location.longitude), start, end)
        #Read dataframe with soil moisture
        sm_df = pd.read_csv('Data/' + city + '_rs_SoilMoisture.csv')
        #For all locations of one city
        Files = glob.glob('Data/'+ city +'*daily.csv')
        for file in Files:
            #Read file for location
            df = pd.read_csv(file)
            #Add soil moisture
            df['sm'] = sm_df['sm']
            df.to_csv(file, index=False)
    
    #%%###SAVING DATA###
    
    #Load metadata and combinations
    Metadata = pd.read_csv('Data/Metadata/Locations.csv', index_col=0)
    Combinations = pd.read_csv('Data/UrbanRuralCombinations.csv')
    
    #Intitialize dictionaries and dataframes to contain all data ready for analysis
    dct_hour = {}
    dct_day = {}
    
    #For every location
    for loc, item, city in zip(Combinations['Location'], range(len(Combinations)), Combinations['City']):
        #Build a dictionairy containg all locations as key and the hourly dataframe and format index
        dct_hour[loc] = pd.read_csv(Combinations['TotalFile'][item])
        dct_hour[loc]['date'] = pd.to_datetime(dct_hour[loc]['date'])
        dct_hour[loc] = dct_hour[loc].set_index('date')
        #Remove days used for API calculation
        dct_hour[loc] = dct_hour[loc].loc[(dct_hour[loc].index >= start_analysis) & (dct_hour[loc].index <= end)]
        #Add metadata
        dct_hour[loc]['City'] = city
        dct_hour[loc]['Location'] = loc
        dct_hour[loc]['LCZ'] = Metadata.loc[Metadata['Locations'] == loc, 'LCZ'].values[0]
        dct_hour[loc]['SVF'] = Metadata.loc[Metadata['Locations'] == loc, 'SVF'].values[0]
        dct_hour[loc]['Inhabitants100'] = Metadata.loc[Metadata['Locations'] == loc, 'Inhabitants100'].values[0]
        dct_hour[loc]['Popdens100'] = Metadata.loc[Metadata['Locations'] == loc, 'Popdens100'].values[0]
        dct_hour[loc]['Inhabitants500'] = Metadata.loc[Metadata['Locations'] == loc, 'Inhabitants500'].values[0]
        dct_hour[loc]['Popdens500'] = Metadata.loc[Metadata['Locations'] == loc, 'Popdens500'].values[0]
        dct_hour[loc]['Seepage'] = Metadata.loc[Metadata['Locations'] == loc, 'Seepage'].values[0]
        dct_hour[loc]['P_sealed'] = Metadata.loc[Metadata['Locations'] == loc, 'P_sealed'].values[0]
        dct_hour[loc]['prof'] = Metadata.loc[Metadata['Locations'] == loc, 'prof'].values[0]
    
        
        #Build a dictionairy containg all locations as key and the daily dataframe and format index
        dct_day[loc] = pd.read_csv(Combinations['DailyFile'][item])    
        dct_day[loc]['date'] = pd.to_datetime(dct_day[loc]['date'])
        dct_day[loc] = dct_day[loc].set_index('date')
        #Remove days used for API calculation
        dct_day[loc] = dct_day[loc].loc[(dct_day[loc].index >= start_analysis) & (dct_day[loc].index <= end)]
        #Add metadata
        dct_day[loc]['City'] = city
        dct_day[loc]['Location'] = loc
        dct_day[loc]['LCZ'] = Metadata.loc[Metadata['Locations'] == loc, 'LCZ'].values[0]
        dct_day[loc]['SVF'] = Metadata.loc[Metadata['Locations'] == loc, 'SVF'].values[0]
        dct_day[loc]['Inhabitants100'] = Metadata.loc[Metadata['Locations'] == loc, 'Inhabitants100'].values[0]
        dct_day[loc]['Popdens100'] = Metadata.loc[Metadata['Locations'] == loc, 'Popdens100'].values[0]
        dct_day[loc]['Inhabitants500'] = Metadata.loc[Metadata['Locations'] == loc, 'Inhabitants500'].values[0]
        dct_day[loc]['Popdens500'] = Metadata.loc[Metadata['Locations'] == loc, 'Popdens500'].values[0]
        dct_day[loc]['Seepage'] = Metadata.loc[Metadata['Locations'] == loc, 'Seepage'].values[0]
        dct_day[loc]['P_sealed'] = Metadata.loc[Metadata['Locations'] == loc, 'P_sealed'].values[0]
        dct_day[loc]['prof'] = Metadata.loc[Metadata['Locations'] == loc, 'prof'].values[0]
    
    #Initialize dataframes with first location
    df_h = dct_hour[list(dct_hour.keys())[0]]
    df_d = dct_day[list(dct_hour.keys())[0]]
    #For all other locations
    for loc in list(dct_hour.keys())[1:]:
        #Add location to dataframes
        df_h = df_h.append(dct_hour[loc])
        df_d = df_d.append(dct_day[loc])
    
    #Save both the dictionaries and the dataframes in pickles
    for file, name in zip([df_d, df_h],['df_d', 'df_h']):
        filename =  'Data/Preprocessed/' + name + '_' + data_periodtype + '_' + \
                str(start_analysis)[0:4] + str(start_analysis)[5:7] + str(start_analysis)[8:10] + \
                '_'     + str(end)[0:4] + str(end)[5:7] + str(end)[8:10]
        outfile = open(filename,'wb')
        pickle.dump(file,outfile)
        outfile.close()