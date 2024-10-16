import numpy as np
import scipy 
import pandas as pd 

def expand_data(data):
    temp = data.copy()
    temp = temp.dropna()
    temp = pd.concat([temp,data[data.numberOfSamples == 1]],ignore_index = True)
    
    data_subset = data[data.numberOfSamples>1]
    for _,dat in data_subset.iterrows():
        repeat = dat.numberOfSamples
        dat.numberOfSamples = 1
        dat.skeletal_total = dat.skeletal_total/repeat
        dat.total_animals_new = dat.total_animals_new/repeat
        dat.total_protists_new = dat.total_protists_new/repeat
        dat.total_alga_new = dat.total_alga_new/repeat
        for i in range(repeat):
            temp = pd.concat([temp,dat.to_frame().T],ignore_index = True)
        
    return temp

def get_timesubset(time,scale,max_time):
    
    return time[(time['scale_level']==scale) & (time.max_ma<=max_time)]

def get_stats(data,skeletal_grain,time_period):
    '''data: dataframe with all the values
    skeletal_grain:
    '''
    time_periods = np.unique(data[time_period])
    
    time_sg = []
    mean_sg = []
    median_sg = []
    max_sg = []
    min_sg = []
    no_of_samples = []
    time_period_sg = []
    time_period
    for e in time_periods:
        temp = data[data[time_period] == e].copy()
    
        time_sg.append(temp['mean_ma'].mean())
        
        mean_sg.append(temp[skeletal_grain].mean())
        median_sg.append(temp[skeletal_grain].median())
        max_sg.append(temp[skeletal_grain].quantile(0.75))
        min_sg.append(temp[skeletal_grain].quantile(0.25))
        no_of_samples.append(temp["numberOfSamples"].sum())
    
        time_period_sg.append(e)
        
    data_stats = pd.DataFrame({'time':time_sg,time_period:time_period_sg,'no_of_samp':no_of_samples,
                              'mean':mean_sg,'median':median_sg,
                              'min':min_sg,'max':max_sg})
    
    data_stats=data_stats.sort_values(by=['time'], ascending=False)

    return data_stats


def get_stats_depo_env(data,skeletal_grain,depo_env,time_period):
    '''data: dataframe with all the values
    skeletal_grain: column name for which we want to calculate the mean
    depo_env: which depo environmen, should be same as entries in the database
    '''
    time_periods = np.unique(data[time_period])
    
    time_sg = []
    mean_sg = []
    median_sg = []
    max_sg = []
    min_sg = []
    no_of_samples = []
    time_period_sg = []
    
    data = data[data['framework'] == depo_env]
    
    for e in time_periods:
        temp = data[data[time_period] == e].copy()
    
        time_sg.append(temp['mean_ma'].mean())
        
        mean_sg.append(temp[skeletal_grain].mean())
        median_sg.append(temp[skeletal_grain].median())
        max_sg.append(temp[skeletal_grain].quantile(0.75))
        min_sg.append(temp[skeletal_grain].quantile(0.25))
        no_of_samples.append(temp["numberOfSamples"].sum())
    
        time_period_sg.append(e)
        
    data_stats = pd.DataFrame({'time':time_sg,time_period:time_period_sg,'no_of_samp':no_of_samples,
                              'mean':mean_sg,'median':median_sg,
                              'min':min_sg,'max':max_sg})
    
    data_stats=data_stats.sort_values(by=['time'], ascending=False)

    return data_stats


def get_mean_time(time,data,time_period):
    # get mean_ma for all data points
    mean_ma = [float(time[dat[time_period] == time.interval_name].mean_ma) for _,dat in data.iterrows()]
    data['mean_ma'] = mean_ma

    data = data.sort_values(by=['mean_ma'], ascending=False)
    return data