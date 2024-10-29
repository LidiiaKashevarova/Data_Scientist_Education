import streamlit as st
import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('education_costs_db.sqlite')

# Reading tables
region_df = pd.read_sql('SELECT * FROM region', conn)
school_gymnasium_results_df = pd.read_sql('SELECT * FROM school_gymnasium_results', conn)
grundskola_costs_forecast_df = pd.read_sql('SELECT * FROM grundskola_costs_forecast', conn)
gymnasieskola_costs_forecast_df = pd.read_sql('SELECT * FROM gymnasieskola_costs_forecast', conn)
cost_region_grundskola_df = pd.read_sql('SELECT * FROM Cost_region_grundskola_forecast_2025_2035', conn)
cost_region_gymnasieskola_df = pd.read_sql('SELECT * FROM Cost_region_gymnasieskola_forecast_2025_2035', conn)

# Select region
region_choice = st.selectbox("Välj region:", region_df['Name_Region'].unique())
selected_region = region_df[region_df['Name_Region'] == region_choice]['Region'].values[0]

# Choice of the year
year_choice = st.selectbox("Välj år:", list(range(2025, 2036)))

# 1. Antal barn i grundskola
st.subheader(f"Antal elever i Grundskola i {region_choice}, {year_choice} år")
filtered_school_data = school_gymnasium_results_df[(school_gymnasium_results_df['Region'] == selected_region) & (school_gymnasium_results_df['year'] == year_choice)]

# Sum up the number of students in all classes
antal_barn_grundskola = filtered_school_data[['F_school', '1_school', '2_school', '3_school', '4_school', '5_school', '6_school', '7_school', '8_school', '9_school']].sum(axis=1).values[0]
st.write(f"Totalt antal elever i Grundskola: {antal_barn_grundskola}")

# Display the number of students by class
st.write("Antal elever per klass:")
for klass, num in zip(['Klass F', 'Klass 1', 'Klass 2', 'Klass 3', 'Klass 4', 'Klass 5', 'Klass 6', 'Klass 7', 'Klass 8', 'Klass 9'],
                      filtered_school_data[['F_school', '1_school', '2_school', '3_school', '4_school', '5_school', '6_school', '7_school', '8_school', '9_school']].values[0]):
    st.write(f"{klass}: {num}")

# 2. Kostnad i grundskola
st.subheader(f"Kostnad i Grundskola i {region_choice}, {year_choice} år")

# Get the cost per student from the table grundskola_costs_forecast
cost_per_child_fixed = grundskola_costs_forecast_df[
    (grundskola_costs_forecast_df['Year'] == year_choice)
]['Predicted_Fixed_Cost_per_child_kr'].values[0]

cost_per_child_current = grundskola_costs_forecast_df[
    (grundskola_costs_forecast_df['Year'] == year_choice)
]['Predicted_Current_Cost_per_child_kr'].values[0]

# Get total costs in a region based on the selected region and year
total_cost_region = cost_region_grundskola_df[
    (cost_region_grundskola_df['Region'] == selected_region) & 
    (cost_region_grundskola_df['Year'] == year_choice)
][['Predicted_Fixed_Cost', 'Predicted_Current_Cost']]

# Output of cost per student
st.write(f"Kostnad per elev (fast pris): {cost_per_child_fixed} kr")
st.write(f"Kostnad per elev (löpande pris): {cost_per_child_current} kr")

# Output of the total cost in the region
st.write(f"Total kostnad i regionen (fast pris): {total_cost_region['Predicted_Fixed_Cost'].values[0]} kr")
st.write(f"Total kostnad i regionen (löpande pris): {total_cost_region['Predicted_Current_Cost'].values[0]} kr")

# 3. Antal barn i gymnasium
st.subheader(f"Antal elever i Gymnasium i {region_choice}, {year_choice} år")

# Filtered gymnasium data
filtered_gymnasium_data = filtered_school_data[['1_gymnasium', '2_gymnasium', '3__gymnasium']]

# Sum up the number of students in gymnasium classes
antal_barn_gymnasium = filtered_gymnasium_data.sum(axis=1).values[0]

st.write(f"Totalt antal elever i Gymnasium: {antal_barn_gymnasium}")

# Display the number of students by course
st.write("Antal elever per kurs:")
for kurs, num in zip(['Kurs 1', 'Kurs 2', 'Kurs 3'],
                     filtered_gymnasium_data.values[0]):
    st.write(f"{kurs}: {num}")

# 4. Kostnad i gymnasium
st.subheader(f"Kostnad i Gymnasium i {region_choice}, {year_choice} år")

# Getting the cost per student from the table gymnasieskola_costs_forecast
cost_per_child_fixed_gymnasium = gymnasieskola_costs_forecast_df[
    (gymnasieskola_costs_forecast_df['Year'] == year_choice)
]['Predicted_Fixed_Cost_per_child_kr'].values[0]

cost_per_child_current_gymnasium = gymnasieskola_costs_forecast_df[
    (gymnasieskola_costs_forecast_df['Year'] == year_choice)
]['Predicted_Current_Cost_per_child_kr'].values[0]

# Get total costs in a region based on the selected region and year
total_cost_region_gymnasium = cost_region_gymnasieskola_df[
    (cost_region_gymnasieskola_df['Region'] == selected_region) & 
    (cost_region_gymnasieskola_df['Year'] == year_choice)
][['Predicted_Fixed_Cost', 'Predicted_Current_Cost']]

# Output of cost per student
st.write(f"Kostnad per elev (fast pris): {cost_per_child_fixed_gymnasium} kr")
st.write(f"Kostnad per elev (löpande pris): {cost_per_child_current_gymnasium} kr")

# Output of the total cost in the region
st.write(f"Total kostnad i regionen (fast pris): {total_cost_region_gymnasium['Predicted_Fixed_Cost'].values[0]} kr")
st.write(f"Total kostnad i regionen (löpande pris): {total_cost_region_gymnasium['Predicted_Current_Cost'].values[0]} kr")

conn.close()