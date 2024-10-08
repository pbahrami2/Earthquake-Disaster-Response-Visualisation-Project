import altair as alt
import pandas as pd

data_path = 'mc1-reports-data-cleaned.csv'  
reports_data = pd.read_csv(data_path)
reports_data['time'] = pd.to_datetime(reports_data['time'], format='%Y-%m-%d %H:%M:%S')

# Round the time to the nearest minute
reports_data['time'] = reports_data['time'].dt.floor('min')

# Replace location numbers with names
location_names = {
    1: 'Palace Hills', 2: 'Northwest', 3: 'Old Town', 4: 'Safe Town',
    5: 'Southwest', 6: 'Downtown', 7: 'Wilson Forest', 8: 'Scenic Vista',
    9: 'Broadview', 10: 'Chapparal', 11: 'Terrapin Springs', 12: 'Pepper Mill',
    13: 'Cheddarford', 14: 'Easton', 15: 'Weston', 16: 'Southton',
    17: 'Oak Willow', 18: 'East Parton', 19: 'West Parton'
}
reports_data['location'] = reports_data['location'].map(location_names)

# Group by time and location to count the number of reports
reports_per_minute = reports_data.groupby(['time', 'location']).size().reset_index(name='reports_count')

# Create a selection element for location
options = sorted(reports_data['location'].unique())
input_dropdown = alt.binding_select(options=options)
selection = alt.selection_point(fields=['location'], bind=input_dropdown, name='Select')

chart = alt.Chart(reports_per_minute).mark_bar().encode(
    x=alt.X('time:T', axis=alt.Axis(title='Time')),
    y=alt.Y('reports_count:Q', axis=alt.Axis(title='Number of Reports per Minute')),
    tooltip=['time:T', 'location:N', 'reports_count:Q']
).properties(
    width=800,
    height=400,
    title='Number of Reports Over Time'
).add_params(
    selection
).transform_filter(
    selection
).interactive()

chart.save('report_number.html')
