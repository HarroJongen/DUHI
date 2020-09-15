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
    from Functions import FormatterSIC, FormatterMocca, FormatterWOW, FormatterRdam, UrbanRuralCombiner, FormatterUrbanRural, FormatterBeijum, BuilderDaily, SatelliteToTimeseries, NormalizerUHI
    
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
    FormatterWOW.FormatterWOW('Amsterdam', '916696001', start, end , file = "Data/Cities/Amsterdam/export_916696001.csv", location = None, rural=True)
    FormatterWOW.FormatterWOW('Rotterdam', '915096001', start, end , file = "Data/Cities/Rotterdam/Rural/export_915096001.csv", location = None, rural=True)
    
    FormatterWOW.FormatterWOW('Enschede', '917576001', start, end , file = "Data/Cities/Twente/Rural/export_917576001.csv", location = None, rural=True)
    FormatterWOW.FormatterWOW('Enschede', 'aacae4bb-0292-e911-80e7-0003ff59889d', start, end , file = "Data/Cities/Twente/export_aacae4bb-0292-e911-80e7-0003ff59889d.csv", location = 'ZuidOost', rural=False)
    FormatterWOW.FormatterWOW('Enschede', 'e12a4b13-783e-e911-867d-0003ff597ce7', start, end , file = "Data/Cities/Twente/export_e12a4b13-783e-e911-867d-0003ff597ce7.csv", location = 'Glanerburg', rural=False)
    
    FormatterWOW.FormatterWOW('Hengelo', '917576001', start, end , file = "Data/Cities/Twente/Rural/export_917576001.csv", location = None, rural=True)
    FormatterWOW.FormatterWOW('Hengelo', '922086001', start, end , file = "Data/Cities/Twente/export_922086001.csv", location = 'Verveld', rural=False)
    FormatterWOW.FormatterWOW('Hengelo', '1881744', start, end , file = "Data/Cities/Twente/export_1881744.csv", location = 'Losser', rural=False)

    FormatterWOW.FormatterWOW('Oldenzaal', '917576001', start, end , file = "Data/Cities/Twente/Rural/export_917576001.csv", location = None, rural=True)
    FormatterWOW.FormatterWOW('Oldenzaal', 'c625a11c-0473-e811-9ccb-0003ff59b2da', start, end , file = "Data/Cities/Twente/export_c625a11c-0473-e811-9ccb-0003ff59b2da.csv", location = '22', rural=False)

    FormatterWOW.FormatterWOW('Eindhoven', '917586001', start, end , file = "Data/Cities/Eindhoven/Rural/export_917586001.csv", location = None, rural=True)
    FormatterWOW.FormatterWOW('Eindhoven', '918216001', start, end , file = "Data/Cities/Eindhoven/export_918216001.csv", location = 'GroteBeek', rural=False)
    FormatterWOW.FormatterWOW('Eindhoven', '976856001', start, end , file = "Data/Cities/Eindhoven/export_976856001.csv", location = 'Sondervinck', rural=False)
    FormatterWOW.FormatterWOW('Eindhoven', 'e0ce6aa1-b5c1-e911-b083-0003ff59a71f', start, end , file = "Data/Cities/Eindhoven/export_e0ce6aa1-b5c1-e911-b083-0003ff59a71f.csv", location = 'Pegbroekenlaan', rural=False)
    FormatterWOW.FormatterWOW('Eindhoven', '670b6488-fc56-e611-9401-0003ff5987fd', start, end , file = "Data/Cities/Eindhoven/export_670b6488-fc56-e611-9401-0003ff5987fd.csv", location = 'Best', rural=False)
    FormatterWOW.FormatterWOW('Eindhoven', '96906327-4fb1-e811-a8ec-0003ff59b2da', start, end , file = "Data/Cities/Eindhoven/export_96906327-4fb1-e811-a8ec-0003ff59b2da.csv", location = 'Oirschot', rural=False)
    FormatterWOW.FormatterWOW('Eindhoven', 'b64f64d5-31c9-e611-9400-0003ff59aed0', start, end , file = "Data/Cities/Eindhoven/export_b64f64d5-31c9-e611-9400-0003ff59aed0.csv", location = 'Nuenen', rural=False)
    FormatterWOW.FormatterWOW('Eindhoven', '921496001', start, end , file = "Data/Cities/Eindhoven/export_921496001.csv", location = 'Son', rural=False)

    FormatterWOW.FormatterWOW('Groningen', '911216001', start, end , file = "Data/Cities/Groningen/Rural/export_911216001.csv", location = None, rural=True)
    FormatterWOW.FormatterWOW('Groningen', '1106d8ca-da22-e811-bbd5-0003ff5993c1', start, end , file = "Data/Cities/Groningen/export_1106d8ca-da22-e811-bbd5-0003ff5993c1.csv", location = 'Ulgersmaborg', rural=False)
    FormatterWOW.FormatterWOW('Groningen', 'f93cfaad-5b9e-e811-b96f-0003ff5993a0', start, end , file = "Data/Cities/Groningen/export_f93cfaad-5b9e-e811-b96f-0003ff5993a0.csv", location = 'Rozemarijnstraat', rural=False)
    FormatterWOW.FormatterWOW('Groningen', '92137096-2d22-e911-9462-0003ff59610a', start, end , file = "Data/Cities/Groningen/export_92137096-2d22-e911-9462-0003ff59610a.csv", location = 'Deheld', rural=False)
    FormatterWOW.FormatterWOW('Groningen', '4895f26e-0c64-e811-bd6d-0003ff59b2de', start, end , file = "Data/Cities/Groningen/export_4895f26e-0c64-e811-bd6d-0003ff59b2de.csv", location = 'Hereweg', rural=False)

    FormatterWOW.FormatterWOW('Maastricht', '917536001', start, end , file = "Data/Cities/Maastricht/Rural/export_917536001.csv", location = None, rural=True)
    FormatterWOW.FormatterWOW('Maastricht', '78095ddd-09cd-e611-9400-000d3ab1cf4b', start, end , file = "Data/Cities/Maastricht/export_78095ddd-09cd-e611-9400-000d3ab1cf4b.csv", location = 'Oost', rural=False)
    FormatterWOW.FormatterWOW('Maastricht', '9b33430b-fcc7-e911-b083-0003ff59a71f', start, end , file = "Data/Cities/Maastricht/export_9b33430b-fcc7-e911-b083-0003ff59a71f.csv", location = 'Gronsveld', rural=False)
    FormatterWOW.FormatterWOW('Maastricht', '4c65e349-e7ca-e911-b3b9-0003ff59a783', start, end , file = "Data/Cities/Maastricht/export_4c65e349-e7ca-e911-b3b9-0003ff59a783.csv", location = 'Daalhof', rural=False)
    FormatterWOW.FormatterWOW('Maastricht', '938466001', start, end , file = "Data/Cities/Maastricht/export_938466001.csv", location = 'Geleen', rural=False)

    FormatterWOW.FormatterWOW('Zwolle', '913976001', start, end , file = "Data/Cities/Zwolle/Rural/export_913976001.csv", location = None, rural=True)
    FormatterWOW.FormatterWOW('Zwolle', 'cb6673ad-fba7-e911-b083-0003ff59a71f', start, end , file = "Data/Cities/Zwolle/export_cb6673ad-fba7-e911-b083-0003ff59a71f.csv", location = 'Centrum', rural=True)
    FormatterWOW.FormatterWOW('Zwolle', '02b21464-89e3-e811-a140-0003ff5993a0', start, end , file = "Data/Cities/Zwolle/export_02b21464-89e3-e811-a140-0003ff5993a0.csv", location = 'Mussehage', rural=False)
    FormatterWOW.FormatterWOW('Zwolle', '7b1d5833-0c65-e811-bd6d-0003ff59b2de', start, end , file = "Data/Cities/Zwolle/export_7b1d5833-0c65-e811-bd6d-0003ff59b2de.csv", location = 'Seringenstraat', rural=False)
    FormatterWOW.FormatterWOW('Zwolle', '67f749dd-1845-e911-867d-0003ff5960dd', start, end , file = "Data/Cities/Zwolle/export_67f749dd-1845-e911-867d-0003ff5960dd.csv", location = 'Bosweg', rural=False)
    FormatterWOW.FormatterWOW('Zwolle', '90a6c1c2-89e3-e811-a140-0003ff5993a0', start, end , file = "Data/Cities/Zwolle/export_90a6c1c2-89e3-e811-a140-0003ff5993a0.csv", location = 'Labyrinthstraat', rural=False)
    FormatterWOW.FormatterWOW('Zwolle', '8d6449bf-17b2-e811-a8eb-0003ff596efb', start, end , file = "Data/Cities/Zwolle/export_8d6449bf-17b2-e811-a8eb-0003ff596efb.csv", location = 'Oase', rural=False)
    FormatterWOW.FormatterWOW('Zwolle', 'e86ae272-8ae3-e811-a140-0003ff5993a0', start, end , file = "Data/Cities/Zwolle/export_e86ae272-8ae3-e811-a140-0003ff5993a0.csv", location = 'Stadshoeve', rural=False)
    FormatterWOW.FormatterWOW('Zwolle', 'b89d8aaa-eaa7-e911-b083-0003ff59a71f', start, end , file = "Data/Cities/Zwolle/export_b89d8aaa-eaa7-e911-b083-0003ff59a71f.csv", location = 'Stadshagen', rural=False)
    FormatterWOW.FormatterWOW('Zwolle', '8a5f044a-8ae3-e811-a140-0003ff598dc6', start, end , file = "Data/Cities/Zwolle/export_8a5f044a-8ae3-e811-a140-0003ff598dc6.csv", location = 'Sterrenkroos', rural=False)
    FormatterWOW.FormatterWOW('Zwolle', 'e1400101-89e3-e811-a140-0003ff5993a0', start, end , file = "Data/Cities/Zwolle/export_e1400101-89e3-e811-a140-0003ff5993a0.csv", location = 'Gorterstraat', rural=False)


    #Rotterdam data
    print('Formatting data for Rotterdam')
    Files = glob.glob('Data/Cities/Rotterdam/*.csv')
    for file in Files:
        FormatterRdam.FormatterRdam(start, end, file)
    #Gent data
    print('Formatting data for Gent')
    FormatterMocca.FormatterMocca(start, end)
    #Beijum data
    FormatterBeijum.FormatterBeijum(start, end, 'Data/Cities/Hobby-meteo-binntemp/WX_Beijum.csv')
    
    
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
    NormalizerUHI.NormalizerUHI(start, end, stations = 7, file = 'Data/Cities/KNMI_20200913_hourly.txt')
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
        dct_day[loc]['P_green'] = Metadata.loc[Metadata['Locations'] == loc, 'P_green'].values[0]
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