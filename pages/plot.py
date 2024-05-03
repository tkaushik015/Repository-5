import streamlit as st
import pandas as pd
import plotly.express as px

# Set page width
st.set_page_config(layout="wide")

# Load data
@st.cache
def load_bowling_data():
    return pd.read_csv('2023_bowling.csv')

@st.cache
def load_batting_data():
    return pd.read_csv('2023_batting.csv')

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
        st.subheader('Bowling Statistics Visualizations')

        # Pie chart of Wickets distribution by Country
        st.write("Pie chart of Wickets distribution by Country:")
        wickets_by_country = filtered_bowling_df.groupby("Country")["Wickets"].sum().reset_index()
        fig = px.pie(wickets_by_country, values='Wickets', names='Country', title='Wickets distribution by Country')
        st.plotly_chart(fig, use_container_width=True)

        # Pie chart of Wickets distribution by Bowler
        st.write("Pie chart of Wickets distribution by Bowler:")
        wickets_by_bowler = filtered_bowling_df.groupby("Name")["Wickets"].sum().reset_index()
        fig = px.pie(wickets_by_bowler, values='Wickets', names='Name', title='Wickets distribution by Bowler')
        st.plotly_chart(fig, use_container_width=True)

    elif analysis_option == 'Batting Stats':
        filtered_batting_df = filter_batting_data(batting_df)
        st.write(filtered_batting_df)

        # Visualizations for Batting Stats
        st.subheader('Batting Statistics Visualizations')

        # Pie chart of Runs distribution by Player
        st.write("Pie chart of Runs distribution by Player:")
        runs_distribution_by_player = filtered_batting_df.groupby("Name")["Runs"].sum().reset_index()
        fig = px.pie(runs_distribution_by_player, values='Runs', names='Name', title='Runs distribution by Player')
        st.plotly_chart(fig, use_container_width=True)

        # Bar plot of Runs by Player
        st.write("Bar plot of Runs by Player:")
        runs_by_player = filtered_batting_df.groupby("Name")["Runs"].sum().reset_index()
        fig = px.bar(runs_by_player, x='Name', y='Runs', title='Runs by Player')
        st.plotly_chart(fig, use_container_width=True)

        # Pie chart of Hundred's distribution by Country
        st.write("Pie chart of Hundred's distribution by Country:")
        hundreds_by_country = batting_df.groupby("Country")["Hundreds"].sum().reset_index()
        fig = px.pie(hundreds_by_country, values='Hundreds', names='Country', title='Hundred\'s distribution by Country')
        st.plotly_chart(fig, use_container_width=True)

        # Pie chart of Fifties distribution by Country for all countries
        st.write("Pie chart of Fifties distribution by Country:")
        fifties_by_country_all = batting_df.groupby("Country")["Fifties"].sum().reset_index()
        fig = px.pie(fifties_by_country_all, values='Fifties', names='Country', title='Fifties distribution by Country')
        st.plotly_chart(fig, use_container_width=True)

        # Bar plot of Batting Averages by Player
        st.write("Bar plot of Batting Averages by Player:")
        fig_avg = px.bar(filtered_batting_df, x='Name', y='Average', title='Batting Averages by Player')
        st.plotly_chart(fig_avg, use_container_width=True)

        # Table of Top Power hitters
        st.subheader('Top Power hitters')
        top_power_hitters = filtered_batting_df[filtered_batting_df['Strike_rate'] >= 150].reset_index(drop=True)
        top_power_hitters.index += 1  # Start numbering from 1
        st.write(top_power
