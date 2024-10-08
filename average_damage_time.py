import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

data_path = 'mc1-reports-data-cleaned.csv'
reports_data = pd.read_csv(data_path)
reports_data['time'] = pd.to_datetime(reports_data['time'], format='%Y-%m-%d %H:%M:%S')
location_names = {
    1: 'Palace Hills', 2: 'Northwest', 3: 'Old Town', 4: 'Safe Town',
    5: 'Southwest', 6: 'Downtown', 7: 'Wilson Forest', 8: 'Scenic Vista',
    9: 'Broadview', 10: 'Chapparal', 11: 'Terrapin Springs', 12: 'Pepper Mill',
    13: 'Cheddarford', 14: 'Easton', 15: 'Weston', 16: 'Southton',
    17: 'Oak Willow', 18: 'East Parton', 19: 'West Parton'
}
reports_data['location'] = reports_data['location'].map(location_names)

# Group by time to count reports per minute
summary_data = reports_data.groupby('time').size().reset_index(name='report_count')

app = dash.Dash(__name__)

# Define the layout of the app 
app.layout = html.Div([
    dcc.Graph(
        id='time-series-chart',
        config={'scrollZoom': True},
        figure=px.line(summary_data, x='time', y='report_count', title='Select the Time Range').update_xaxes(rangeslider_visible=True)
    ),
    dcc.Graph(id='bar-chart')
])

# Callback to update the bar chart based on selected range in the time series chart
@app.callback(
    Output('bar-chart', 'figure'),
    Input('time-series-chart', 'relayoutData')
)
def update_bar_chart(relayoutData):
    start_date = summary_data['time'].min()
    end_date = summary_data['time'].max()

    if relayoutData and 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
        start_date = pd.to_datetime(relayoutData['xaxis.range[0]'])
        end_date = pd.to_datetime(relayoutData['xaxis.range[1]'])

    filtered_data = reports_data[(reports_data['time'] >= start_date) & (reports_data['time'] <= end_date)]
    melted_data = filtered_data.melt(id_vars=['time', 'location'],
                                     value_vars=['sewer_and_water', 'power', 'roads_and_bridges', 'medical', 'buildings', 'shake_intensity'],
                                     var_name='category', value_name='value')
    grouped_data = melted_data.groupby(['location', 'category']).agg({'value': 'mean'}).reset_index()

    fig = px.bar(grouped_data, x='location', y='value', color='category',
                 labels={'value': 'Average Damage Value'}, title='Average Damage Value')
    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)