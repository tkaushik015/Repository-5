elif analysis_option == 'Batting Stats':
    filtered_batting_df = filter_batting_data(batting_df)
    st.write(filtered_batting_df)

    # Visualizations for Batting Stats
    st.subheader('Batting Statistics Visualizations')

    # Pie chart of Hundred's distribution by Country
    st.write("Pie chart of Hundred's distribution by Country:")
    hundreds_by_country = filtered_batting_df.groupby("Country")["Hundreds"].sum().reset_index()
    fig = px.pie(hundreds_by_country, values='Hundreds', names='Country', title='Hundred\'s distribution by Country')
    st.plotly_chart(fig)

    # Scatter plot of Strike Rate vs Fifties
    st.write("Scatter plot of Strike Rate vs Fifties:")
    fig = px.scatter(filtered_batting_df, x='Strike_rate', y='Fifties', title='Strike Rate vs Fifties')
    st.plotly_chart(fig)

    # Bar plot of Runs by Player
    st.write("Bar plot of Runs by Player:")
    runs_by_player = filtered_batting_df.groupby("Name")["Runs"].sum().reset_index()
    fig = px.bar(runs_by_player, x='Name', y='Runs', title='Runs by Player')
    st.plotly_chart(fig)

    # Pie chart of Fifties distribution by Country
    st.write("Pie chart of Fifties distribution by Country:")
    fifties_by_country = filtered_batting_df.groupby("Country")["Fifties"].sum().reset_index()
    fig = px.pie(fifties_by_country, values='Fifties', names='Country', title='Fifties distribution by Country')
    st.plotly_chart(fig)
