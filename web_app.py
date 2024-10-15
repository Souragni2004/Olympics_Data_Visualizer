import streamlit as st
import Graphs
import dataframer,assist
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.figure_factory as ff

noc_data = pd.read_csv('noc2_regions.csv')
athletes = pd.read_csv('athlete_events.csv')

raw_data = dataframer.data(athletes,noc_data)
st.sidebar.title('Olympic Analysis')
st.sidebar.image('https://wallup.net/wp-content/uploads/2017/11/23/525200-olympic-flag-symbols.jpg')
userchoice = st.sidebar.radio('Select an Option',('Medal Tally','Overall Analysis','Nation-wise Analysis','Athlete-wise Analysis'))
if userchoice == 'Medal Tally':
    st.header('Medal Tally')
    years,country = assist.olympic_years(raw_data)
    chosen_year = st.sidebar.selectbox('Year',years)
    chosen_country = st.sidebar.selectbox('Country',country)
    noc_region_map = dict(zip(noc_data['region'], noc_data['NOC']))
    medal_table = assist.get_medal_tally(raw_data,noc_region_map,chosen_year,chosen_country)
    if chosen_year == 'Overall' and chosen_country == 'Overall':
        st.title('Overall Tally')
    elif chosen_year != 'Overall' and chosen_country == 'Overall':
        st.title('Overall Tally in '+ str(chosen_year))
    elif chosen_year == 'Overall' and chosen_country != 'Overall':
        st.title(str(chosen_country) + ' Overall Tally')
    else:
        st.title(str(chosen_country) + ' Overall Medal Tally in '+ str(chosen_year))
    st.table(medal_table)
elif userchoice == 'Overall Analysis':
    editions = raw_data['Year'].unique().shape[0]
    cities = raw_data['City'].unique().shape[0]
    sports = raw_data['Sport'].unique().shape[0]
    events = raw_data['Event'].unique().shape[0]
    nations = raw_data['region'].unique().shape[0]
    participants = raw_data['Name'].unique().shape[0]
    men_participants = raw_data[raw_data['Sex'] == 'M']['Name'].nunique()
    women_participants = raw_data[raw_data['Sex'] == 'F']['Name'].nunique()
    st.title('Historic Stats')
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    with col4:
        st.header("Events")
        st.title(events)

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.header("Nations")
        st.title(nations)
    with col6:
        st.header("Athletes")
        st.title(participants)
    with col7:
        st.header("Men")
        st.title(men_participants)
    with col8:
        st.header("Women")
        st.title(women_participants)
    nations = Graphs.participation(raw_data)
    st.title('Participating Nations over all Editions')
    figure = px.line(nations,x="Edition",y="Participating Nations")
    st.plotly_chart(figure)
    events = Graphs.events(raw_data)
    st.title('Events over all editions')
    figure = px.line(events,x="Edition",y="Events")
    st.plotly_chart(figure)
    names = Graphs.compete(raw_data)
    st.title('No. of Athletes over all editions')
    figure = px.line(names,x="Edition",y="No. of Athletes")
    st.plotly_chart(figure)
    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(25,35))
    x = athletes.drop_duplicates(['Year', 'Sport', 'Event'])
    pivot_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    ax = sns.heatmap(pivot_data,annot=True,fmt='d',cmap='coolwarm',linewidths=0.3,linecolor='black',cbar_kws={'shrink': 0.8})
    st.pyplot(fig)

    st.title('Top 10 most decorated athletes')
    games_list = athletes['Sport'].unique().tolist()
    games_list.sort()
    games_list.insert(0, 'Overall')
    chosen_sport = st.selectbox('Sport',games_list)
    z = assist.most_successful_athlete(raw_data,chosen_sport)
    st.table(z)
elif userchoice == 'Nation-wise Analysis':
    st.sidebar.title('Nation-Wise Analysis')
    country_list = np.unique(raw_data['region'].dropna().values).tolist()
    country_list.sort()
    chosen_country = st.sidebar.selectbox('Nation', country_list)
    z = Graphs.graph(raw_data,chosen_country)
    st.title('Medals won by '+ chosen_country + ' across all editions')
    figure = px.line(z, x="Year", y="Total")
    st.plotly_chart(figure)
    st.title('Medals in events won by ' + chosen_country + ' across all editions')
    fig,ax = plt.subplots(figsize=(18, 22))
    pivot_data = Graphs.heatmap(raw_data,chosen_country)
    ax = sns.heatmap(pivot_data, annot=True, cmap='viridis', linewidths=0.5, linecolor='gray', cbar=True, square=True)
    st.pyplot(fig)
    st.title('Most decorated athletes of ' + chosen_country + ' across all editions')
    decorated = assist.success_country(raw_data,chosen_country)
    st.table(decorated)
    st.title(chosen_country + ' contingent across all editions')
    contingent = Graphs.contingent_list(raw_data,chosen_country)
    fig = px.line(contingent, x="Edition", y="No. of Athletes")
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)
else:
    st.title('Most Probable age for winning an Olympic Medal')
    athlete_df = raw_data.drop_duplicates(subset=['Name', 'region'])
    z1 = athlete_df['Age'].dropna().tolist()
    z2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna().tolist()
    z3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna().tolist()
    z4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna().tolist()
    fig = ff.create_distplot([z1, z2, z3, z4],['Overall Age', 'Gold Medallist', 'Silver Medallist', 'Bronze Medallist'], show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)
    st.title('Distribution of Age wrt sports(Gold Medallist)')
    age,sports = Graphs.probable_age(raw_data,'Gold')
    fig = ff.create_distplot(age, sports, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
    st.title('Distribution of Age wrt sports(Silver Medallist)')
    age, sports = Graphs.probable_age(raw_data, 'Silver')
    fig = ff.create_distplot(age, sports, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
    selected_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                       'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                       'Tennis', 'Golf', 'Softball', 'Archery',
                       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                       'Rhythmic Gymnastics', 'Rugby Sevens',
                       'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    selected_sports.sort()
    selected_sports.insert(0,'Overall')
    sel_sports = st.selectbox('Sports',selected_sports)
    st.title('Weight vs Height for ' + sel_sports)
    temp_df = Graphs.w_vs_h(raw_data,sel_sports)
    fig,ax = plt.subplots(figsize=(8,8))
    ax = sns.scatterplot(x="Weight",y="Height",data=temp_df,hue=temp_df['Medal'])
    st.pyplot(fig)
    st.title('Men vs Women participation in Olympics')
    last = Graphs.gender(raw_data)
    figure = px.line(last, x="Year", y=["Male", "Female"])
    figure.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(figure)



