import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from layout import create_top_bar, placeholder

# Create Dash application
app = dash.Dash(__name__)

# Read Excel data
df = pd.read_excel("data/3_city_case_death.xlsx")

# Convert 'Month' column to datetime format
df['Month'] = pd.to_datetime(df['Month'], format='%Y-%m')

# Get the list of all unique cities
cities = df['City'].unique()

# Define Dash application layout
app.layout = html.Div(
    style={'fontFamily': 'Arial', 'padding': '0', 'margin': '0',
           'backgroundColor': 'rgba(245, 245, 245, 1)'},
    children=[
        # Top blue bar
        create_top_bar('AED Mortality Rate Analysis by Different Years and Cities'),
        placeholder,
    
    html.Div(
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in df['Month'].dt.year.unique()],
            value=2022  # Set the initial value to 2022
        ),
        style={'width': '200px', 'margin-top': '10px', 'margin-bottom': '20px'}  # Adjust the width and alignment of the dropdown
    ),

    html.Div(
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': city, 'value': city} for city in cities],
            value='Brussels'  # Set the initial city
        ),
        style={'width': '200px', 'margin-top': '10px', 'margin-bottom': '20px'}  # Adjust the width and alignment of the dropdown
    ),

    dcc.Graph(
        id='monthly-data-graph',
        style={'width': '80vw', 'height': '70vh'}  # Set the width and height of the graph
    )
])

# Set callback function to update the graph data based on selected year and city
@app.callback(
    Output('monthly-data-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('city-dropdown', 'value')]
)
def update_figure(selected_year, selected_city):
    # Filter data based on selected city and year
    df_filtered = df[(df['City'] == selected_city) & (df['Month'].dt.year == selected_year)]

    # Get the months, total cases, deaths, and death rates
    months = df_filtered['Month'].dt.strftime('%Y-%m').tolist()
    total_cases = df_filtered['Total Cases'].tolist()
    deaths = df_filtered['Deaths'].tolist()
    death_rates = df_filtered['Death Rate (%)'].tolist()  # Assuming 'Death Rate' column contains percentage values

    # Create the bar chart
    fig = go.Figure()

    # Add total cases bar chart
    fig.add_trace(go.Bar(
        x=months, 
        y=total_cases,
        name='Total Cases',
        marker_color='rgb(55, 83, 109)',
        text=total_cases,
        textposition='auto'
    ))

    # Add deaths bar chart
    fig.add_trace(go.Bar(
        x=months, 
        y=deaths,
        name='Deaths',
        marker_color='rgb(255, 123, 0)',
        text=deaths,
        textposition='auto'
    ))

    # Add death rate line chart with yellow color
    fig.add_trace(go.Scatter(
        x=months,
        y=death_rates,
        name='Death Rate',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='rgb(255, 205, 0)', width=3),  # Using yellow color
        marker=dict(color='rgb(255, 205, 0)', size=8, symbol='circle')  # Using the same yellow color
    ))

    # Update the layout of the chart
    fig.update_layout(
        title=f'Total Cases and Death Count in {selected_city} for {selected_year}',
        xaxis=dict(
            tickmode='array',
            tickvals=months,  # Only display month labels
            tickformat='%Y-%m'
        ),
        yaxis=dict(
            title='Count',
            titlefont=dict(size=14),
            tickfont=dict(size=12),
            gridcolor='rgba(200, 200, 200, 0.5)'
        ),
        yaxis2=dict(
            title='Death Rate (%)',
            overlaying='y',
            side='right',
            tickformat='.1f',  # Ensure the secondary y-axis shows correct format
            titlefont=dict(size=14),
            tickfont=dict(size=12),
            showgrid=False  # Hide the grid for the secondary y-axis
        ),
        barmode='group',  # Group the bar charts
        bargap=0.2,  # Adjust the gap between bars
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set chart background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
        legend=dict(
            x=1.05,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0.5)',
            borderwidth=1
        )
    )

    return fig

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
