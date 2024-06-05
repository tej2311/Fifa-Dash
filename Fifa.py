import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
file_path = 'Cleaned_Fifa_Dataset.csv'
fifa_df = pd.read_csv(file_path)

# Sidebar for user inputs
st.write("Column Names in the Dataset:", fifa_df.columns)

# Sidebar for user inputs
st.sidebar.header('Filter Players')
selected_clubs = st.sidebar.multiselect('Select Clubs', sorted(fifa_df['Club'].unique()))
selected_nationality = st.sidebar.multiselect('Select Nationality', sorted(fifa_df['Nationality'].unique()))
selected_position = st.sidebar.multiselect('Select Position(s)', fifa_df['Positions'].str.split(', ').explode().unique())
selected_age = st.sidebar.slider('Select Age Range', int(fifa_df['Age'].min()), int(fifa_df['Age'].max()), (int(fifa_df['Age'].min()), int(fifa_df['Age'].max())))
selected_rating = st.sidebar.slider('Select Overall Rating Range', int(fifa_df['Overall Rating'].min()), int(fifa_df['Overall Rating'].max()), (int(fifa_df['Overall Rating'].min()), int(fifa_df['Overall Rating'].max())))
selected_wage = st.sidebar.slider('Select Wage Range (EUR)', int(fifa_df['Wage(EUR)_Avg'].min()), int(fifa_df['Wage(EUR)_Avg'].max()), (int(fifa_df['Wage(EUR)_Avg'].min()), int(fifa_df['Wage(EUR)_Avg'].max())))

# Filter data based on user inputs
filtered_data = fifa_df.copy()
if selected_clubs:
    filtered_data = filtered_data[filtered_data['Club'].isin(selected_clubs)]
if selected_nationality:
    filtered_data = filtered_data[filtered_data['Nationality'].isin(selected_nationality)]
if selected_position:
    filtered_data = filtered_data[filtered_data['Positions'].apply(lambda x: any(pos in x.split(', ') for pos in selected_position))]
filtered_data = filtered_data[(filtered_data['Age'] >= selected_age[0]) & (filtered_data['Age'] <= selected_age[1])]
filtered_data = filtered_data[(filtered_data['Overall Rating'] >= selected_rating[0]) & (filtered_data['Overall Rating'] <= selected_rating[1])]
filtered_data = filtered_data[(filtered_data['Wage(EUR)_Avg'] >= selected_wage[0]) & (filtered_data['Wage(EUR)_Avg'] <= selected_wage[1])]

# Title
st.title('FIFA Players Dashboard')

# Display filtered data
st.write(f"### Players (Total: {filtered_data.shape[0]})")
st.dataframe(filtered_data)

# Interactive visualizations
# Age vs. Overall Rating scatter plot
st.write("### Age vs. Overall Rating")
fig1 = px.scatter(filtered_data, x='Age', y='Overall Rating', color='Nationality', hover_name='Name', title='Age vs. Overall Rating')
st.plotly_chart(fig1)

# Wage distribution across clubs
st.write("### Wage Distribution by Club")
fig2 = px.box(filtered_data, x='Club', y='Wage(EUR)_Avg', color='Club', title='Wage Distribution by Club')
st.plotly_chart(fig2)

# Top players by Overall Rating
st.write("### Top Players by Overall Rating")
top_players = filtered_data.nlargest(10, 'Overall Rating')
fig3 = px.bar(top_players, x='Name', y='Overall Rating', color='Name', title='Top 10 Players by Overall Rating')
st.plotly_chart(fig3)

# Correlation Heatmap
st.write("### Correlation Heatmap")
corr_matrix = filtered_data[['Age', 'Overall Rating', 'Potential', 'Wage(EUR)_Avg']].corr()
fig4 = px.imshow(corr_matrix, text_auto=True, title='Correlation Heatmap')
st.plotly_chart(fig4)

# Advanced: Player Comparison
st.write("### Compare Players")
players_to_compare = st.multiselect('Select Players to Compare', fifa_df['Name'])
if players_to_compare:
    comparison_data = fifa_df[fifa_df['Name'].isin(players_to_compare)]
    st.dataframe(comparison_data)
    fig5 = px.parallel_coordinates(comparison_data, dimensions=['Age', 'Overall Rating', 'Potential', 'Wage(EUR)_Avg'],
                                   color='Overall Rating', title='Player Comparison')
    st.plotly_chart(fig5)

# Advanced: Team Analysis
st.write("### Team Analysis")
selected_team = st.selectbox('Select a Team', sorted(fifa_df['Club'].unique()))
team_data = fifa_df[fifa_df['Club'] == selected_team]
if not team_data.empty:
    st.write(f"#### {selected_team} Players (Total: {team_data.shape[0]})")
    st.dataframe(team_data)
    fig6 = px.scatter(team_data, x='Age', y='Overall Rating', color='Nationality', hover_name='Name',
                      title=f'{selected_team} - Age vs. Overall Rating')
    st.plotly_chart(fig6)
    fig7 = px.box(team_data, x='Positions', y='Wage(EUR)_Avg', color='Positions', title=f'{selected_team} - Wage Distribution by Position')
    st.plotly_chart(fig7)

# Player Attribute Radar Charts
st.write("### Player Attribute Radar Chart")
player_for_radar = st.selectbox('Select a Player for Radar Chart', fifa_df['Name'])
if player_for_radar:
    radar_data = fifa_df[fifa_df['Name'] == player_for_radar].iloc[0]
    fig8 = go.Figure()
    fig8.add_trace(go.Scatterpolar(
          r=[radar_data.get('Pace', 0), radar_data.get('Shooting', 0), radar_data.get('Passing', 0), radar_data.get('Dribbling Rate', 0), radar_data.get('Defending.1', 0), radar_data.get('Physicality', 0)],
          theta=['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physicality'],
          fill='toself'
    ))
    fig8.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 100]
        )),
      showlegend=False,
      title=f'{player_for_radar} Attribute Radar Chart'
    )
    st.plotly_chart(fig8)

# Wage vs. Overall Rating
st.write("### Wage vs. Overall Rating")
fig9 = px.scatter(filtered_data, x='Wage(EUR)_Avg', y='Overall Rating', color='Nationality', hover_name='Name', title='Wage vs. Overall Rating')
st.plotly_chart(fig9)

# Player Age Distribution by Position
st.write("### Player Age Distribution by Position")
fig10 = px.violin(filtered_data, x='Positions', y='Age', color='Positions', box=True, points='all', title='Age Distribution by Position')
st.plotly_chart(fig10)

# Nationality Distribution
st.write("### Nationality Distribution")
fig11 = px.pie(filtered_data, names='Nationality', title='Nationality Distribution of Players')
st.plotly_chart(fig11)
