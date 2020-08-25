#Title: Main file for DUHI
#Date: 16-06-2020
#Author: Harro Jongen
#Excecutes the complete proces to analyze the connections of drought and UHI for NL and BE

###IMPORTING###

#Import packages
print('Importing packages and functions')
import datetime
import pandas as pd
import glob
from geopy.geocoders import Nominatim
import matplotlib
import matplotlib.pyplot as plt


#Import functions
from Functions import SICFormatter, MoccaFormatter, WOWFormatter, RdamFormatter, UrbanRuralCombiner, UrbanRuralFormatter, DailyBuilder, SatelliteToTimeseries

###SETTINGS###
print('Loading settings')

#Define period of interest
start = datetime.datetime(2018, 7, 15)
end = datetime.datetime(2018 , 7, 27)
#Give a name to the analysis, starting with Heatwave (periods can be found in the data folder), Yearly or Summer followed by the year
analysis = 'Heatwave_2018'

###FORMATTING DATA###

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
        df.to_csv(file)
        
#Load metadata
Metadata = pd.read_csv('Data/Metadata/Locations.csv', index_col=0)

#Intitialize dictionaries to contain all data
dct_hour = {}
dct_day = {}
#For every location
for loc, item in zip(Combinations['Location'], range(len(Combinations))):
    #Build a dictionairy containg all locations as key and the hourly dataframe and format index
    dct_hour[loc] = pd.read_csv(Combinations['TotalFile'][item])
    dct_hour[loc]['date'] = pd.to_datetime(dct_hour[loc]['date'])
    dct_hour[loc] = dct_hour[loc].set_index('date')
    #Build a dictionairy containg all locations as key and the daily dataframe and format index
    dct_day[loc] = pd.read_csv(Combinations['DailyFile'][item])    
    dct_day[loc]['date'] = pd.to_datetime(dct_day[loc]['date'])
    dct_day[loc] = dct_day[loc].set_index('date')

  
    
###ANALYSIS###



###VISUALIZATION###

plot_count = 1
fig = plt.figure()

#For every location
for loc in dct_hour.keys():
    df = dct_hour[loc]
    ax = fig.add_subplot(3,3,plot_count)
    ax.plot(df['T_urban'], color='red')
    ax.plot(df['T_rural'], color='green')
    ax.set_title(loc)
    ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())

    ax.grid(b=True, which='major', color='w', linewidth=1.5)
    ax.grid(b=True, which='minor', color='w', linewidth=0.75)

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    if plot_count == 9:
        fig.tight_layout()
        plot_count = 1
        fig = plt.figure()
    else:
        plot_count += 1
    
fig.tight_layout()
    