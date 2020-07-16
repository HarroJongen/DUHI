#Title: Main file for DUHI
#Date: 16-06-2020
#Author: Harro Jongen
#Excecutes the complete proces to analyze the connections of drought and UHI for NL and BE

###IMPORTING###

#Import packages
import datetime
import pandas as pd
import glob

#Import functions
from Functions import SICFormatter, WOWFormatter, RdamFormatter, UrbanRuralCombiner, UrbanRuralFormatter, DailyBuilder

#Define period of interest
start = datetime.datetime(2017, 1, 1)
end = datetime.datetime(2018 , 12, 31)

###FORMATTING DATA###

#Select period and format Amsterdata from Summer in the City to project's format
SICFormatter.SICFormatter(start, end, file = "Data/5G0D2194(5G0D2194)-1554817879612.xlsx")

#Format WOW-NL data
WOWFormatter.WOWFormatter('Amsterdam', start, end , file = "Data/Amsterdam/export_916696001.csv")
    
#Format Rotterdam data
Files = glob.glob('Data/Rotterdam/*.csv')
for item in Files:
    RdamFormatter.RdamFormatter(start, end, item)
 
#Create csv with rural and urban station combinations
UrbanRuralCombiner.UrbanRuralCombiner()

#Create combined datasets
Combinations = pd.read_csv('Data/UrbanRuralCombinations.csv')
for item in range(len(Combinations)):
    UrbanRuralFormatter.UrbanRuralFormatter(Combinations['City'][item], Combinations['UrbanFile'][item],\
                                            Combinations['RuralFile'][item])

#Calculate matrics on daily basis
for file in Combinations['TotalFile']:
    DailyBuilder.DailyBuilder(file, k_API = 0.85)

###ANALYSIS###





###VISUALIZATION###