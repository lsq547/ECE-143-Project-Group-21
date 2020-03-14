import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def generate_df():
    """
    Loads, reformats, and merges DataFrame needed to perform tag-level analysis
    :return: Merged and Modified DataFrame, all_df
    """
    steam_df = pd.read_csv('./dataset/steam.csv')
    tags_df = pd.read_csv('./dataset/steamspy_tag_data.csv')

    steam_df.set_index('appid', inplace=True)
    tags_df.set_index('appid', inplace=True)

    steam_df['scores'] = (steam_df['positive_ratings']) / (steam_df['negative_ratings'] + steam_df['positive_ratings'])
    steam_df['num_reviews'] = steam_df['positive_ratings'] + steam_df['negative_ratings']
    steam_df['release_year'] = steam_df.apply(lambda row: row['release_date'].split('-')[0], axis = 1)
    steam_df['release_year'] = steam_df['release_year'].astype('int')

    all_df = pd.merge(steam_df, tags_df, on='appid')

    tags = list(tags_df.columns.values)
    tags = tags
    for tag in tags:
        all_df.loc[all_df[tag] >= (all_df[tags].max(axis=1) / 2), tag] = 1
        all_df.loc[all_df[tag] < (all_df[tags].max(axis=1) / 2), tag] = 0

    return all_df


def get_tags():
    """
    Returns a list of all the existing tags used in Steam games
    :return: list of strings: all the tags used in Steam
    """
    temp = pd.read_csv('./dataset/steamspy_tag_data.csv')
    temp.set_index('appid', inplace=True)
    tags = list(temp.columns.values)
    return tags


def find_changed_tags_ratios(all_df, n):
    """
    Returns a list of the tags and their relative prevalence that have changed the most in the past 10 years
    :param all_df: DataFrame used to find these tags
    :param n: Number of tags to be returned
    :return: List of n tags that have changed the most, relative presence of each tag by year (categorical)
    """

    assert(isinstance(n, int))
    assert(n > 0)

    tags = get_tags()
    years = all_df.groupby('release_year')
    tag_counts = years[tags].agg(['sum'])
    tag_ratio = tag_counts.div(tag_counts.sum(axis=1), axis=0)
    tag_diff = tag_ratio.loc[2008:2018].max() - tag_ratio.loc[2008:2018].min()
    changed_tags = tag_diff.sort_values(ascending=False).head(n).index
    changed_tags = list(list(zip(*list(changed_tags)))[0])

    return changed_tags, tag_ratio


def plot_tag_prevalence(tags, ratios):
    """
    Plots the relative prevalence of the tags given by year
    Try to limit the number of tags inputted to avoid crowding the plot
    :param tags: list of tags used by Steam
    :param ratios: tag_ratio categorical given by find_changed_tags
    """

    assert(isinstance(tags, list))
    assert(len(tags) > 0)

    fig = plt.figure()
    for tag in tags:
        plt.plot(np.arange(2008, 2020), ratios.loc[2008:2019][tag].values, label=tag[0].upper() + tag[1:])
    plt.xlabel('Year', fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylabel('Representation Across All Tags', fontsize=14)
    lg = plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fancybox=True, shadow=True, fontsize=14)
    plt.xlim((2008, 2019))
    fig.patch.set_alpha(0)
    plt.show()


def plot_tag_scores_per_year(all_df, tag):
    """
    Plots histograms for the scores received by a specific tag by year
    :param all_df: DataFrame generated with generate_df
    :param tag: The tag used to plot scores
    """

    assert(isinstance(tag, str))
    assert(len(tag) > 0)

    years = all_df.groupby('release_year')
    colors = plt.cm.winter_r(np.linspace(0, 1, 7))

    fig = plt.figure()
    for n in range(2012, 2019):
        c = tuple(colors[n - 2012])[0:3]
        subset = years.get_group(n)
        subset_scores = subset.loc[subset[tag] == 1]['scores']
        sns.distplot(subset_scores, bins=101, kde=True, kde_kws={'color': c}, hist=False, label='%d' % n)
    lg = plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fancybox=True, shadow=True, prop={'size': 14})
    plt.title('Distribution of ' + tag + ' Scores by Year', fontsize=16)
    fig.patch.set_alpha(0)
    plt.xlabel('Score', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()

