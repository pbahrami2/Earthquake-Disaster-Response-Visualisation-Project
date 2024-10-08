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

# Melting the DataFrame to have category, time, and intensity
melted_data = reports_data.melt(id_vars=['time', 'location'], 
                                value_vars=['sewer_and_water', 'power', 'roads_and_bridges', 'medical', 'buildings', 'shake_intensity'],
                                var_name='category', value_name='intensity')

melted_data.dropna(subset=['intensity'], inplace=True)

# Group by the exact timestamp, location, and category, then calculate the standard deviation
std_dev_intensity_time = melted_data.groupby(['time', 'location', 'category']).agg(
    std_dev_intensity=('intensity', 'std')
).reset_index()

# Group by the exact timestamp and location to calculate the total number of reports
total_reports_time = melted_data.groupby(['time', 'location']).size().reset_index(name='total_reports')

# Merge the standard deviation and total reports dataframes on time and location
merged_data_std = pd.merge(std_dev_intensity_time, total_reports_time, on=['time', 'location'])

# Create a selection element for location
options = [location_names[key] for key in sorted(location_names)]
input_dropdown = alt.binding_select(options=options)
selection = alt.selection_point(fields=['location'], bind=input_dropdown, name='Select')

leselection = alt.selection_point(fields=['category'], bind='legend')

chart_std_dev = alt.Chart(merged_data_std).mark_circle().encode(
    alt.X('time:T', axis=alt.Axis(title='Time')),
    alt.Y('std_dev_intensity:Q', axis=alt.Axis(title='Standard Deviation of Damage Value')),
    size=alt.Size('total_reports:Q', legend=alt.Legend(title="Total Reports")),
    color=alt.condition(leselection, 'category:N', alt.value('rgba(0,0,0,0.07)')),
    tooltip=['time:T', 'location:N', 'category:N', 'std_dev_intensity:Q', 'total_reports:Q']
).properties(
    width=800,
    height=400,
    title='Standard Deviation of Reports Over Time'
).add_params(
    selection,
    leselection
).transform_filter(
    selection
).interactive()

chart_std_dev.save('std_deviation_perhour.html')
