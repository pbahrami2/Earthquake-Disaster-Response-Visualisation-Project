import altair as alt
import pandas as pd

# Mapping of location numbers to names
location_names = {
    1: 'Palace Hills', 2: 'Northwest', 3: 'Old Town', 4: 'Safe Town',
    5: 'Southwest', 6: 'Downtown', 7: 'Wilson Forest', 8: 'Scenic Vista',
    9: 'Broadview', 10: 'Chapparal', 11: 'Terrapin Springs', 12: 'Pepper Mill',
    13: 'Cheddarford', 14: 'Easton', 15: 'Weston', 16: 'Southton',
    17: 'Oak Willow', 18: 'East Parton', 19: 'West Parton'
}

data_path = 'mc1-reports-data-cleaned.csv'  
reports_data = pd.read_csv(data_path)
reports_data['time'] = pd.to_datetime(reports_data['time'], format='%Y-%m-%d %H:%M:%S')

# Replace location numbers with names
reports_data['location'] = reports_data['location'].map(location_names)

# Melting the DataFrame to have category, time, and intensity 
melted_data = reports_data.melt(id_vars=['time', 'location'], 
                                value_vars=['sewer_and_water', 'power', 'roads_and_bridges', 'medical', 'buildings', 'shake_intensity'],
                                var_name='category', value_name='intensity')

# Group by the exact timestamp, location, and category, then calculate the average intensity
avg_intensity_time = melted_data.groupby(['time', 'location', 'category']).agg(
    avg_intensity=('intensity', 'mean')
).reset_index()

# Group by the exact timestamp and location to calculate the total number of reports
total_reports_time = melted_data.groupby(['time', 'location']).size().reset_index(name='total_reports')

# Merge the average intensity and total reports dataframes on time and location
merged_data = pd.merge(avg_intensity_time, total_reports_time, on=['time', 'location'])

# Create a selection element for location
options = [location_names[key] for key in sorted(location_names)]
input_dropdown = alt.binding_select(options=options)
selection = alt.selection_point(fields=['location'], bind=input_dropdown, name='Select')

leselection = alt.selection_point(fields=['category'], bind='legend')

chart = alt.Chart(merged_data).mark_circle().encode(
    alt.X('time:T', axis=alt.Axis(title='Time')),
    alt.Y('avg_intensity:Q', axis=alt.Axis(title='Average Damage Value')),
    size='total_reports:Q',
    color=alt.condition(leselection, 'category:N', alt.value('rgba(0,0,0,0.07)')),
    tooltip=['time:T', 'location:O', 'category:N', 'avg_intensity:Q', 'total_reports:Q']
).properties(
    width=800,
    height=400,
    title='Average Damage Reports Over Time'
).add_params(
    selection
).transform_filter(
    selection
).add_params(
    leselection
).interactive()

chart.save('overview.html')
