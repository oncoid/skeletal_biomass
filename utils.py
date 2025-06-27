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
    
    return time[(time['scale_level']==scale) & (time.max_ma<=max_time)].copy()

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
        temp = temp[temp[skeletal_grain]!=-1]
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
    mean_ma = [float(time[dat[time_period] == time.interval_name].iloc[0].mean_ma) for _,dat in data.iterrows()]
    data['mean_ma'] = mean_ma

    data = data.sort_values(by=['mean_ma'], ascending=False)
    return data


def get_phylum_level_occurrence(occurrence):
    relative_occurrence = dict.fromkeys(occurrence['early_interval'].unique(),{})
    for time_interval in occurrence['early_interval'].unique():
        
        subset = occurrence[occurrence['early_interval'] == time_interval].copy()
        relative_occurrence[time_interval] = dict.fromkeys(occurrence['phylum'].unique(), np.nan)
        for phylum in occurrence['phylum'].unique():
            relative_occurrence[time_interval][phylum] = subset[subset['phylum'] == phylum]['phylum'].count()
    relative_occurrence = pd.DataFrame(relative_occurrence).T
    return relative_occurrence


def get_relative_occurrence_percentage(relative_occurrence):
    relative_occurrence = relative_occurrence.astype(float)
    for i in range(len(relative_occurrence)):
        dat = relative_occurrence.iloc[i]
        relative_occurrence.iloc[i] = np.array(dat.to_list())*100/np.array(dat.to_list()).sum()
    
    return relative_occurrence


def get_total_occurrence(dat):
    
    return np.array(dat.to_list()).sum()
    

def load_data(file_path, low_memory=True):
    occurrence = pd.read_csv(file_path,low_memory=low_memory)
    return occurrence[['phylum', 'early_interval']]


def load_occurrence_data():
    animal_occurrence = pd.read_csv(f'./data/pbdb_occurrence_data/pbdb.cleaned.animals.csv',low_memory=False)
    algae_occurrence = pd.read_csv(f'./data/pbdb_occurrence_data/pbdb.cleaned.algae.csv',low_memory=False)
    protist_occurrence = pd.read_csv(f'./data/pbdb_occurrence_data/pbdb.cleaned.protists.csv',low_memory=False)
    
    return animal_occurrence, algae_occurrence, protist_occurrence


def get_mean_ma(relative_occurrence_time, time_epoch):
    k = relative_occurrence_time
    if 'Upper' in k:
        k = ' '.join(['Late', k.split()[-1]])
    elif 'Lower' in k:
        k = ' '.join(['Early', k.split()[-1]])
    elif k == 'Miaolingian':
        k = 'Series 3'
    return time_epoch[time_epoch['interval_name'] == k]['mean_ma'].values[0]


def get_animal_phyllum_occurrence(animal_relative_occurrence, time_epoch):
    animal_relative_occurrence_phylum = get_relative_occurrence_percentage(animal_relative_occurrence.copy())
    animal_relative_occurrence_phylum.reset_index(inplace=True)
    animal_relative_occurrence_phylum['mean_ma'] = animal_relative_occurrence_phylum['index'].apply(lambda x: get_mean_ma(x,time_epoch))
    animal_relative_occurrence_phylum.reset_index(inplace=True)

    for i, dat in animal_relative_occurrence_phylum.iterrows():
        k = dat['index']
        if 'Upper' in k:
            animal_relative_occurrence_phylum.at[i,'index'] = ' '.join(['Late', k.split()[-1]])
        elif 'Lower' in k:
            animal_relative_occurrence_phylum.at[i,'index'] = ' '.join(['Early', k.split()[-1]])
        elif k == 'Miaolingian':
            animal_relative_occurrence_phylum.at[i,'index'] = 'Series 3'
            
    return animal_relative_occurrence_phylum


def get_skeletal_occurrence(animal_relative_occurrence, algae_relative_occurrence, protist_relative_occurrence, time_epoch):
    # calculate skeletal occurrence
    animal_relative_occurrence['animal'] = animal_relative_occurrence.apply(get_total_occurrence, axis=1)
    algae_relative_occurrence['algae'] = algae_relative_occurrence.apply(get_total_occurrence, axis=1)
    protist_relative_occurrence['protist'] = protist_relative_occurrence.apply(get_total_occurrence, axis=1)
    
    animal_relative_occurrence.reset_index(inplace=True)
    animal_relative_occurrence['mean_ma'] = animal_relative_occurrence['index'].apply(lambda x: get_mean_ma(x,time_epoch))
    animal_relative_occurrence.rename(columns={'index':'time'}, inplace=True)

    algae_relative_occurrence.reset_index(inplace=True)
    algae_relative_occurrence['mean_ma'] = algae_relative_occurrence['index'].apply(lambda x: get_mean_ma(x,time_epoch))
    algae_relative_occurrence.rename(columns={'index':'time'}, inplace=True)

    protist_relative_occurrence.reset_index(inplace=True)
    protist_relative_occurrence['mean_ma'] = protist_relative_occurrence['index'].apply(lambda x: get_mean_ma(x,time_epoch))
    protist_relative_occurrence.rename(columns={'index':'time'}, inplace=True)

    
    skeletal_occurrence = pd.DataFrame({'time': animal_relative_occurrence['time'], 'animal':animal_relative_occurrence['animal'],'mean_ma':animal_relative_occurrence['mean_ma']})
    skeletal_occurrence = skeletal_occurrence.merge(algae_relative_occurrence[['algae', 'time']],on='time', how='outer')
    skeletal_occurrence = skeletal_occurrence.merge(protist_relative_occurrence[['protist', 'time']],on='time', how='outer')

    skeletal_occurrence['total'] = [np.sum(dat[['animal', 'algae','protist']]) for _, dat in skeletal_occurrence.iterrows()]

    skeletal_occurrence['animal']=skeletal_occurrence['animal']*100/skeletal_occurrence['total']
    skeletal_occurrence['algae']=skeletal_occurrence['algae']*100/skeletal_occurrence['total']
    skeletal_occurrence['protist']=skeletal_occurrence['protist']*100/skeletal_occurrence['total']

    skeletal_occurrence.sort_values(by='mean_ma', ascending=False, inplace=True)
    
    for i, dat in skeletal_occurrence.iterrows():
        k = dat['time']
        if 'Upper' in k:
            skeletal_occurrence.at[i,'time'] = ' '.join(['Late', k.split()[-1]])
        elif 'Lower' in k:
            skeletal_occurrence.at[i,'time'] = ' '.join(['Early', k.split()[-1]])
        elif k == 'Miaolingian':
            skeletal_occurrence.at[i,'time'] = 'Series 3'
            
    return skeletal_occurrence

            
def get_skeletal_animal_phyllum_occurrence(animal_occurrence, algae_occurrence, protist_occurrence, time_epoch):
    animal_relative_occurrence = get_phylum_level_occurrence(animal_occurrence)
    algae_relative_occurrence = get_phylum_level_occurrence(algae_occurrence)
    protist_relative_occurrence = get_phylum_level_occurrence(protist_occurrence)
    
    # for animal phylum level relative occurrence
    animal_relative_occurrence_phylum = get_animal_phyllum_occurrence(animal_relative_occurrence, time_epoch)
        
    skeletal_occurrence = get_skeletal_occurrence(animal_relative_occurrence, algae_relative_occurrence, protist_relative_occurrence, time_epoch)
   

    # no data for Pridoli
    skeletal_occurrence = skeletal_occurrence[~(skeletal_occurrence['time'] == 'Pridoli')]
    animal_relative_occurrence_phylum = animal_relative_occurrence_phylum[~(animal_relative_occurrence_phylum['index'] == 'Pridoli')]
    
    return skeletal_occurrence, animal_relative_occurrence_phylum


def get_sep_epoch(time, time_epoch):
    if time == 0:
        return 'Holocene'
    else:
        return time_epoch[(time_epoch['max_ma']>=time) & (time_epoch['min_ma']<time)]['interval_name'].values[0]
    
def load_sepkoski_diversity_data():
    time_file = './data/timeScale.xlsx'
    time = pd.read_excel(time_file,sheet_name='Sheet1')
    time_epoch = get_timesubset(time,4,541)

    sepkoski_div = pd.read_excel('./data/SQS_diversity_data/sepkoski_diversity.xlsx')
    sepkoski_div = sepkoski_div[sepkoski_div['Date']<=541]
    sepkoski_div['epoch'] = sepkoski_div['Date'].apply(lambda x: get_sep_epoch(x, time_epoch))


    
    sepkoski_div_epoch = []
    for epoch in sepkoski_div.epoch.unique():
        subset = sepkoski_div[sepkoski_div['epoch'] == epoch]
        sepkoski_div_epoch.append(dict(epoch = epoch, diversity = subset['Total D'].mean()))
    sepkoski_div_epoch = pd.DataFrame(sepkoski_div_epoch)
    
    sepkoski_div_epoch['mean_ma'] = sepkoski_div_epoch['epoch'].apply(lambda x: time_epoch[time_epoch['interval_name'] == x]['mean_ma'].values[0])
    return sepkoski_div_epoch