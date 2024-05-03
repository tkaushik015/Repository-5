import streamlit as st
import pandas as pd
import plotly.express as px

# Set page width
st.set_page_config(layout="wide")

# Load data
@st.cache
def load_bowling_data():
    df = pd.read_csv('2023_bowling.csv', index_col=0)  # Assuming the index column is the first column
    df.index += 1  # Add 1 to the index
    return df

@st.cache
def load_batting_data():
    df = pd.read_csv('2023_batting.csv', index_col=0)  # Assuming the index column is the first column
    df.index += 1  # Add 1 to the index
    return df

bowling_df = load_bowling_data()
batting_df = load_batting_data()

# Sidebar filters
st.sidebar.header('Filters')
analysis_option = st.sidebar.selectbox('Analysis Option', ['Bowling Stats', 'Batting Stats'])

country_list = list(bowling_df['Country'].unique())

country = st.sidebar.selectbox("Select Country", country_list)

# Function to filter bowling data
def filter_bowling_data(df):
    if country:
        df2 = df[df['Country'].str.contains(country, case=False)]
    else:
        df2 = df  # Return original dataframe if no country selected
    return df2

# Function to filter batting data
def filter_batting_data(df):
    if country:
        df2 = df[df['Country'].str.contains(country, case=False)]
    else:
        df2 = df  # Return original dataframe if no country selected
    return df2

# Function to filter batting data by country
def filter_batting_data_by_country(df, country):
    if country:
        return df[df['Country'] == country]
    else:
        return df

if st.sidebar.button('Submit'):
    if analysis_option == 'Bowling Stats':
        filtered_bowling_df = filter_bowling_data(bowling_df)
        st.write(filtered_bowling_df)

        # Visualizations for Bowling Stats
        st.subheader('**Bowling Statistics Visualizations**')

        # Pie chart of Wickets distribution by Country
        st.write("**Pie chart of Wickets distribution by Country:**")
        wickets_by_country = bowling_df.groupby("Country")["Wickets"].sum().reset_index()
        fig = px.pie(wickets_by_country, values='Wickets', names='Country', title='Wickets distribution by Country')
        st.plotly_chart(fig, use_container_width=True)

        # Pie chart of Wickets distribution by Bowler
        st.write("**Pie chart of Wickets distribution by Bowler:**")
        wickets_by_bowler = filtered_bowling_df.groupby("Name")["Wickets"].sum().reset_index()
        fig = px.pie(wickets_by_bowler, values='Wickets', names='Name', title='Wickets distribution by Bowler')
        st.plotly_chart(fig, use_container_width=True)

        # Bar plot Showing Wickets Taken by Players
        st.write("**Bar plot Showing Wickets Taken by Players:**")
        fig_bar = px.bar(filtered_bowling_df, x='Name', y='Wickets', title='Wickets Taken by Players')
        st.plotly_chart(fig_bar, use_container_width=True)

        # Best Bowling Average bar plot
        st.subheader('**Best Bowling Average**')
        best_bowling_average = filtered_bowling_df[['Name', 'Average']].copy()
        best_bowling_average = best_bowling_average[best_bowling_average['Average'] != 0]  # Filter non-zero averages
        best_bowling_average = best_bowling_average.sort_values(by='Average').reset_index(drop=True)
        best_bowling_average.index += 1  # Start numbering from 1
        fig_best_avg = px.bar(best_bowling_average, x='Name', y='Average', title='Best Bowling Average')
        st.plotly_chart(fig_best_avg, use_container_width=True)

        # Table of Number of Four Wicket Hauls by Each Player
        st.subheader('**Number of Four Wicket Hauls by Each Player**')
        four_wickets_by_player = filtered_bowling_df[['Name', 'Four_wickets']].copy()
        four_wickets_by_player = four_wickets_by_player[four_wickets_by_player['Four_wickets'] != 0]  # Filter non-zero four wickets
        four_wickets_by_player.index += 1  # Start numbering from 1
        st.write(four_wickets_by_player)

        # Table of Number of Five Wicket Hauls by Each Player
        st.subheader('**Number of Five Wicket Hauls by Each Player**')
        five_wickets_by_player = filtered_bowling_df[['Name', 'Five_wickets']].copy()
        five_wickets_by_player = five_wickets_by_player[five_wickets_by_player['Five_wickets'] != 0]  # Filter non-zero five wickets
        five_wickets_by_player.index += 1  # Start numbering from 1
        st.write(five_wickets_by_player)

        # Table of Top Economical Players
        st.subheader('**Top Economical Players**')
        top_economical_players = filtered_bowling_df[['Name', 'Economy']].copy()
        top_economical_players = top_economical_players[top_economical_players['Economy'] != 0]  # Filter non-zero economy
        top_economical_players = top_economical_players.sort_values(by='Economy').reset_index(drop=True)
        top_economical_players.index += 1  # Start numbering from 1
        st.write(top_economical_players)

        # Correlation Matrix for Bowling Stats
        st.subheader('**Correlation Matrix for Bowling Stats:**')
        bowling_heatmap = filtered_bowling_df.select_dtypes(include=['float64', 'int64']).corr()
        st.write(bowling_heatmap)

    elif analysis_option == 'Batting Stats':
        filtered_batting_df = filter_batting_data(batting_df)
        st.write(filtered_batting_df)

        # Orange Cap Pie Chart
        st.subheader('**Orange Cap Pie Chart**')

        # Pie chart of Runs distribution by Player
        runs_distribution_by_player = filtered_batting_df.groupby("Name")["Runs"].sum().reset_index()
        fig = px.pie(runs_distribution_by_player, values='Runs', names='Name', title='Runs distribution by Player')
        st.plotly_chart(fig, use_container_width=True)

        # Bar plot of Bar Plot Showing Runs Scored by Players
        st.subheader('**Bar Plot Showing Runs Scored by Players**')
        runs_by_player = filtered_batting_df.groupby("Name")["Runs"].sum().reset_index()
        fig = px.bar(runs_by_player, x='Name', y='Runs', title='Bar Plot Showing Runs Scored by Players')
        st.plotly_chart(fig, use_container_width=True)

        # Pie chart of Hundred's distribution by Country
        st.sub
