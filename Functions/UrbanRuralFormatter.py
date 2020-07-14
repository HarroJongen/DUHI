#Title: Urban and Rural formatter
#Date: 29-06-2020
#Author: Harro Jongen
#Downloads Combines data of rural and urban meteorological station for analysis

def UrbanRuralFormatter(City, urbanfile, ruralfile):
    import pandas as pd
    
    #Read urban and rural file
    Urban = pd.read_csv(urbanfile)
    Rural = pd.read_csv(ruralfile)
    
    #Set dates as datetime
    Urban['date'] = pd.to_datetime(Urban['date'])
    Rural['date'] = pd.to_datetime(Rural['date'])
    
    
    #Calculate timestep
    Urban_dt = Urban['date'][1] - Urban['date'][0]
    Rural_dt = Rural['date'][1] - Rural['date'][0]
    
    #Set date as index
    Urban.set_index('date', inplace=True)
    Rural.set_index('date', inplace=True)
    
    
    #Check if timestep are equal
    if Urban_dt == Rural_dt:
        #Combine stations
        Total = Urban.join(Rural, how = 'outer')
    #Else resample data to largest timestep
    else:
        if Rural_dt < Urban_dt:
            Rural_res =  Rural.resample(Urban_dt).mean()
            #Combine stations
            Total = Urban.join(Rural_res, how = 'outer')
        else:
            Urban_res =  Urban.resample(Rural_dt).mean()
            #Combine stations
            Total = Urban_res.join(Rural, how = 'outer')
    
    #Add UHI column
    Total['UHI'] = Total['T_urban'] - Total['T_rural']
    
    #Write combined stations to csv
    Total.to_csv(urbanfile[0:-9] + 'total.csv')
