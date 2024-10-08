import altair as alt
import pandas as pd

data_path = 'mc1-reports-data-cleaned.csv'  
reports_data = pd.read_csv(data_path)
reports_data['time'] = pd.to_datetime(reports_data['time'], format='%Y-%m-%d %H:%M:%S')

# Round the time to the nearest hour to group by each hour
reports_data['time'] = reports_data['time'].dt.floor('h')

# Replace location numbers with names
location_names = {
    1: 'Palace Hills', 2: 'Northwest', 3: 'Old Town', 4: 'Safe Town',
    5: 'Southwest', 6: 'Downtown', 7: 'Wilson Forest', 8: 'Scenic Vista',
    9: 'Broadview', 10: 'Chapparal', 11: 'Terrapin Springs', 12: 'Pepper Mill',
    13: 'Cheddarford', 14: 'Easton', 15: 'Weston', 16: 'Southton',
    17: 'Oak Willow', 18: 'East Parton', 19: 'West Parton'
}
reports_data['location'] = reports_data['location'].map(location_names)

# Melt the DataFrame to have category, time, and value
melted_data = reports_data.melt(id_vars=['time', 'location'], 
                                value_vars=['sewer_and_water', 'power', 'roads_and_bridges', 'medical', 'buildings', 'shake_intensity'],
                                var_name='category', value_name='value')

# Calculate the average damage value for each category and hour
avg_damage_per_category_hour = melted_data.groupby(['time', 'location', 'category']).mean().reset_index()

# Create a selection element for location
input_dropdown = alt.binding_select(options=sorted(avg_damage_per_category_hour['location'].unique()))
location_selection = alt.selection_point(fields=['location'], bind=input_dropdown, name='Select')

# Create a selection for the legend
legend_selection = alt.selection_point(fields=['category'], bind='legend')

# Define the stacked area chart with interactive legend
stacked_area_chart = alt.Chart(avg_damage_per_category_hour).mark_area().encode(
    x='time:T',
    y=alt.Y('value:Q', stack='zero', axis=alt.Axis(title='Average Damage Value')),
    color=alt.Color('category:N', legend=alt.Legend(title="Category")),
    opacity=alt.condition(legend_selection, alt.value(1), alt.value(0.2)),
    tooltip=['time:T', 'location:N', 'category:N', 'value:Q']
).add_params(
    location_selection,
    legend_selection
).transform_filter(
    location_selection  # Filter by the location selection
).properties(
    width=800,
    height=500,
    title='Average Damage Value Area Chart'
)

stacked_area_chart.save('average_damage_area.html')
 