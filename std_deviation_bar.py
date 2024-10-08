import altair as alt
import pandas as pd

data_path = 'mc1-reports-data-cleaned.csv' 
reports_data = pd.read_csv(data_path)
reports_data['time'] = pd.to_datetime(reports_data['time'], format='%Y-%m-%d %H:%M:%S')

# Round the time to the nearest hour to group by each hour
reports_data['time'] = reports_data['time'].dt.floor('6h')

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

# Calculate the number of reports and standard deviation per hour for each location
std_dev_and_counts = melted_data.groupby(['time', 'location']).agg(
    std_dev=('intensity', 'std'),
    counts=('intensity', 'size')
).reset_index()

# Calculate the weighted average standard deviation per hour for each location
def weighted_avg(group):
    d = group['std_dev']
    weights = group['counts']
    try:
        return (d * weights).sum() / weights.sum()
    except ZeroDivisionError:
        return 0

# Apply the weighted_avg function 
weighted_std_dev_per_hour = std_dev_and_counts.groupby('location').apply(weighted_avg, include_groups=False).reset_index(name='weighted_avg_std_dev_per_hour')

# Group by location to calculate the total number of reports
total_reports_per_hour = melted_data.groupby(['time', 'location']).size().groupby('location').mean().reset_index(name='avg_reports_per_hour')

# Merge the two dataframes
merged_data = pd.merge(total_reports_per_hour, weighted_std_dev_per_hour, on='location')

# Sort merged data by weighted standard deviation for chart ordering
merged_data = merged_data.sort_values(by='weighted_avg_std_dev_per_hour', ascending=False)

# Melt the dataframe for visualization
final_data = merged_data.melt(id_vars='location', value_vars=['avg_reports_per_hour', 'weighted_avg_std_dev_per_hour'],
                              var_name='Metric', value_name='Value')

# Define scales
scale_reports = alt.Scale(domain=(0, final_data[final_data['Metric']=='avg_reports_per_hour']['Value'].max()))
scale_std_dev = alt.Scale(domain=(0, final_data[final_data['Metric']=='weighted_avg_std_dev_per_hour']['Value'].max()))

# Create the grouped bar chart
base = alt.Chart(final_data).encode(
    y=alt.Y('location:N', axis=alt.Axis(title='Location'), sort=None),
    color='Metric:N'
)

bar_reports = base.transform_filter(
    alt.datum.Metric == 'avg_reports_per_hour'
).mark_bar(opacity=0.7, color='blue').encode(
    x=alt.X('Value:Q', axis=alt.Axis(title='Average Reports per Hour'), scale=scale_reports)
)

bar_std_dev = base.transform_filter(
    alt.datum.Metric == 'weighted_avg_std_dev_per_hour'
).mark_bar(opacity=0.7, color='red').encode(
    x=alt.X('Value:Q', axis=alt.Axis(title='Weighted Average Standard Deviation per Hour'), scale=scale_std_dev)
)

# Layer the bars for grouped effect
chart = alt.layer(bar_reports, bar_std_dev).resolve_scale(
    x='independent'
).properties(
    width=700,
    height=400,
    title='Average Number of Reports and Weighted Standard Deviation by Location'
)

chart.save('std_deviation_bar.html')
