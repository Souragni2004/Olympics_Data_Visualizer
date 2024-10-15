import numpy as np
import pandas as pd

def olympic_years(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.reverse()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years,country
def get_medal_tally(athletes_dummy,noc_region_map,year,country):
    medal_tally = athletes_dummy.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    gold = 0
    silver = 0
    bronze = 0
    if year == 'Overall' and country == 'Overall':
        medal_tally = athletes_dummy.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
        final_tally = medal_tally.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values(['Gold', 'Silver', 'Bronze'], ascending=[False, False, False]).reset_index()
        final_tally['Total'] = final_tally['Gold'] + final_tally['Silver'] + final_tally['Bronze']
        return final_tally
    elif year == 'Overall' and country != 'Overall':
        new_tally = medal_tally[medal_tally['region'] == country]
        new_tally = new_tally.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',ascending=True).reset_index()
        new_tally['Total'] = new_tally['Gold'] + new_tally['Silver'] + new_tally['Bronze']
        return new_tally
    elif year != 'Overall' and country == 'Overall':
        medal_year = medal_tally[medal_tally['Year'] == int(year)]
        new_tally = medal_year.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values(['Gold', 'Silver', 'Bronze'],ascending=False).reset_index()
        new_tally['Total'] = new_tally['Gold'] + new_tally['Silver'] + new_tally['Bronze']
        return new_tally
    else:
        medal_year = medal_tally[medal_tally['Year'] == int(year)]
        new_tally = medal_year.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values(['Gold', 'Silver', 'Bronze'],ascending=False).reset_index()
        new_tally['Total'] = new_tally['Gold'] + new_tally['Silver'] + new_tally['Bronze']
        return new_tally[new_tally['NOC'] == noc_region_map[country]]
def most_successful_athlete(athletes,sports):
    new_df = athletes.dropna(subset = ['Medal'])
    if sports != 'Overall':
        new_df = new_df[new_df['Sport'] == sports]
    y = new_df['Name'].value_counts().reset_index().merge(athletes)[['Name','count','Sport','region']].drop_duplicates('Name').head(10)
    y = y.rename(columns={'count':'Medals','region':'Country'})
    return y
def success_country(athletes,country):
    new_df = athletes.dropna(subset = ['Medal'])
    new_df = new_df[new_df['region'] == country]
    y = new_df['Name'].value_counts().reset_index().merge(athletes)[['Name','count','Sport','region']].drop_duplicates('Name').head(10)
    y = y.rename(columns={'count':'Medals','region':'Country'})
    return y
