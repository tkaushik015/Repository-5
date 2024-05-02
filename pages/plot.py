import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache
def load_batting_data():
    return pd.read_csv('2023_batting.csv')

batting_df = load_batting_data()

# Sidebar filters
st.sidebar.header('Filters')
country_list = list(batting_df['Country'].unique())
country = st.sidebar.selectbox("Select Country", country_list)

# Function to filter batting data
def filter_batting_data(df):
    if country:
        df2 = df[df['Country'].str.contains(country, case=False)]
    else:
        df2 = df  # Return original dataframe if no country selected
    return df2

if st.sidebar.button('Submit'):
    filtered_batting_df = filter_batting_data(batting_df)
    st.write(filtered_batting_df)

    # Visualizations for Batting Stats
    st.subheader('Batting Statistics Visualizations')

    # Pie chart of Hundred's distribution by Country
    st.write("Pie chart of Hundred's distribution by Country:")
    hundreds_by_country = filtered_batting_df.groupby("Country")["Hundreds"].sum().reset_index()
    fig = px.pie(hundreds_by_country, values='Hundreds', names='Country', title='Hundred\'s distribution by Country')
    st.plotly_chart(fig)

    # Pie chart of Fifties distribution by Country
    st.write("Pie chart of Fifties distribution by Country:")
    fifties_by_country = filtered_batting_df.groupby("Country")["Fifties"].sum().reset_index()
    fig = px.pie(fifties_by_country, values='Fifties', names='Country', title='Fifties distribution by Country')
    st.plotly_chart(fig)

else:
    st.write(batting_df)
