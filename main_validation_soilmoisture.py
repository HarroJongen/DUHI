#Title: Validation of soil moisture
#Date: 23-07-2020
#Author: Harro Jongen
#Script for validating remote sensing soil moisture data against in situ observations in Cabauw and Veenkampen

#%%
###IMPORTING###

import datetime
import pandas as pd
import matplotlib.pyplot as plt
import math
    
from Functions import SatelliteToTimeseries, FormatterCabauw, FormatterVeenkampen, ValStat

#%%
###SETTINGS###

#Define period of interest
start = datetime.datetime(2017, 1, 1)
end = datetime.datetime(2018 , 12, 31)

#%%
###FORMATTING DATA###

#Create soil moisture time series for validation
SatelliteToTimeseries.SatelliteToTimeseries('Cabauw', 	(51.969, 4.926), start, end)
SatelliteToTimeseries.SatelliteToTimeseries('Veenkampen', (51.981, 5.620), start, end)

#Soil moisture time series from Veenkampen en Cabauw
FormatterCabauw.FormatterCabauw('Data/SoilMoisture/Cabauw/', start, end)
FormatterVeenkampen.FormatterVeenkampen(start, end)


#Read all data remote sensed (rs) and in situ (is), create date index and combine ber location
Cabauw_rs = pd.read_csv('Data/Cabauw_rs_SoilMoisture.csv')
Cabauw_rs['date'] = pd.to_datetime(Cabauw_rs['date'])
Cabauw_rs.set_index('date', inplace=True)

Cabauw_is = pd.read_csv('Data/Cabauw_SoilMoisture.csv')
Cabauw_is['date'] = pd.to_datetime(Cabauw_is['date'])
Cabauw_is.set_index('date', inplace=True)

Cabauw_df = Cabauw_rs.join(Cabauw_is, how = 'outer')


Veenk_rs = pd.read_csv('Data/Veenkampen_rs_SoilMoisture.csv')
Veenk_rs['date'] = pd.to_datetime(Veenk_rs['date'])
Veenk_rs.set_index('date', inplace=True)

Veenk_is = pd.read_csv('Data/Veenkampen_SoilMoisture.csv')
Veenk_is['date'] = pd.to_datetime(Veenk_is['date'])
Veenk_is.set_index('date', inplace=True)

Veenk_df = Veenk_rs.join(Veenk_is, how = 'outer')

#%%
###VALIDATION###

#Create dataframe for statistics
Stats = pd.DataFrame(columns=['loc', 'var', 'MSE', 'MSE_s', 'MSE_u', 'RMSE', 'RMSE_s', 'RMSE_u', 'pearson_r', 'spearman_r'])

#Calculate statistics
Stats = ValStat.ValStat(Cabauw_df, 'sm', Stats, 'Cabauw')
Stats = ValStat.ValStat(Veenk_df, 'sm', Stats, 'Veenkampen')
    
#%%
###VISUALIZATION###

#Determine dimensions of subplots
key_ls = ['sm_03', 'sm_05', 'sm_19', 'sm_33', 'sm_40', 'sm_56']
dim_Cabauw = math.ceil(math.sqrt(len(key_ls)))
dim_Veenk = math.ceil(math.sqrt(len(Veenk_df.keys())))

#Scatter remote vs in situ observations
fig = plt.figure()
for var, num in zip(key_ls, range(1,len(key_ls))):
    ax = fig.add_subplot(dim_Cabauw,dim_Cabauw,num)
    ax.scatter(Cabauw_df['sm'], Cabauw_df[[var]])
    ax.plot([0,1], [-0,1], color='red')
    ax.set_title(var)
fig.tight_layout()

fig = plt.figure()
for var, num in zip(Veenk_df.keys()[1:], range(1,len(Veenk_df.keys()))):
    ax = fig.add_subplot(dim_Veenk,dim_Veenk,num)
    ax.scatter(Veenk_df['sm'], Veenk_df[[var]])
    ax.plot([0,1], [-0,1], color='red')
    ax.set_title(var)
fig.tight_layout()


    
    

