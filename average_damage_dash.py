import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

data_path = 'mc1-reports-data-cleaned.csv' 
reports_data = pd.read_csv(data_path)
reports_data['time'] = pd.to_datetime(reports_data['time'], format='%Y-%m-%d %H:%M:%S')
reports_data['time'] = reports_data['time'].dt.floor('h')  

# Melt the DataFrame for the stacked bar chart
melted_data = reports_data.melt(id_vars=['time', 'location'],
                                value_vars=['sewer_and_water', 'power', 'roads_and_bridges', 'medical', 'buildings', 'shake_intensity'],
                                var_name='category', value_name='value')
# Calculate average values for the stacked bar chart
avg_damage_per_category_hour = melted_data.groupby(['time', 'location', 'category']).mean().reset_index()

# Calculate report counts per minute for the bar chart
reports_per_minute = reports_data.groupby(['time', 'location']).size().reset_index(name='reports_count')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Number of Reports and Average Damage Value per Hour Over Time"),
    dcc.Dropdown(
        id='location-dropdown',
        options=[{'label': name, 'value': name} for name in sorted(reports_data['location'].unique())],
        value='All',  
        clearable=False
    ),
    dcc.Graph(id='stacked-bar-chart'),
    dcc.Graph(id='bar-chart')
], style={'backgroundColor': 'white'})  

@app.callback(
    [Output('stacked-bar-chart', 'figure'),
     Output('bar-chart', 'figure')],
    [Input('location-dropdown', 'value')]
)
def update_graphs(selected_location):
    # Filter the data for the stacked bar chart
    filtered_avg_data = avg_damage_per_category_hour[avg_damage_per_category_hour['location'] == selected_location]
    # Create the stacked bar chart
    stacked_fig = go.Figure()
    for category in filtered_avg_data['category'].unique():
        category_data = filtered_avg_data[filtered_avg_data['category'] == category]
        stacked_fig.add_trace(go.Bar(
            x=category_data['time'],
            y=category_data['value'],
            name=category
        ))
    stacked_fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        paper_bgcolor='white',
        title='Average Damage Value',
        xaxis_title='Time',
        yaxis_title='Average Damage Value',
        xaxis=dict(
            tickangle=-45,
            tickformat='%b %d %H:%M',
        ),
        legend_title='Category',
        height = 800
    )
    
    # Filter the data for the bar chart
    filtered_report_data = reports_per_minute[reports_per_minute['location'] == selected_location]
    # Create the bar chart
    bar_fig = px.bar(filtered_report_data, x='time', y='reports_count',
                     labels={'reports_count': 'Number of Reports'},
                     title='Number of Reports')
    bar_fig.update_traces(marker_color='blue', marker_line_color='blue')
    bar_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color="black",
        title_font_color="black",
        bargap=0,
        height=600,
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='black',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='black'
            ),
            tickformat='%b %d %H:%M',  
            tickvals=filtered_report_data['time'][::4]  
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=True,
            showline=True,
            showticklabels=True
        )
    )

    return stacked_fig, bar_fig

if __name__ == '__main__':
    app.run_server(debug=True)
