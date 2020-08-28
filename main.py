#Title: Main file for DUHI
#Date: 16-06-2020
#Author: Harro Jongen
#Excecutes the complete proces to analyze the connections of drought and UHI for NL and BE


#%%###IMPORTING###

#Import packages
print('Importing packages and functions')
import datetime
import pandas as pd
import glob
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import re
import pickle


#Import functions
from Functions import SICFormatter, MoccaFormatter, WOWFormatter, RdamFormatter, UrbanRuralCombiner, UrbanRuralFormatter, DailyBuilder, SatelliteToTimeseries

#%%###SETTINGS DATA###
print('Loading settings')

#Define period of interest
start = datetime.datetime(2019, 6, 1)
end = datetime.datetime(2019, 8, 1) #end date should be one day after the last day of interest
#Add 20 extra days foe API calculation
start_analysis = start
start = start - datetime.timedelta(days=20)

#Give a name to the analysis, starting with Heatwave (periods can be found in the data folder), Yearly or Summer followed by the year
name = 'Summer_2018'
#Analyze name for properties
regex = re.compile(r'([AaA-Za-z]+)_([0-9]+)')
analysis = regex.search(name).group(1)
time = regex.search(name).group(2)


#%%###FORMATTING DATA###

#Format external data sources
#Amsterdam data from Summer in the City
print('Formatting data for Amsterdam')
SICFormatter.SICFormatter(start, end, file = "Data/Amsterdam/5G0D2194(5G0D2194)-1554817879612.xlsx")
#WOW-NL data
print('Formatting data form WOW-NL')
WOWFormatter.WOWFormatter('Amsterdam', '916696001', start, end , file = "Data/Amsterdam/export_916696001.csv", rural=True)
WOWFormatter.WOWFormatter('Rotterdam', '915096001', start, end , file = "Data/Rotterdam/Rural/export_915096001.csv", rural=True)
#Rotterdam data
print('Formatting data for Rotterdam')
Files = glob.glob('Data/Rotterdam/*.csv')
for file in Files:
    RdamFormatter.RdamFormatter(start, end, file)
#Gent data
print('Formatting data for Gent')
MoccaFormatter.MoccaFormatter(start, end)


#Combine datasets for locations
#Create csv with filepaths for rural and urban station combinations
print('Combining rural and urban locations')
UrbanRuralCombiner.UrbanRuralCombiner()
Combinations = pd.read_csv('Data/UrbanRuralCombinations.csv')
#Create combined datasets
for item in range(len(Combinations)):
    UrbanRuralFormatter.UrbanRuralFormatter(Combinations['City'][item], Combinations['UrbanFile'][item],\
                                            Combinations['RuralFile'][item])
        
#Calculate metrics on daily basis
print('Creating daily datasets')
for file in Combinations['TotalFile']:
    DailyBuilder.DailyBuilder(file, k_API = [0.85])
    
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
for loc, item in zip(Combinations['Location'], range(len(Combinations))):
    #Build a dictionairy containg all locations as key and the hourly dataframe and format index
    dct_hour[loc] = pd.read_csv(Combinations['TotalFile'][item])
    dct_hour[loc]['date'] = pd.to_datetime(dct_hour[loc]['date'])
    dct_hour[loc] = dct_hour[loc].set_index('date')
    #Remove days used for API calculation
    dct_hour[loc] = dct_hour[loc].loc[(dct_hour[loc].index >= start_analysis) & (dct_hour[loc].index <= end)]
    #Add metadata
    dct_hour[loc]['LCZ'] = Metadata.loc[Metadata['Locations'] == loc, 'LCZ'].values[0]
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
    dct_day[loc]['LCZ'] = Metadata.loc[Metadata['Locations'] == loc, 'LCZ'].values[0]
    dct_day[loc]['Inhabitants100'] = Metadata.loc[Metadata['Locations'] == loc, 'Inhabitants100'].values[0]
    dct_day[loc]['Popdens100'] = Metadata.loc[Metadata['Locations'] == loc, 'Popdens100'].values[0]
    dct_day[loc]['Inhabitants500'] = Metadata.loc[Metadata['Locations'] == loc, 'Inhabitants500'].values[0]
    dct_day[loc]['Popdens500'] = Metadata.loc[Metadata['Locations'] == loc, 'Popdens500'].values[0]
    dct_day[loc]['Seepage'] = Metadata.loc[Metadata['Locations'] == loc, 'Seepage'].values[0]
    dct_day[loc]['P_sealed'] = Metadata.loc[Metadata['Locations'] == loc, 'P_sealed'].values[0]
    dct_day[loc]['prof'] = Metadata.loc[Metadata['Locations'] == loc, 'prof'].values[0]

#Initialize dataframes with first location
df_hour = dct_hour[list(dct_hour.keys())[0]]
df_day = dct_day[list(dct_hour.keys())[0]]
#For all other locations
for loc in list(dct_hour.keys())[1:]:
    #Add location to dataframes
    df_hour = df_hour.append(dct_hour[loc])
    df_day = df_day.append(dct_day[loc])

#Save both the dictionaries and the dataframes in pickles
for file, name in zip([df_day, df_hour, dct_day, dct_hour],['df_day', 'df_hour', 'dct_day', 'dct_hour']):
    filename =  'Data/Preprocessed/' + name + '_' + analysis + '_' + \
            str(start_analysis)[0:4] + str(start_analysis)[5:7] + str(start_analysis)[8:10] + \
            '_'     + str(end)[0:4] + str(end)[5:7] + str(end)[8:10]
    outfile = open(filename,'wb')
    pickle.dump(file,outfile)
    outfile.close()

#%%###SETTINGS ANALYSIS###

#%%###LOADING DATA###

#List all names of pickles available
Pickles = glob.glob('Data/Preprocessed/*')
infile = open(filename,'rb')
new_dict = pickle.load(infile)
infile.close()


#%%###ANALYSIS###



#For every location
for loc in dct_day.keys():
    df = dct_day[loc]
    
    
#%%###VISUALIZATION###

#Visualization total

df_day.boxplot(column='UHI_max', by='LCZ')
df_day.boxplot(column='UHI_int', by='LCZ')
df_day.boxplot(column='T_max_urban', by='LCZ')
df_day.boxplot(column='DTR_urban', by='LCZ')

df_day.boxplot(column='UHI_max', by='Seepage')
df_day.boxplot(column='UHI_int', by='Seepage')
df_day.boxplot(column='T_max_urban', by='Seepage')
df_day.boxplot(column='DTR_urban', by='Seepage')

df_day['sm_cor'] = df_day['sm']-df_day['P_sealed']/100*df_day['sm']
fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(df_day['API0.85_rural'], df_day['DTR_urban'], c=df_day.index)
fig.show()

fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(df_day['UHI_max'], df_day['API0.85_rural'], c = df_day['Popdens500'])
fig.show()

#Visualization per location

plot_count = 1
fig_T = plt.figure()

#For every location
for loc in dct_hour.keys():
    df = dct_hour[loc]
    ax = fig_T.add_subplot(3,3,plot_count)
    ax.plot(df['T_urban'], color='red')
    ax.plot(df['T_rural'], color='green')
    ax.set_title(loc + ', LCZ = ' + str(df['LCZ'][0]))
    ax.set_ylabel('Temperature')
    ax.figure.autofmt_xdate()
    
    
    
    
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    if plot_count == 9:
        fig_T.tight_layout()
        plot_count = 1
        fig_T = plt.figure()
    else:
        plot_count += 1
    
fig_T.tight_layout()
    