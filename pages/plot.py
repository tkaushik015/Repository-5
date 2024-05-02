import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data
@st.cache_data
def load_bowling_data():
    return pd.read_csv('2023_bowling.csv')

@st.cache_data
def load_batting_data():
    return pd.read_csv('2023_batting.csv')

bowling_df = load_bowling_data()
batting_df = load_batting_data()

# Sidebar filters
st.sidebar.header('Filters')
analysis_option = st.sidebar.selectbox('Analysis Option', ['Bowling Stats', 'Batting Stats'])

country_list = list(set(batting_df['Country'].unique()).union(set(bowling_df['Country'].unique())))
country = st.sidebar.selectbox("Select Country", country_list)

def filter_bowling_data(df, country):
    if country:
        return df[df['Country'].str.contains(country, case=False)]
    return df

def filter_batting_data(df, country):
    if country:
        return df[df['Country'].str.contains(country, case=False)]
    return df

if st.sidebar.button('Submit'):
    if analysis_option == 'Bowling Stats':
        filtered_bowling_df = filter_bowling_data(bowling_df, country)
        st.write(filtered_bowling_df)

        st.subheader('Bowling Statistics Visualizations')

        # Bar plot of Wickets by Country
        fig = px.bar(filtered_bowling_df, x='Country', y='Wickets', title='Wickets by Country')
        st.plotly_chart(fig)

        # Heatmap of Correlation Matrix
        df4 = filtered_bowling_df[['Inns','Balls','Overs','Runs','Wickets','Average','Economy','Strike_Rate','Four_wickets','Five_wickets']]
        corr_matrix = df4.corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        st.pyplot(plt)

        # Scatter plot of Economy vs Wickets
        fig = px.scatter(filtered_bowling_df, x='Economy', y='Wickets', title='Economy vs Wickets')
        st.plotly_chart(fig)

        # Line plot of Wickets over Time (assuming time-series data available)
        if 'Year' in filtered_bowling_df.columns:
            wickets_by_year = filtered_bowling_df.groupby("Year")["Wickets"].sum().reset_index()
            fig = px.line(wickets_by_year, x="Year", y="Wickets", title='Wickets Over Time')
            st.plotly_chart(fig)

    elif analysis_option == 'Batting Stats':
        filtered_batting_df = filter_batting_data(batting_df, country)
        st.write(filtered_batting_df)

        st.subheader('Batting Statistics Visualizations')

        # Pie chart of Hundred's distribution by Country
        hundreds_by_country = filtered_batting_df.groupby("Country")["Hundreds"].sum().reset_index()
        fig = px.pie(hundreds_by_country, values='Hundreds', names='Country', title='Hundred\'s distribution by Country')
        st.plotly_chart(fig)

        # Scatter plot of Strike Rate vs Fifties
        fig = px.scatter(filtered_batting_df, x='Strike_rate', y='Fifties', title='Strike Rate vs Fifties')
        st.plotly_chart(fig)

        # Box plot of Runs by Country
        fig = px.box(filtered_batting_df, x='Country', y='Runs', title='Runs by Country')
        st.plotly_chart(fig)

        # Line plot of Runs over Time (assuming time-series data available)
        if 'Year' in filtered_batting_df.columns:
            runs_by_year = filtered_batting_df.groupby("Year")["Runs"].sum().reset_index()
            fig = px.line(runs_by_year, x="Year", y="Runs", title='Runs Over Time')
            st.plotly_chart(fig)

else:
    if analysis_option == 'Bowling Stats':
        st.write(bowling_df)
    elif analysis_option == 'Batting Stats':
        st.write(batting_df)

# Player Comparison
st.sidebar.header('Player Comparison')
player1_name = st.sidebar.selectbox("Select Player 1", sorted(set(bowling_df['Name']).union(set(batting_df['Name']))))
player2_name = st.sidebar.selectbox("Select Player 2", sorted(set(bowling_df['Name']).union(set(batting_df['Name']))))

def compare_players(player1, player2):
    player1_bowling = bowling_df[bowling_df['Name'].str.contains(player1, case=False)]
    player1_batting = batting_df[batting_df['Name'].str.contains(player1, case=False)]
    
    player2_bowling = bowling_df[bowling_df['Name'].str.contains(player2, case=False)]
    player2_batting = batting_df[batting_df['Name'].str.contains(player2, case=False)]
    
    comparison_data = pd.DataFrame({
        'Player': [player1, player1, player2, player2],
        'Type': ['Bowling', 'Batting', 'Bowling', 'Batting'],
        'Average': [player1_bowling['Average'].mean(), player1_batting['Average'].mean(), 
                    player2_bowling['Average'].mean(), player2_batting['Average'].mean()],
        'Strike Rate': [player1_bowling['Strike_Rate'].mean(), player1_batting['Strike_rate'].mean(),
                        player2_bowling['Strike_Rate'].mean(), player2_batting['Strike_rate'].mean()],
        'Runs/Wickets': [player1_batting['Runs'].sum(), player1_bowling['Wickets'].sum(),
                         player2_batting['Runs'].sum(), player2_bowling['Wickets'].sum()]
    })
    
    st.write(comparison_data)
    
    # Additional visualizations
    fig = px.bar(comparison_data, x='Player', y=['Average', 'Strike Rate'], color='Type', barmode='group', title='Player Comparison - Averages & Strike Rates')
    st.plotly_chart(fig)

    # Radar chart comparing various metrics for both players
    categories = ['Average', 'Strike Rate', 'Runs/Wickets']
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()

    angles += angles[:1]  # Repeat the first angle to close the plot
    stats1 = comparison_data[comparison_data['Player'] == player1][categories].values.flatten().tolist() + [comparison_data[comparison_data['Player'] == player1][categories].values[0, 0]]
    stats2 = comparison_data[comparison_data['Player'] == player2][categories].values.flatten().tolist() + [comparison_data[comparison_data['Player'] == player2][categories].values[0, 0]]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='polar'))
    ax.plot(angles, stats1, label=player1)
    ax.fill(angles, stats1, alpha=0.1)
    ax.plot(angles, stats2, label=player2)
    ax.fill(angles, stats2, alpha=0.1)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    plt.legend(loc='upper right')
    st.pyplot(plt)

if st.sidebar.button('Compare Players'):
    compare_players(player1_name, player2_name)
