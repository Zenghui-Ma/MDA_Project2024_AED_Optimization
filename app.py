import dash
from dash import Dash, html, Input, Output, dcc, callback_context, State
import dash_leaflet as dl
import json
import pandas as pd

from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

# Import self-defined function
import aed_location_existed

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.VAPOR],
                title='MDA Project-AED Location Optimization',
                use_pages=True,
                suppress_callback_exceptions=True)
server = app.server

months = [
    "2022-06", "2022-07", "2022-08", "2022-09", "2022-10",
    "2022-11", "2022-12", "2023-01", "2023-02", "2023-03",
    "2023-04", "2023-05"
]
marks = {i: month for i, month in enumerate(months)}

# Define CSS styles for the slider marks
mark_style = {
    'color': '#488A99',  # Change the mark color
    'fontSize': '16px',  # Change the mark font size
    'fontFamily': 'Gill Sans, sans-serif',  # Change the mark font family
}

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("AED Optimization for Survival", style={'text-align': 'center', 'color': 'white'}),
                width=12
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dl.Map(
                        id='map',
                        children=[dl.TileLayer()],
                        center=[50.8503, 4.3517],
                        zoom=12.5,
                        style={'width': '100%', 'height': '60vh'}
                    ),
                    width=6
                ),
                dbc.Col(
                    html.Div(
                        dcc.Checklist(
                            options=[
                                {'label': 'Show AED Locations', 'value': 'AED'},
                                {'label': 'Enable Map Clicks', 'value': 'CLICK'},
                            ],
                            value=[],
                            id='show-aed-checklist',
                            style={
                                'color': '#488A99',  # Change text color
                                'fontSize': '18px',  # Change font size
                                'fontFamily': 'Gill Sans, sans-serif',  # Change font family
                            }
                        ),
                        style={
                            'display': 'flex',
                            'flexDirection': 'column',
                            'alignItems': 'flex-start',
                            'padding': '10px',  # Add padding for better spacing
                            'height': '60vh'  # Make the height same as the map
                        }
                    ),
                    width=4
                ),
            ],
            justify='start',  # Align to the left
            align='start'  # Align items at the start vertically
        ),
        dbc.Row(
            dbc.Col(
                html.Div(id='out'),
                width=12
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Store(id='store-coordinates'),
                width=12
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Store(id='store-map-children', data=[]),
                width=12
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(id='another-output'),
                width=12
            )
        ),
        
        dbc.Row(
            dbc.Col(
                html.Div(
                    dcc.Slider(
                        min=0,
                        max=len(months) - 1,
                        step=1,
                        value=0,
                        marks={i: {'label': month, 'style': mark_style} for i, month in enumerate(months)},
                        included=True,
                        updatemode='drag',
                        vertical=False
                    ),
                    style={'width': '60%'}
                ),
                width=12
            )
        )
    ],
    fluid=True
)

@app.callback(
    Output('map', 'children'),
    Output('store-coordinates', 'data'),
    Output('store-map-children', 'data'),
    Input('map', 'clickData'),
    Input('show-aed-checklist', 'value'),
    State('store-map-children', 'data'),
    prevent_initial_call=True
)
def update_map(click_data, checklist_values, stored_children):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    current_children = [dl.TileLayer()]

    if 'AED' in checklist_values:
        aed_data = aed_location_existed.read_aed_data()
        aed_markers = aed_location_existed.generate_aed_markers(aed_data)
        current_children += aed_markers

    if 'CLICK' in checklist_values:
        current_children += stored_children

    if triggered_id == 'map' and click_data and 'CLICK' in checklist_values:
        coordinates = click_data['latlng']
        lat, lon = coordinates.values()
        print("New location of AED is", lat, lon)

        aed_icon = {
            "iconUrl": "/assets/aed_new.png",
            "iconSize": [50, 50],
            "iconAnchor": [25, 50],
            "popupAnchor": [1, -34],
        }
        new_marker = dl.Marker(position=[lat, lon], icon=aed_icon)
        current_children.append(new_marker)
        return current_children, json.dumps(coordinates), current_children

    return current_children, dash.no_update, stored_children

@app.callback(
    Output('another-output', 'children'),
    Input('store-coordinates', 'data')
)
def use_coordinates(data):
    if data is None:
        return "No coordinates stored yet."
    data = json.loads(data) if isinstance(data, str) else data
    lat, lon = data['lat'], data['lon']
    return f"Stored coordinates: Latitude {lat}, Longitude {lon}"

if __name__ == '__main__':
    app.run_server(debug=True)
