#Title: Main file for DUHI
#Date: 16-06-2020
#Author: Harro Jongen
#Excecutes the complete proces to analyze the connections of drought and UHI for NL and BE


#%%###IMPORTING###

#Import packages
print('Importing packages and functions')
import datetime
import numpy as np
import glob
import matplotlib.pyplot as plt
import re
import pickle
from sklearn.linear_model import LinearRegression


#Import functions
from Functions import BuilderData, Visualization

#%%###FORMATTING DATA###

#Define k_API
k_API = [0.85]

#All heatwave data
BuilderData.BuilderData(start = datetime.datetime(2018, 7, 15), end = datetime.datetime(2018, 8, 7), data_periodtype = 'Heatwave', k_API = k_API)
BuilderData.BuilderData(start = datetime.datetime(2019, 7, 22), end = datetime.datetime(2019, 7, 27), data_periodtype = 'Heatwave', k_API = k_API)
BuilderData.BuilderData(start = datetime.datetime(2019, 8, 23), end = datetime.datetime(2019, 8, 28), data_periodtype = 'Heatwave', k_API = k_API)

#All summer data
BuilderData.BuilderData(start = datetime.datetime(2018, 7, 1), end = datetime.datetime(2018, 8, 31), data_periodtype = 'Summer', k_API = k_API)
BuilderData.BuilderData(start = datetime.datetime(2019, 7, 1), end = datetime.datetime(2019, 8, 31), data_periodtype = 'Summer', k_API = k_API)

#All yearly data
BuilderData.BuilderData(start = datetime.datetime(2018, 1, 1), end = datetime.datetime(2018, 12, 31), data_periodtype = 'Year', k_API = k_API)
BuilderData.BuilderData(start = datetime.datetime(2019, 1, 1), end = datetime.datetime(2019, 12, 31), data_periodtype = 'Year', k_API = k_API)

#%%###SETTINGS ANALYSIS###

#Choose the dataset for analysis, options are:
    #Heatwave (Selects all heatwaves available)
    #Heatwave_2018 (Selects all heatwaves available from the specified year)
    #Heatwave_20180715 (Selects heatwave starting at the specified date)
    #Summer (Selects all summers available)
    #Summer_2018 (Selects the summer from the specified year)
    #Year (Selects all years available)
    #Year_2018 (Selects the specified year)
#Optional suffixes:
    #_Subset (Followed by Heatwave, Summer or Year, adds extra dataframes as a subset for comparison)
    
analysis_name = 'Year_Subset_Heatwave'
regex = re.compile(r'([A-Za-z]+)_?([0-9]*)_?S?u?b?s?e?t?_?([A-Za-z]*)_?([0-9]*)')
analysis_periodtype = regex.search(analysis_name).group(1)
analysis_date = regex.search(analysis_name).group(2)
subset_periodtype = regex.search(analysis_name).group(3)



#%%###LOADING DATA###

#List all names of pickles available
Pickles = glob.glob('Data/Preprocessed/*')

#Create empty dataframe for the dataset
data = {}

#Define regex item to find characteristics of saved data
regex = re.compile(r'Data/Preprocessed\\df_([dh]+)_([A-Za-z]+)_([0-9]+)_[0-9]+')

#For all preprocessed files
for Pickle in Pickles:
    #Open the pickle file
    infile = open(Pickle,'rb')
    #Define characteristics of the pickle file
    res = regex.search(Pickle).group(1)
    periodtype = regex.search(Pickle).group(2)
    start_day = regex.search(Pickle).group(3)
    
    #Check if the file meets the analysis type
    if analysis_periodtype == periodtype == 'Heatwave' and len(analysis_date) == 0:
        #Heatwave
        if 'df_' + res in data:
            data['df_' + res] = data['df_' + res].append(pickle.load(infile)) 
        else:
            data['df_' + res] = pickle.load(infile)
    elif analysis_periodtype == periodtype == 'Heatwave' and len(analysis_date) == 4 and start_day[0:4] == analysis_date:
        #Heatwave_2018
        if 'df_' + res in data:
            data['df_' + res] = data['df_' + res].append(pickle.load(infile)) 
        else:
            data['df_' + res] = pickle.load(infile)
    elif analysis_periodtype == periodtype == 'Heatwave' and len(analysis_date) == 8 and start_day == analysis_date:
        #Heatwave_20180715
        data['df_' + res] = pickle.load(infile)
    elif (analysis_periodtype == periodtype == 'Summer' or analysis_periodtype == periodtype == 'Year') and len(analysis_date) == 0:
        #Summer
        if 'df_' + res in data:
            data['df_' + res] = data['df_' + res].append(pickle.load(infile)) 
        else:
            data['df_' + res] = pickle.load(infile)
    elif (analysis_periodtype == periodtype == 'Summer' or analysis_periodtype == periodtype == 'Year') and len(analysis_date) == 4 and start_day[0:4] == analysis_date:
        #Summer_2018
        data['df_' + res] = pickle.load(infile)
        
    if (subset_periodtype == periodtype == 'Summer' or subset_periodtype == periodtype == 'Heatwave') and len(analysis_date) == 0:
        #Subset_Heatwave
        if 'df_' + res + '_sub' in data:
            data['df_' + res + '_sub'] = data['df_' + res + '_sub'].append(pickle.load(infile)) 
        else:
            data['df_' + res + '_sub'] = pickle.load(infile)
    elif (subset_periodtype == periodtype == 'Summer' or subset_periodtype == periodtype == 'Heatwave') and len(analysis_date) == 4 and start_day[0:4] == analysis_date:
        #Subset_Heatwave_2018
        if 'df_' + res + '_sub' in data:
            data['df_' + res + '_sub'] = data['df_' + res + '_sub'].append(pickle.load(infile))
        else:
            data['df_' + res + '_sub'] = pickle.load(infile)
    elif len(subset_periodtype) != 0 and len(analysis_date) == 8:
        print('No subset available for this type.')
    infile.close()

#Unpack datasets from dictionairy
df_d = data['df_d']
df_h = data['df_h']
if len(subset_periodtype) != 0:
    df_d_sub = data['df_d_sub']
    df_h_sub = data['df_h_sub']

#Give an analysis_date for titles later on
if len(analysis_date) == 0:
    analysis_date = 'All'
    
#%%###ANALYSIS###

df_d['sm_cor'] = df_d['sm']-df_d['P_sealed']/100*df_d['sm']


df_d['Norm_loc'] = df_d['Norm']/(2-(1-df_d['P_sealed']/100)-df_d['SVF'])
df_d['UHI_norm_loc'] = df_d['UHI_max']/df_d['Norm_loc']
df_d['UHI_norm'] = df_d['UHI_max']/df_d['Norm']

df_d_sub['Norm_loc'] = df_d_sub['Norm']/(2-(1-df_d_sub['P_sealed']/100)-df_d_sub['SVF'])
df_d_sub['UHI_norm_loc'] = df_d_sub['UHI_max']/df_d_sub['Norm_loc']
df_d_sub['UHI_norm'] = df_d_sub['UHI_max']/df_d_sub['Norm']


#%%###VISUALIZATION###

#Visualization total

Visualization.Boxplot(cat='LCZ', dataframe=df_d, analysis_periodtype=analysis_periodtype, analysis_date=analysis_date)
Visualization.Boxplot(cat='City', dataframe=df_d, analysis_periodtype=analysis_periodtype, analysis_date=analysis_date)

fig, axes = plt.subplots(figsize=(20,10), nrows=2, ncols=2)
axes[0,0].scatter(df_d['sm'], df_d['API0.8_rural'])
mask = ~np.isnan(df_d['sm']) & ~np.isnan(df_d['API0.8_rural'])
X = df_d[mask]['sm'].values.reshape(-1, 1)
y = df_d[mask]['API0.8_rural'].values.reshape(-1,1)
reg = LinearRegression()
reg.fit(X,y)
y_pred = reg.predict(np.array(np.arange(0, 1.1, 0.1)).reshape(-1,1))
axes[0,0].plot(np.array(np.arange(0, 1.1, 0.1)).reshape(-1,1), y_pred, color='red')
axes[0,0].set_ylabel('API (k = 0.80)')


axes[0,1].scatter(df_d['sm'], df_d['API0.85_rural'])
mask = ~np.isnan(df_d['sm']) & ~np.isnan(df_d['API0.85_rural'])
X = df_d[mask]['sm'].values.reshape(-1, 1)
y = df_d[mask]['API0.85_rural'].values.reshape(-1,1)
reg = LinearRegression()
reg.fit(X,y)
y_pred = reg.predict(np.array(np.arange(0, 1.1, 0.1)).reshape(-1,1))
axes[0,1].plot(np.array(np.arange(0, 1.1, 0.1)).reshape(-1,1), y_pred, color='red')
axes[0,1].set_ylabel('API (k = 0.85)')


axes[1,0].scatter(df_d['sm'], df_d['API0.9_rural'])
mask = ~np.isnan(df_d['sm']) & ~np.isnan(df_d['API0.9_rural'])
X = df_d[mask]['sm'].values.reshape(-1, 1)
y = df_d[mask]['API0.9_rural'].values.reshape(-1,1)
reg = LinearRegression()
reg.fit(X,y)
y_pred = reg.predict(np.array(np.arange(0, 1.1, 0.1)).reshape(-1,1))
axes[1,0].plot(np.array(np.arange(0, 1.1, 0.1)).reshape(-1,1), y_pred, color='red')
axes[1,0].set_ylabel('API (k = 0.90)')
fig.show()

fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(df_d['sm'], df_d['API0.85_rural'])
mask = ~np.isnan(df_d['sm']) & ~np.isnan(df_d['API0.85_rural'])
X = df_d[mask]['sm'].values.reshape(-1, 1)
y = df_d[mask]['API0.85_rural'].values.reshape(-1,1)
reg = LinearRegression()
reg.fit(X,y)
y_pred = reg.predict(np.array(np.arange(0, 1.1, 0.1)).reshape(-1,1))
ax.plot(np.array(np.arange(0, 1.1, 0.1)).reshape(-1,1), y_pred, color='red')
ax.set_ylabel('API (k = 0.85)')

if 'df_d_sub' in globals():
    Visualization.ScatterSubset(cat = 'UHI_max', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubset(cat = 'UHI_int', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubset(cat = 'UHI_norm', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubset(cat = 'UHI_norm_loc', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubset(cat = 'Norm_loc', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubset(cat = 'DTR_urban', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    Visualization.ScatterSubset(cat = 'T_max_urban', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)
    
    
    
    for loc in df_d['Location'].unique():
        Visualization.ScatterSubsetSelect(cat = 'UHI_norm_loc', cat_select = 'Location', select=loc, dataframe=df_d, dataframe_sub=df_d_sub, analysis_name=analysis_name)
    
    
    
    Visualization.ScatterSubsetSelect(cat = 'UHI_norm_loc', cat_select = 'Location', select = '2236', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)



    Visualization.ScatterSubsetCity(cat1 = 'UHI_norm_loc', cat2 = 'sm', dataframe = df_d, dataframe_sub = df_d_sub, analysis_name = analysis_name)



fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(df_d['sm'], df_d['API0.85_rural'], c = df_d['Seepage'], cmap='RdYlGn')
ax.legend()
fig.show()

fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(df_d['Norm'], df_d['UHI_max'])
ax.legend()
fig.show()

fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(df_d['UHI_max'], df_d['sm'], c = df_d['Seepage'])
fig.show()

#Visualization per location

plot_count = 1
fig = plt.figure()

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
        plot_count = 1
        fig = plt.figure()
    else:
        plot_count += 1
    
fig.tight_layout()