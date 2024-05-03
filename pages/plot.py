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

# Filter to compare batsmen
st.sidebar.header('Compare Batsmen')
batsmen_to_compare = st.sidebar.multiselect('Select Batsmen', batting_df['Name'].unique())

if st.sidebar.button('Compare'):
    filtered_batting_df = batting_df[batting_df['Name'].isin(batsmen_to_compare)]
    st.write(filtered_batting_df)

    # Visualizations for Batting Stats
    st.subheader('**Batting Statistics Visualizations**')

    # Bar plot of Runs by Player
    st.subheader('**Bar Plot Showing Runs Scored by Players**')
    runs_by_player = filtered_batting_df.groupby("Name")["Runs"].sum().reset_index()
    fig = px.bar(runs_by_player, x='Name', y='Runs', title='Bar Plot Showing Runs Scored by Players')
    st.plotly_chart(fig, use_container_width=True)

    # Bar plot of Batting Averages by Player
    st.subheader('**Batting Averages of Players**')
    fig_avg = px.bar(filtered_batting_df, x='Name', y='Average', title='Batting Averages of Players')
    st.plotly_chart(fig_avg, use_container_width=True)

else:
    if analysis_option == 'Bowling Stats':
        st.write(bowling_df)

    elif analysis_option == 'Batting Stats':
        st.write(batting_df)

# Set background color
def set_background_color(color):
    st.markdown(f"""
        <style>
            .reportview-container {{
                background-color: {color};
            }}
            h1, h2, h3, h4, h5, h6 {{
                font-size: 18px;
            }}
        </style>
    """, unsafe_allow_html=True)

set_background_color("#000000")
