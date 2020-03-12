import pandas as pd
import numpy as np
import re

def data_process():
    '''
    Cleaning, transforming the data, adding necessary columns for later analysis
    :return: df: pd.Dataframe
    '''
    import datetime as dt
    
    steamspy_df = pd.read_csv("./dataset/steamspy_data.csv")
    steam_df = pd.read_csv("./dataset/steam.csv")
    steamreq_df = pd.read_csv("./dataset/steam_requirements_data.csv")
    
    #convert price in GBP to USD by merging data from another dataframe
    steamspy_df['initialprice'] = steamspy_df['initialprice']/100
    steamspy_temp = steamspy_df.loc[:, ['appid', 'initialprice']]
    df = pd.merge(steam_df,steamspy_temp,on='appid').drop('price', axis=1)

    #merge system requirement data from another dataframe
    steamreq_df = steamreq_df[['steam_appid', 'recommended']]
    steamreq_df.rename(columns={'steam_appid':'appid'}, inplace=True)
    df = pd.merge(df,steamreq_df,on='appid')
    #df.set_index('appid', inplace=True)
    df.rename(columns={'initialprice':'price', 'recommended':'recommended_spec'}, inplace=True)
    assert sum(df['price'].isna())==0

    #calculate total ratings and positive rating percentage using postive & negative ratings
    df['total_ratings'] = df['positive_ratings']+df['negative_ratings']
    df['rating_score'] = df['positive_ratings']/df['total_ratings']
    #calculate rating using rating algorithm
    df['rating'] = df['rating_score']-(df['rating_score']-0.5)*2**(-np.log10(df['total_ratings'] + 1))
    
    #add release_year column
    yr=pd.to_datetime(df['release_date'])
    df['release_year'] = yr.dt.strftime('%Y')
    
    #convert owners interval to midpoint of the interval
    df['owners'] = df['owners'].str.split(pat='-').apply(lambda x: int((int(x[0])+int(x[1]))/2))
    
    #encode popular categories/genres to individual binary columns
    pop_cat = ['Single-player','Multi-player']
    pop_genre = ['Action','Adventure','Casual','FPS','Indie','Racing','RPG','Simulation','Sports','Strategy']
    for cat in pop_cat:
        df[cat] = np.where(df['categories'].str.contains(cat), 1, 0)
        assert df[cat].sum()>0
    for gen in pop_genre:
        if gen=='FPS':
            df[gen] = np.where(df['steamspy_tags'].str.contains(gen), 1, 0)
        else:
            df[gen] = np.where(df['genres'].str.contains(gen), 1, 0)
        assert df[gen].sum()>0

    
    #parse developers and only take first in list
    df['developer']=df['developer'].str.split(pat=';').apply(lambda x: x[0])
    df['publisher']=df['publisher'].str.split(pat=';').apply(lambda x: x[0])
    
    #parse spec info
    def parse_spec(x):
        x = str(x)
        gpu_info = re.search(r'nvidia\s*(geforce)?\s*([gr]t[xs])?\s*[\d\w]+',x, re.IGNORECASE)
        if gpu_info is not None:
            return gpu_info.group()
        return ''
    df['GPU'] = df['recommended_spec'].apply(parse_spec)

    return df