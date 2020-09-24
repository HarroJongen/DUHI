#Title: Main file for DUHI
#Date: 16-06-2020
#Author: Harro Jongen
#Excecutes the complete proces to analyze the connections of drought and UHI for NL and BE


#%%###IMPORTING###

#Import packages
print('Importing packages and functions')
import datetime
import glob
import matplotlib.pyplot as plt
import re
import pickle
import numpy as np
import pandas as pd


#Import functions
from Functions import BuilderData, Visualization, BuilderPeriods, FilteringUHI

 #%%###FORMATTING DATA###

#Define k_API
k_API = [0.85 ]

#Define period
start = datetime.datetime(2017, 1, 1)
end = datetime.datetime(2019, 12, 31)

#All data
BuilderData.BuilderData(start = start, end = end, k_API = k_API)


#%%###SETTINGS ANALYSIS###

#Choose the dataset for analysis, options are:
    #Heatwave (Selects all heatwaves available)
    #Heatwave_2018 (Selects all heatwaves available from the specified year)
    #Summer (Selects all summers available)
    #Summer_2018 (Selects the summer from the specified year)
    #Year (Selects all years available)
    #Year_2018 (Selects the specified year)
#Optional suffixes:
    #_Subset (Followed by Heatwave, Summer or Year, adds extra dataframes as a subset for comparison)
    
analysis_name = 'Summer'
regex = re.compile(r'([A-Za-z]+)_?([0-9]*)_?S?u?b?s?e?t?_?([A-Za-z]*)_?([0-9]*)')
analysis_periodtype = regex.search(analysis_name).group(1)
analysis_year = regex.search(analysis_name).group(2)
subset_periodtype = regex.search(analysis_name).group(3)

#Select filter
Filter = False

#%%###LOADING DATA###

#List all names of pickles available
Pickles = glob.glob('Data/Preprocessed/*')

#Create empty dataframe for the dataset
data = {}

#Define regex item to find characteristics of saved data
regex = re.compile(r'Data/Preprocessed\\df_([dh]+)_[0-9]+_[0-9]+')

#For all preprocessed files
for Pickle in Pickles:
    #Open the pickle file
    infile = open(Pickle,'rb')
    #Define characteristics of the pickle file
    res = regex.search(Pickle).group(1)
    data['df_' + res] = pickle.load(infile)
    infile.close()

#Select years for analysis
if len(analysis_year) == 0:
    Years = range(start.year, end.year+1)
else:
    Years = [int(analysis_year)]

#Build dictionairy of all potential periods
dct_periods = BuilderPeriods.BuilderPeriods(start, end)

#For every possible time range of the selected periodtype
for i in range(len(dct_periods[analysis_periodtype])):
    #For every year in analysis
        for year in Years:
            #Check if the period falls within the analysis
            if dct_periods[analysis_periodtype][i][0].year == year:
                #Save the period in the dataframe
                if 'df_d' not in locals():
                    df_d = data['df_d'][(data['df_d'].index >= dct_periods[analysis_periodtype][i][0]) & (data['df_d'].index <= dct_periods[analysis_periodtype][i][-1])].copy()
                    df_h = data['df_h'][(data['df_h'].index >= dct_periods[analysis_periodtype][i][0]) & (data['df_h'].index <= dct_periods[analysis_periodtype][i][-1])].copy()
                else:
                    df_d = df_d.append(data['df_d'][(data['df_d'].index >= dct_periods[analysis_periodtype][i][0]) & (data['df_d'].index <= dct_periods[analysis_periodtype][i][-1])].copy())
                    df_h = df_h.append(data['df_h'][(data['df_h'].index >= dct_periods[analysis_periodtype][i][0]) & (data['df_h'].index <= dct_periods[analysis_periodtype][i][-1])].copy())
                if len(subset_periodtype) != 0:
                    if 'df_d_sub' not in locals():
                        df_d_sub = data['df_d'][(data['df_d'].index >= dct_periods[subset_periodtype][i][0]) & (data['df_d'].index <= dct_periods[subset_periodtype][i][-1])].copy()
                        df_h_sub = data['df_h'][(data['df_h'].index >= dct_periods[subset_periodtype][i][0]) & (data['df_h'].index <= dct_periods[subset_periodtype][i][-1])].copy()
                    else:
                        df_d_sub = df_d_sub.append(data['df_d'][(data['df_d'].index >= dct_periods[subset_periodtype][i][0]) & (data['df_d'].index <= dct_periods[subset_periodtype][i][-1])].copy())
                        df_h_sub = df_h_sub.append(data['df_h'][(data['df_h'].index >= dct_periods[subset_periodtype][i][0]) & (data['df_h'].index <= dct_periods[subset_periodtype][i][-1])].copy())

if Filter:
    for Loc in df_d['Location'].unique():
        df_d.loc[df_d['Location']==Loc, df_d.keys()], df_h.loc[df_h['Location']==Loc, df_h.keys()] = FilteringUHI.FilteringUHI(df_d.loc[df_d['Location']==Loc, df_d.keys()], df_h.loc[df_h['Location']==Loc, df_h.keys()])
        
        if len(subset_periodtype) != 0:
            df_d_sub.loc[df_d_sub['Location']==Loc, df_d_sub.keys()], df_h_sub.loc[df_h_sub['Location']==Loc, df_h_sub.keys()] = FilteringUHI.FilteringUHI(df_d_sub.loc[df_d_sub['Location']==Loc, df_d_sub.keys()], df_h_sub.loc[df_h_sub['Location']==Loc, df_h_sub.keys()])
            
            
            
#%%###ANALYSIS###

df_d['sm_cor'] = np.nan
for City in df_d['City'].unique():
    df_d.loc[df_d['City'] == City, 'sm_cor'] = df_d.loc[df_d['City'] == City, 'sm']-np.nanmin(df_d.loc[df_d['City'] == City,'sm'])


df_d['T_max_dif'] = df_d['T_max_urban'] - df_d['T_max_rural']

df_d['DTR_dif'] = df_d['DTR_urban'] - df_d['DTR_rural']


df_d['T_min_rural'] = df_d['T_max_rural'] - df_d['DTR_rural']
df_d['T_min_urban'] = df_d['T_max_urban'] - df_d['DTR_urban']
df_d['T_min_dif'] = df_d['T_min_urban'] -  df_d['T_min_rural']


df_d['Norm_loc'] = df_d['Norm']/(2-(df_d['P_green']/100)-df_d['SVF'])
df_d['UHI_norm_loc'] = df_d['UHI_max']/df_d['Norm_loc']
df_d['UHI_norm'] = df_d['UHI_max']/df_d['Norm']

if len(subset_periodtype) != 0:
    df_d_sub['Norm_loc'] = df_d_sub['Norm']/(2-(df_d_sub['P_green']/100)-df_d_sub['SVF'])
    df_d_sub['UHI_norm_loc'] = df_d_sub['UHI_max']/df_d_sub['Norm_loc']
    df_d_sub['UHI_norm'] = df_d_sub['UHI_max']/df_d_sub['Norm']


#%%###VISUALIZATION###

#Visualization total

Visualization.Boxplot(cat='LCZ', dataframe=df_d, analysis_periodtype=analysis_periodtype, analysis_year=analysis_year)
Visualization.Boxplot(cat='City', dataframe=df_d, analysis_periodtype=analysis_periodtype, analysis_year=analysis_year)


Visualization.Scatter(cat='DTR_rural', dataframe = df_d, analysis_name=analysis_name)



Visualization.ScatterCitySM(cat1 = 'UHI_max', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCitySM(cat1 = 'UHI_norm', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCitySM(cat1 = 'UHI_norm_loc', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCitySM(cat1 = 'UHI_int', dataframe = df_d, analysis_name=analysis_name)

Visualization.ScatterCitySM(cat1 = 'T_max_urban', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCitySM(cat1 = 'T_max_rural', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCitySM(cat1 = 'T_max_dif', dataframe = df_d, analysis_name=analysis_name)

Visualization.ScatterCitySM(cat1 = 'T_min_urban', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCitySM(cat1 = 'T_min_rural', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCitySM(cat1 = 'T_min_dif', dataframe = df_d, analysis_name=analysis_name)

Visualization.ScatterCitySM(cat1 = 'DTR_urban', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCitySM(cat1 = 'DTR_rural', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCitySM(cat1 = 'DTR_dif', dataframe = df_d, analysis_name=analysis_name)


Visualization.ScatterCity(cat1 = 'UHI_max', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCity(cat1 = 'UHI_norm', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCity(cat1 = 'UHI_norm_loc', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCity(cat1 = 'UHI_int', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)

Visualization.ScatterCity(cat1 = 'T_max_urban', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCity(cat1 = 'T_max_rural', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCity(cat1 = 'T_max_dif', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)

Visualization.ScatterCity(cat1 = 'T_min_urban', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCity(cat1 = 'T_min_rural', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCity(cat1 = 'T_min_dif', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)

Visualization.ScatterCity(cat1 = 'DTR_urban', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCity(cat1 = 'DTR_rural', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)
Visualization.ScatterCity(cat1 = 'DTR_dif', cat2 = 'API0.85_rural', dataframe = df_d, analysis_name=analysis_name)


for loc in df_d['Location'].unique():
    Visualization.ScatterSelect(cat = 'UHI_norm', cat_select = 'Location', select=loc, dataframe=df_d, analysis_name=analysis_name)

if 'df_d_sub' in globals():
    Visualization.ScatterSubset(cat = 'UHI_max', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubset(cat = 'UHI_int', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubset(cat = 'UHI_norm', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubset(cat = 'UHI_norm_loc', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubset(cat = 'Norm_loc', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubset(cat = 'DTR_urban', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubset(cat = 'T_max_urban', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    
    Visualization.ScatterSubsetCity(cat1 = 'UHI_norm_loc', cat2 = 'sm', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubsetCity(cat1 = 'UHI_norm_loc', cat2 = 'P_green', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)

    Visualization.ScatterSubsetCity(cat1 = 'UHI_norm', cat2 = 'sm', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubsetCity(cat1 = 'UHI_norm', cat2 = 'API0.85_rural', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)




    
    for loc in df_d['Location'].unique():
        Visualization.ScatterSubsetSelect(cat = 'UHI_norm_loc', cat_select = 'Location', select=loc, dataframe=df_d, dataframe_sub=df_d_sub, analysis_name=analysis_name)
        Visualization.ScatterSubsetSelect(cat = 'UHI_norm', cat_select = 'Location', select=loc, dataframe=df_d, dataframe_sub=df_d_sub, analysis_name=analysis_name)
        Visualization.ScatterSubsetSelect(cat = 'UHI_max', cat_select = 'Location', select=loc, dataframe=df_d, dataframe_sub=df_d_sub, analysis_name=analysis_name)

    
    






fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(df_d['sm_cor'], df_d['DTR_urban'], c=pd.factorize(df_d['City'])[0])
fig.show()


 



#Visualization per location

plot_count = 1
fig_count = 1
fig = plt.figure(figsize=(20,10))

#For every location
for Loc in df_h['Location'].unique():
    df = df_h.loc[df_h['Location'] == Loc]
    ax = fig.add_subplot(3,3,plot_count)
    ax.plot(df['T_urban'], color='red')
    ax.plot(df['T_rural'], color='green')
    ax.set_title(Loc + ', LCZ = ' + str(df['LCZ'][0]))
    ax.set_ylabel('Temperature')
    ax.figure.autofmt_xdate()
    

    
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    if plot_count == 9:
        fig.tight_layout()
        plt.savefig('Figures/TimeSerie_temperature_no'+ str(fig_count) + '_' +  analysis_name)
        plt.close()
        fig_count += 1
        plot_count = 1
        fig = plt.figure(figsize=(20,10))
    else:
        plot_count += 1
    
fig.tight_layout()
plt.savefig('Figures/TimeSerie_temperature_no'+ str(fig_count) + '_' +  analysis_name)
plt.close()