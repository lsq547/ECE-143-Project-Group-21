import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def comp_score(df, col):
    '''
    Calculate score for developers/publisher based on 20% avg # of game released, 20% total owners, 20% avg total reviews, 40% avg ratings
    :df: pd.DataFrame
    :col: developer col or publisher col
    :return: df: pd.DateFrame
    '''
    from scipy import stats
    
    assert isinstance(df, pd.DataFrame)
    assert isinstance(col,str)
    
    if col=='developer':
        df['dev_score'] = (0.2*stats.zscore(np.log10(df['game_num']))+0.2*stats.zscore(np.log10(df['sum_owners']))+0.2*stats.zscore(np.log10(df['avg_total_ratings']))+0.4*stats.zscore(df['avg_rating']))/5
    else:
        df['pub_score'] = (0.2*stats.zscore(np.log10(df['game_num']))+0.2*stats.zscore(np.log10(df['sum_owners']))+0.2*stats.zscore(np.log10(df['avg_total_ratings']))+0.4*stats.zscore(df['avg_rating']))/5
    return df

def pivot_col(df, col):
    '''
    Create pivot table for given column (developers/publisher)
    :df: pd.Datadrame
    :col: pivot column
    :return: pivot table
    '''
    assert isinstance(df, pd.DataFrame)
    assert isinstance(col,str)
    
    pvtable = pd.pivot_table(df,index=col, values=['appid','price','total_ratings','rating','owners'], 
                  aggfunc={'appid':'count','price':np.mean,'total_ratings':np.mean,'rating':np.mean,'owners':np.sum}).rename(
                  {'appid':'game_num','price':'avg_price','total_ratings':'avg_total_ratings','rating':'avg_rating','owners':'sum_owners'}, axis=1)
    comp_score(pvtable,col)
    if col=='developer':
        top_comp=pvtable.sort_values('dev_score', ascending=False).head(10)
    else:
        top_comp=pvtable.sort_values('pub_score', ascending=False).head(10)
    return top_comp


def genre_and_company(df, col):
    '''
    Get the chart describing number of games each genre for top 10 developers/publishers
    :col: devloper or publisher col
    :return: dataframe of num games each genre for each top developer/publisher
    '''
    assert isinstance(df, pd.DataFrame)
    assert col=='developer' or col=='publisher'
    
    top_dev_pub=pivot_col(df,col)
    genre_chart = pd.DataFrame()
    for i in top_dev_pub.index:
        dev_pub_game = df[df[col].str.match(i,case=False)].sort_values(by='rating', ascending=False)
        genre_chart[i] = dev_pub_game[['Action','Adventure','Casual','FPS','Indie','Racing','RPG','Simulation','Sports','Strategy']].sum()
    return genre_chart

def top_game_of_company(df,col):
    '''
    Get the chart of top 5 rated games for each of top 10 developers/publishers
    :col: devloper or publisher col
    :return: dataframe of top 5 rated games for each top developer/publisher
    '''
    assert isinstance(df, pd.DataFrame)
    assert col=='developer' or col=='publisher'

    top_dev_pub=pivot_col(df,col)
    top_list=[]
    for i in top_dev_pub.index:
        top_game = df[df[col] == i].sort_values(by='rating', ascending=False)
        top_list.append( ', '.join([i for i in top_game.name[:5]]))
    top_dev_pub['top_5_game'] = top_list
    pd.set_option('display.max_colwidth', 300)
    if col=='developer':
        return top_dev_pub[['dev_score', 'top_5_game']]
    else:
        return top_dev_pub[['pub_score', 'top_5_game']]

def radar_chart(df,col,comp,n,gcolor):
    '''
    Plot the radar chart on genres of given developer/publisher
    :df: dataframe of given dev/pub
    :col: a str indicating developer or publisher
    :comp: a str indicating name of the developer/publisher
    :n: float representing maximum grid range
    :gcolor: color str indicating color of the plot
    '''
    assert isinstance(df, pd.DataFrame)
    assert isinstance(col,str)
    assert isinstance(comp,str)
    assert isinstance(n,float)
    assert isinstance(gcolor,str)
    
    #choose columns on genre data
    stats = df[['Action','Adventure','Casual','FPS','Indie','Racing','RPG','Simulation','Sports','Strategy']].sum() #df[df[col] == comp].iloc[:,-10:].sum()
    stats = stats[stats!=0]
    labels = np.array(list(stats.index))
    vals = stats.values
    vals = vals / sum(vals)+0.1
    #print(vals)
    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    stats=np.concatenate((vals,[vals[0]]))
    angles=np.concatenate((angles,[angles[0]]))
    #print(angles)

    fig=plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', color=gcolor,linewidth=1)
    ax.fill(angles, stats, color=gcolor, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, labels, fontsize=14)
    for label, angle in zip(ax.get_xticklabels(), angles):
        if 1.5*np.pi>angle>np.pi/2:
            label.set_horizontalalignment('right')
        else:
            label.set_horizontalalignment('left')
       
    ax.set_title(comp+' as '+col,fontweight='bold',fontsize=15,y=1.1)
    ax.set_rlim(0,n)
    ax.grid(True)
    ax.set_rgrids(np.arange(0,n,0.3), angle=45)

def plot_barh(df,pub):
    '''
    Plot stacked horizontal bar chart for given publisher
    :df: dataframe of given publisher
    :pub: str indicating publisher name
    '''
    assert isinstance(df, pd.DataFrame)
    assert isinstance(pub,str)
    
    pub_df=df[df['publisher'].str.match(pub,case=False)].groupby('release_year').sum()
    ax=pub_df.loc[:,['Action','Adventure','Casual','FPS','Indie','Racing','RPG','Simulation','Sports','Strategy']]
    ax.plot.barh(stacked=True,figsize=(10,8), title=pub+" Game Distribution by Year")

def plot_pie(df,dev_pub):
    '''
    Plot pie charts for top 10 developers/publishers
    :df: cleaned dataframe 
    :dev_pub: str indicating developer or publisher
    '''
    assert isinstance(df, pd.DataFrame)
    assert isinstance(dev_pub,str)
    
    top_comp=pivot_col(df,dev_pub)
    pi_chart=genre_and_company(df, dev_pub).transpose()
    pi_chart.set_index(top_comp.index)
    fig, axes = plt.subplots(2, 5, figsize=(18, 6))
    color_map={'Action':'#1f77b4','Adventure':'#ff7f0e','Casual':'#2ca02c','FPS':'#d62728','Indie':'#9467bd','Racing':'#8c564b','RPG':'#e377c2','Simulation':'#7f7f7f','Sports':'#bcbd22','Strategy':'#17becf'}
    for i, (idx, row) in enumerate(pi_chart.set_index(top_comp.index).iterrows()):
        ax = axes[i // 5, i % 5]
        #row = row[row.gt(row.sum() * .01)]
        ax.pie(row, colors=[color_map[i] for i in row.index],startangle=30) #autopct='%1.1f%%',
        ax.set_title(idx, fontweight='bold')
    #set patch color and labels for legend
    patch_list = []
    for key in color_map:
        data_key = mpatches.Patch(color=color_map[key], label=key)
        patch_list.append(data_key)
    fig.legend(handles=patch_list,labels=color_map.keys())
    plt.subplots_adjust(wspace=0.4,right=0.9)
