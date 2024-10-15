import pandas as pd
import numpy as np

def participation(athletes):
    nations = athletes.groupby('Year')['region'].nunique().reset_index(name='Participating Nations')
    nations = nations.rename(columns={'Year': 'Edition'})
    return nations
def events(athletes):
    events = athletes.groupby('Year')['Event'].nunique().reset_index(name='Events')
    events = events.rename(columns={'Year': 'Edition'})
    return events
def compete(athletes):
    names = athletes.groupby('Year')['Name'].nunique().reset_index(name='No. of Athletes')
    names = names.rename(columns={'Year': 'Edition'})
    return names
def graph(athletes_dummy,country):
  medal_tally = athletes_dummy.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
  new_tally = medal_tally[medal_tally['region'] == country]
  new_tally = new_tally.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
  new_tally['Total']= new_tally['Gold']+new_tally['Silver']+new_tally['Bronze']
  return new_tally
def heatmap(athletes,country):
    z = athletes.dropna(subset=['Medal'])
    z.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_z = z[z['region'] == country]
    all_sports = athletes['Sport'].unique()
    all_sports.sort()
    all_years = athletes['Year'].unique()
    all_years.sort()
    pivot_data = new_z.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    pivot_data = pivot_data.reindex(index=all_sports, columns=all_years, fill_value=0)
    return pivot_data
def contingent_list(athletes,country):
  participants = athletes[athletes['region'] == country]
  participants = participants.drop_duplicates(subset=['Name','Year'])
  names = participants.groupby('Year')['Name'].nunique().reset_index(name='No. of Athletes')
  names = names.rename(columns={'Year':'Edition'})
  return names
def probable_age(athletes,medal):
    age_data = []
    sport_names = []
    unique_athletes = athletes.drop_duplicates(subset=['Name', 'region'])
    selected_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                       'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                       'Tennis', 'Golf', 'Softball', 'Archery',
                       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                       'Rhythmic Gymnastics', 'Rugby Sevens',
                       'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in selected_sports:
        filtered_sport_df = unique_athletes[unique_athletes['Sport'] == sport]
        age_data.append(filtered_sport_df[filtered_sport_df['Medal'] == medal]['Age'].dropna())
        sport_names.append(sport)
    return age_data,sport_names
def w_vs_h(athletes,game):
    athlete_df = athletes.drop_duplicates(subset=['Name', 'region'])
    sports_df = athlete_df['Medal'].fillna('No Medal', inplace=True)
    temp_df = athlete_df[athlete_df['Sport'] == game]
    if game == 'Overall':
        return athlete_df
    else:
        return temp_df
def gender(athletes):
    athlete_df = athletes.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year')['Name'].size().reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year')['Name'].size().reset_index()
    last = men.merge(women, on='Year')
    last.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    print(last)
    return last
