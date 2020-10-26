#Title: Validation Statisitcs
#Date: 12-08-2020
#Author: Harro Jongen
#Function creating a dataframe with validation statistics


def ValStat(data, observations, statistics, location):
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    import numpy as np
    import math
    
    for var in data.keys()[1:]:
        #Create a linear regression model for the variable
        df = data[[observations, var]]
        df = df.dropna()
        
        if len(df) != 0:
            X = pd.DataFrame(df[observations])
            y = pd.DataFrame(df[var])
            
            model = LinearRegression()
            model.fit(X, y)
        
            #Add model prediction to dataframe
            df[var + "_reg"] = model.predict(X)
            
            #Create a list for all statistics of one variable
            ls = []
            #Add location name
            ls.append([location])
            #Add variable name
            ls.append([var])
            #Add MSE (Mean Square Error)
            ls.append([(np.square(np.subtract(df[observations],df[var])).mean())])
            #Add MSE_s (systematic Mean Square Error)
            ls.append([(np.square(np.subtract(df[observations],df[var + "_reg"])).mean())])
            #Add MSE_u (unsystematic Mean Square Error)
            ls.append([(np.square(np.subtract(df[var],df[var + "_reg"])).mean())])
            #Add RMSE (Root Mean Square Error)
            ls.append([(math.sqrt(np.square(np.subtract(df[observations],df[var])).mean()))])
            #Add RMSE_s (systematic Root Mean Square Error)
            ls.append([(math.sqrt(np.square(np.subtract(df[observations],df[var + "_reg"])).mean()))])
            #Add RMSE_u (unsystematic Root Mean Square Error)
            ls.append([(math.sqrt(np.square(np.subtract(df[var],df[var + "_reg"])).mean()))])            
            #Add pearson's correlation
            ls.append([df[observations].corr(df[var], method='pearson')])            
            #Add spearman's correlation
            ls.append([df[observations].corr(df[var], method='spearman')])
        else:
            ls = [[location], [var], [np.nan], [np.nan], [np.nan], [np.nan], [np.nan], [np.nan], [np.nan], [np.nan]]
        
        #Transform list to a dataframe and add to dataframe for statistics
        ls = np.array(ls)
        ls = ls.T
        row = pd.DataFrame(ls, columns=['loc', 'var', 'MSE', 'MSE_s', 'MSE_u', 'RMSE', 'RMSE_s', 'RMSE_u', 'pearson_r', 'spearman_r'])
        statistics = statistics.append(row)
    return(statistics)