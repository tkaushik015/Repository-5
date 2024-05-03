import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Load data
@st.cache
def load_bowling_data():
    return pd.read_csv('2023_bowling.csv')

@st.cache
def load_batting_data():
    return pd.read_csv('2023_batting.csv')

bowling_df = load_bowling_data()
batting_df = load_batting_data()

# Custom CSS for black background
st.markdown(
    """
    <style>
    .reportview-container {
        background: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Images for IPL
ipl_images = [
    "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.moneycontrol.com%2Fsports%2Fcricket%2Fipl-2024-csk-to-face-rcb-in-tournament-opener-on-march-22-bcci-announces-21-match-schedule-article-12332511.html&psig=AOvVaw0_gphs1H4ge14zNs0WMzbl&ust=1714781526579000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCKD2pZGZ8IUDFQAAAAAdAAAAABAE",
    "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwallpapers.com%2Fipl-2021&psig=AOvVaw0_gphs1H4ge14zNs0WMzbl&ust=1714781526579000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCKD2pZGZ8IUDFQAAAAAdAAAAABAR",
    "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwisden.com%2Fstories%2Fglobal-t20-leagues%2Findian-premier-league-2024%2Fipl-2024-auction-full-list-captains-each-team-ahead-csk-mi-rcb-kkr-dc-rr-srh-pbks-lsg-gt&psig=AOvVaw0_gphs1H4ge14zNs0WMzbl&ust=1714781526579000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCKD2pZGZ8IUDFQAAAAAdAAAAABAh"
]

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
        st.plotly_chart(fig)

        # Pie chart of Wickets distribution by Bowler
        st.write("Pie chart of Wickets distribution by Bowler:")
        wickets_by_bowler = filtered_bowling_df.groupby("Name")["Wickets"].sum().reset_index()
        fig = px.pie(wickets_by_bowler, values='Wickets', names='Name', title='Wickets distribution by Bowler')
        st.plotly_chart(fig)

    elif analysis_option == 'Batting Stats':
        filtered_batting_df = filter_batting_data(batting_df)
        st.write(filtered_batting_df)

        # Visualizations for Batting Stats
        st.subheader('Batting Statistics Visualizations')

        # Pie chart of Runs distribution by Player
        st.write("Pie chart of Runs distribution by Player:")
        runs_distribution_by_player = filtered_batting_df.groupby("Name")["Runs"].sum().reset_index()
        fig = px.pie(runs_distribution_by_player, values='Runs', names='Name', title='Runs distribution by Player')
        st.plotly_chart(fig)

        # Bar plot of Runs by Player
        st.write("Bar plot of Runs by Player:")
        runs_by_player = filtered_batting_df.groupby("Name")["Runs"].sum().reset_index()
        fig = px.bar(runs_by_player, x='Name', y='Runs', title='Runs by Player')
        st.plotly_chart(fig)

        # Pie chart of Hundred's distribution by Country
        st.write("Pie chart of Hundred's distribution by Country:")
        hundreds_by_country = batting_df.groupby("Country")["Hundreds"].sum().reset_index()
        fig = px.pie(hundreds_by_country, values='Hundreds', names='Country', title='Hundred\'s distribution by Country')
        st.plotly_chart(fig)

        # Pie chart of Fifties distribution by Country for all countries
        st.write("Pie chart of Fifties distribution by Country:")
        fifties_by_country_all = batting_df.groupby("Country")["Fifties"].sum().reset_index()
        fig = px.pie(fifties_by_country_all, values='Fifties', names='Country', title='Fifties distribution by Country')
        st.plotly_chart(fig)

        # Bar plot for Number of Power Hitters (Strike Rate >= 150) by Country
        st.write("Bar plot of Number of Power Hitters (Strike Rate >= 150) by Country:")
        power_hitters_df = batting_df[batting_df['Strike_rate'] >= 150]
        power_hitters_by_country = power_hitters_df.groupby("Country").size().reset_index(name='Number of Power Hitters')
        fig = px.bar(power_hitters_by_country, x='Country', y='Number of Power Hitters', title='Number of Power Hitters (Strike Rate >= 150) by Country')
        st.plotly_chart(fig)

# Display IPL images that change every 5 seconds
while True:
    for image_url in ipl_images:
        st.image(image_url, use_column_width=True)
        time.sleep(5)
