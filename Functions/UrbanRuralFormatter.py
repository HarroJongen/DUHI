#Title: Urban and Rural formatter
#Date: 29-06-2020
#Author: Harro Jongen
#Downloads Combines data of rural and urban meteorological station for analysis

def UrbanRuralFormatter(City, urbanfile, ruralfile):
    import pandas as pd
    import datetime
    
    #Read urban and rural file
    Urban = pd.read_csv(urbanfile)
    Rural = pd.read_csv(ruralfile)
    
    #Set dates as datetime
    Urban['date'] = pd.to_datetime(Urban['date'])
    Rural['date'] = pd.to_datetime(Rural['date'])
    
    #Set date as index
    Urban.set_index('date', inplace=True)
    Rural.set_index('date', inplace=True)
    
    #Resample data to hourly timestep
    Urban_res = Urban.resample(datetime.timedelta(1/24)).mean()
    Rural_res = Rural.resample(datetime.timedelta(1/24)).mean()
    #Combine stations
    Total = Urban_res.join(Rural_res, how = 'outer')
    
    #Add UHI column
    Total['UHI'] = Total['T_urban'] - Total['T_rural']
    
    #Write combined stations to csv
    Total.to_csv(urbanfile[0:-9] + 'total.csv')
