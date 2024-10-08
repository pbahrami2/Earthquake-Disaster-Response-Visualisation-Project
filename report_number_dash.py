import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

data_path = 'mc1-reports-data-cleaned.csv'  
reports_data = pd.read_csv(data_path)
reports_data['time'] = pd.to_datetime(reports_data['time'], format='%Y-%m-%d %H:%M:%S')
reports_data['time'] = reports_data['time'].dt.floor('min')

location_names = {
    1: 'Palace Hills', 2: 'Northwest', 3: 'Old Town', 4: 'Safe Town',
    5: 'Southwest', 6: 'Downtown', 7: 'Wilson Forest', 8: 'Scenic Vista',
    9: 'Broadview', 10: 'Chapparal', 11: 'Terrapin Springs', 12: 'Pepper Mill',
    13: 'Cheddarford', 14: 'Easton', 15: 'Weston', 16: 'Southton',
    17: 'Oak Willow', 18: 'East Parton', 19: 'West Parton'
}
reports_data['location'] = reports_data['location'].map(location_names)
reports_per_minute = reports_data.groupby(['time', 'location']).size().reset_index(name='reports_count')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Number of Reports"),
    dcc.Dropdown(
        id='location-dropdown',
        options=[{'label': name, 'value': name} for name in sorted(reports_data['location'].unique())],
        value='All',  
        clearable=False
    ),
    dcc.Graph(id='bar-chart')
], style={'backgroundColor': 'white'})  

# Callback to update the bar chart based on selected location
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('location-dropdown', 'value')]
)
def update_bar_chart(selected_location):
    filtered_data = reports_per_minute[reports_per_minute['location'] == selected_location]
    fig = px.bar(filtered_data, x='time', y='reports_count',
                 labels={'reports_count': 'Number of Reports per Minute'},
                 title='Number of Reports per Minute')

    # Customize the chart colors
    fig.update_traces(marker_color='blue', marker_line_color='blue')  # Set bar fill and line color to blue
    fig.update_layout(
        plot_bgcolor='white',  # White background inside the plot
        paper_bgcolor='white',  # White background color outside the plot
        font_color="black",  # Font color set to black for contrast
        title_font_color="black",  # Title color set to black
        bargap=0,  # Remove gaps between bars
        height=600,  # Increase the height of the chart
        xaxis=dict(
            showline=True,  # Show the x-axis line
            showgrid=True,  # Show the gridlines
            showticklabels=True,  # Show the tick labels
            linecolor='black',  # x-axis line color
            linewidth=2,  # x-axis line width
            ticks='outside',  # Position ticks to outside
            tickfont=dict(
                family='Arial',
                size=12,
                color='black'
            ),
        ),
        yaxis=dict(
            showgrid=True,  # Show Y-axis gridlines
            zeroline=True,  # Show the zero line
            showline=True,  # Show Y-axis line
            showticklabels=True  # Show Y-axis tick labels
        )
    )
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
