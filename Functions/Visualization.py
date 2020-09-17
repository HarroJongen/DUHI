#Title: DUHI visualization
#Date: 04-09-2020
#Author: Harro Jongen
#Visualization functions for the DUHI project

def Boxplot(cat, dataframe, analysis_periodtype, analysis_date):
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(figsize=(20,10), nrows=2, ncols=2)

    dataframe.boxplot(column='UHI_max', by=cat, ax=axes[0,0])
    axes[0,0].set_ylabel('UHI_max')
    axes[0,0].set_title('')
    
    dataframe.boxplot(column='UHI_int', by=cat, ax=axes[0,1])
    axes[0,1].set_ylabel('UHI_int')
    axes[0,1].set_title('')
    
    dataframe.boxplot(column='T_max_urban', by=cat, ax=axes[1,0])
    axes[1,0].set_ylabel('T_max in city')
    axes[1,0].set_title('')
    
    dataframe.boxplot(column='DTR_urban', by=cat, ax=axes[1,1])
    axes[1,1].set_ylabel('DTR in city')
    axes[1,1].set_title('')
    
    fig.suptitle('Boxplots by ' + cat + ' for ' + analysis_periodtype + ' ' + analysis_date)
    
    plt.savefig('Figures/Boxplots_' + cat + '_' +  analysis_periodtype + '_' + analysis_date)
    plt.close()

def Scatter(cat, dataframe, analysis_name):
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(figsize=(20,10), nrows=1, ncols=2)
    
    axes[0].scatter(dataframe['sm_cor'], dataframe[cat])
    axes[0].set_ylabel(cat)
    axes[0].set_xlabel('Soil moisture')
  
    axes[1].scatter(dataframe['API0.85_rural'], dataframe[cat])
    axes[1].set_xlabel('Antecedent precipitation index (k = 0.85)')
    
    fig.suptitle('Scatter ' + cat + ' against moisture proxies')
    
    plt.savefig('Figures/Scatter_' + cat + '_SM_' +  analysis_name)
    plt.close()

def ScatterCity(cat1, cat2, dataframe, analysis_name):
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(figsize=(20,10), nrows=2, ncols=2)
    
    axes[0,0].scatter(dataframe[cat2], dataframe[cat1 ])
    axes[0,0].set_ylabel(cat1)
    axes[0,0].set_title('All cities')
  
    axes[0,1].scatter(dataframe[dataframe['City'] == 'Amsterdam'][cat2], dataframe[dataframe['City'] == 'Amsterdam'][cat1])
    axes[0,1].set_title('Amsterdam')

    axes[1,0].scatter(dataframe[dataframe['City'] == 'Rotterdam'][cat2], dataframe[dataframe['City'] == 'Rotterdam'][cat1])
    axes[1,0].set_ylabel(cat1)
    axes[1,0].set_xlabel(cat2)
    axes[1,0].set_title('Rotterdam')

    axes[1,1].scatter(dataframe[dataframe['City'] == 'Gent'][cat2], dataframe[dataframe['City'] == 'Gent'][cat1])
    axes[1,1].set_xlabel(cat2)
    axes[1,1].set_title('Gent')

    
    fig.suptitle('Scatter ' + cat1 + ' against ' + cat2 + ' per city')
    
    plt.savefig('Figures/Scatter_' + cat1 + '_' + cat2[0] + '_' +  analysis_name)
    plt.close()
    
def ScatterCitySM(cat1, dataframe, analysis_name):
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(figsize=(20,10), nrows=2, ncols=2)
    
    axes[0,0].scatter(dataframe['sm_cor'], dataframe[cat1 ])
    axes[0,0].set_ylabel(cat1)
    axes[0,0].set_title('All cities')
  
    axes[0,1].scatter(dataframe[dataframe['City'] == 'Amsterdam']['sm'], dataframe[dataframe['City'] == 'Amsterdam'][cat1])
    axes[0,1].set_title('Amsterdam')

    axes[1,0].scatter(dataframe[dataframe['City'] == 'Rotterdam']['sm'], dataframe[dataframe['City'] == 'Rotterdam'][cat1])
    axes[1,0].set_ylabel(cat1)
    axes[1,0].set_xlabel('sm')
    axes[1,0].set_title('Rotterdam')

    axes[1,1].scatter(dataframe[dataframe['City'] == 'Gent']['sm'], dataframe[dataframe['City'] == 'Gent'][cat1])
    axes[1,1].set_xlabel('sm')
    axes[1,1].set_title('Gent')

    
    fig.suptitle('Scatter ' + cat1 + ' against sm per city')
    
    plt.savefig('Figures/Scatter_' + cat1 + '_sm_' +  analysis_name)
    plt.close()

def ScatterSelect(cat, cat_select, select, dataframe, analysis_name):
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(figsize=(20,10), nrows=1, ncols=2)
    
    axes[0].scatter(dataframe[dataframe[cat_select] == select]['sm'], dataframe[dataframe[cat_select] == select][cat])
    axes[0].set_ylabel(cat)
    axes[0].set_xlabel('Soil moisture')
  
    axes[1].scatter(dataframe[dataframe[cat_select] == select]['API0.85_rural'], dataframe[dataframe[cat_select] == select][cat])
    axes[1].set_xlabel('Antecedent precipitation index (k = 0.85)')
    
    fig.suptitle('Scatter ' + cat + ' against moisture proxies for ' + cat_select + ' is ' + select)
    
    plt.savefig('Figures/Scatter_' + cat + '_' + select + '_SM_' +  analysis_name)
    plt.close()

#%% Subset plots

def ScatterSubset(cat, dataframe, dataframe_sub, analysis_name):
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(figsize=(20,10), nrows=1, ncols=2)
    
    axes[0].scatter(dataframe['sm'], dataframe[cat])
    axes[0].scatter(dataframe_sub['sm'], dataframe_sub[cat])
    axes[0].set_ylabel(cat)
    axes[0].set_xlabel('Soil moisture')
  
    axes[1].scatter(dataframe['API0.85_rural'], dataframe[cat])
    axes[1].scatter(dataframe_sub['API0.85_rural'], dataframe_sub[cat])
    axes[1].set_xlabel('Antecedent precipitation index (k = 0.85)')
    
    fig.suptitle('Scatter ' + cat + ' against moisture proxies')
    
    plt.savefig('Figures/Scatter_' + cat + '_SM_' +  analysis_name)
    plt.close()
    
def ScatterSubsetSelect(cat, cat_select, select, dataframe, dataframe_sub, analysis_name):
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(figsize=(20,10), nrows=1, ncols=2)
    
    axes[0].scatter(dataframe[dataframe[cat_select] == select]['sm'], dataframe[dataframe[cat_select] == select][cat])
    axes[0].scatter(dataframe_sub[dataframe_sub[cat_select] == select]['sm'], dataframe_sub[dataframe_sub[cat_select] == select][cat])
    axes[0].set_ylabel(cat)
    axes[0].set_xlabel('Soil moisture')
  
    axes[1].scatter(dataframe[dataframe[cat_select] == select]['API0.85_rural'], dataframe[dataframe[cat_select] == select][cat])
    axes[1].scatter(dataframe_sub[dataframe_sub[cat_select] == select]['API0.85_rural'], dataframe_sub[dataframe_sub[cat_select] == select][cat])
    axes[1].set_xlabel('Antecedent precipitation index (k = 0.85)')
    
    fig.suptitle('Scatter ' + cat + ' against moisture proxies for ' + cat_select + ' is ' + select)
    
    plt.savefig('Figures/Scatter_' + cat + '_' + select + '_SM_' +  analysis_name)
    plt.close()
    
def ScatterSubsetC(cat, dataframe, dataframe_sub, analysis_name, c = None):
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(figsize=(20,10), nrows=1, ncols=2)
    
    axes[0].scatter(dataframe['sm'], dataframe[cat], c=dataframe[c])
    axes[0].scatter(dataframe_sub['sm'], dataframe_sub[cat], c=dataframe_sub[c])
    axes[0].set_ylabel(cat)
    axes[0].set_xlabel('Soil moisture')
  
    axes[1].scatter(dataframe['API0.85_rural'], dataframe[cat], c=dataframe[c])
    axes[1].scatter(dataframe_sub['API0.85_rural'], dataframe_sub[cat], c=dataframe_sub[c])
    axes[1].set_xlabel('Antecedent precipitation index (k = 0.85)')
    
    fig.suptitle('Scatter ' + cat + ' against moisture proxies')
    
    plt.savefig('Figures/Scatter_' + cat + '_SM_' +  analysis_name)
    plt.close()
    
def ScatterSubsetSelectC(cat, cat_select, select, dataframe, dataframe_sub, analysis_name, c = None):
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(figsize=(20,10), nrows=1, ncols=2)
    
    axes[0].scatter(dataframe[dataframe[cat_select] == select]['sm'], dataframe[dataframe[cat_select] == select][cat], c=dataframe[dataframe[cat_select] == select][c])
    axes[0].scatter(dataframe_sub[dataframe_sub[cat_select] == select]['sm'], dataframe_sub[dataframe_sub[cat_select] == select][cat], c=dataframe_sub[dataframe_sub[c]])
    axes[0].set_ylabel(cat)
    axes[0].set_xlabel('Soil moisture')
  
    axes[1].scatter(dataframe[dataframe[cat_select] == select]['API0.85_rural'], dataframe[dataframe[cat_select] == select][cat], c=dataframe[dataframe[cat_select] == select][c])
    axes[1].scatter(dataframe_sub[dataframe_sub[cat_select] == select]['API0.85_rural'], dataframe_sub[dataframe_sub[cat_select] == select][cat], c=dataframe_sub[dataframe_sub[c]])
    axes[1].set_xlabel('Antecedent precipitation index (k = 0.85)')
    
    fig.suptitle('Scatter ' + cat + ' against moisture proxies for ' + cat_select + ' is ' + select)
    
    plt.savefig('Figures/Scatter_' + cat + '_' + select + '_SM_' +  analysis_name)
    plt.close()
    
def ScatterSubsetCity(cat1, cat2, dataframe, dataframe_sub, analysis_name):
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(figsize=(20,10), nrows=2, ncols=2)
    
    axes[0,0].scatter(dataframe[cat2], dataframe[cat1 ])
    axes[0,0].scatter(dataframe_sub[cat2], dataframe_sub[cat1 ])
    axes[0,0].set_ylabel(cat1)
    axes[0,0].set_title('All cities')
  
    axes[0,1].scatter(dataframe[dataframe['City'] == 'Amsterdam'][cat2], dataframe[dataframe['City'] == 'Amsterdam'][cat1])
    axes[0,1].scatter(dataframe_sub[dataframe_sub['City'] == 'Amsterdam'][cat2], dataframe_sub[dataframe_sub['City'] == 'Amsterdam'][cat1])
    axes[0,1].set_title('Amsterdam')

    axes[1,0].scatter(dataframe[dataframe['City'] == 'Rotterdam'][cat2], dataframe[dataframe['City'] == 'Rotterdam'][cat1])
    axes[1,0].scatter(dataframe_sub[dataframe_sub['City'] == 'Rotterdam'][cat2], dataframe_sub[dataframe_sub['City'] == 'Rotterdam'][cat1])
    axes[1,0].set_ylabel(cat1)
    axes[1,0].set_xlabel(cat2)
    axes[1,0].set_title('Rotterdam')

    axes[1,1].scatter(dataframe[dataframe['City'] == 'Gent'][cat2], dataframe[dataframe['City'] == 'Gent'][cat1])
    axes[1,1].scatter(dataframe_sub[dataframe_sub['City'] == 'Gent'][cat2], dataframe_sub[dataframe_sub['City'] == 'Gent'][cat1])
    axes[1,1].set_xlabel(cat2)
    axes[1,1].set_title('Gent')

    
    fig.suptitle('Scatter ' + cat1 + ' against ' + cat2 + ' per city')
    
    plt.savefig('Figures/Scatter_' + cat1 + '_' + cat2[0] + '_' +  analysis_name)
    plt.close()