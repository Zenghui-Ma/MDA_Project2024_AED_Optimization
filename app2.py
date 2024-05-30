import dash
from dash import Dash, html, Input, Output, dcc, callback_context, State
import dash_leaflet as dl
import json
import pandas as pd

from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

# Import self-defined function
import aed_location_existed

app = Dash(__name__,
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

# Initialize a DataFrame to store patient coordinates
initial_patients_df = pd.DataFrame(columns=['index', 'latitude', 'longitude'])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("AED Optimization for Survival", style={'text-align': 'center', 'color': '#488A99'}),
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
                                {'label': 'New Intervention', 'value': 'NEW_INTERVENTION'},
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
                dcc.Store(id='store-patients', data=initial_patients_df.to_dict('records')),
                width=12
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(id='patient-output'),
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
        ),
        dbc.Row(
            dbc.Col(
                html.Div([
                    dcc.Textarea(
                        id='textarea-patient-discription',
                        value='Textarea content initialized\nwith multiple lines of text',
                        style={'width':'100%', 'height':300},
                    ),
                    html.Div(id='textarea-patient-discription-output', style={'whiteSpace': 'pre-line'})
                    ]),
            )
        )
    ],
    fluid=True
)

# Callback to display existing AED locations
@app.callback(
    Output('map', 'children', allow_duplicate=True),
    Input('show-aed-checklist', 'value'),
    State('map', 'children'),
    prevent_initial_call='initial_duplicate'
)
def update_aed_locations(checklist_values, current_children):
    current_layers = [layer for layer in current_children if isinstance(layer, dl.TileLayer)]
    
    if 'AED' in checklist_values:
        aed_data = aed_location_existed.read_aed_data()
        aed_markers = aed_location_existed.generate_aed_markers(aed_data)
        current_layers += aed_markers
    
    return current_layers

# Callback to handle new AED locations
@app.callback(
    Output('map', 'children', allow_duplicate=True),
    Output('store-coordinates', 'data'),
    Input('map', 'clickData'),
    State('map', 'children'),
    prevent_initial_call='initial_duplicate'
)
def enable_map_clicks(click_data, current_children):
    current_layers = [layer for layer in current_children if isinstance(layer, dl.TileLayer)]
    
    if click_data:
        coordinates = click_data['latlng']
        lat, lon = coordinates.values()
        
        aed_icon = {
            "iconUrl": "/assets/aed_new.png",
            "iconSize": [50, 50],
            "iconAnchor": [25, 50],
            "popupAnchor": [1, -34],
        }
        new_marker = dl.Marker(position=[lat, lon], icon=aed_icon)
        current_layers.append(new_marker)
        return current_layers, json.dumps(coordinates)
    
    return current_layers, dash.no_update

# Callback to handle new interventions
@app.callback(
    Output('map', 'children', allow_duplicate=True),
    Output('store-patients', 'data'),
    Input('map', 'clickData'),
    Input('show-aed-checklist', 'value'),
    State('store-patients', 'data'),
    State('map', 'children'),
    prevent_initial_call='initial_duplicate'
)
def new_intervention(click_data, checklist_values, stored_patients, current_children):
    current_layers = [layer for layer in current_children if isinstance(layer, dl.TileLayer)]
    patients_df = pd.DataFrame(stored_patients)
    
    if 'NEW_INTERVENTION' in checklist_values and click_data:
        coordinates = click_data['latlng']
        lat, lon = coordinates.values()
        
        new_index = len(patients_df) + 1
        new_row = pd.DataFrame({'index': [new_index], 'latitude': [lat], 'longitude': [lon]})
        patients_df = pd.concat([patients_df, new_row], ignore_index=True)
        
        patient_marker = dl.Marker(position=[lat, lon], icon={
            "iconUrl": "/assets/patient.png",
            "iconSize": [50, 50],
            "iconAnchor": [25, 50],
            "popupAnchor": [1, -34],
        }, children=[
            dl.Popup([
                html.Div(f"Patient Location: ({lat}, {lon})")
            ])
        ])
        current_layers.append(patient_marker)
        return current_layers, patients_df.to_dict('records')
    
    if 'NEW_INTERVENTION' not in checklist_values:
        # Clear patients_df and remove markers
        patients_df = pd.DataFrame(columns=['index', 'latitude', 'longitude'])
        current_layers = [layer for layer in current_layers if not isinstance(layer, dl.Marker)]
    
    return current_layers, patients_df.to_dict('records')

# Callback to update coordinate output
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

# Callback to update patient output
@app.callback(
    Output('patient-output', 'children'),
    Input('store-patients', 'data')
)
def update_patient_output(stored_patients):
    if not stored_patients:
        return "No patients stored yet."
    df = pd.DataFrame(stored_patients)
    return html.Div([
        html.H4("Patient Coordinates"),
        dcc.Graph(
            figure={
                'data': [
                    {
                        'x': df['longitude'],
                        'y': df['latitude'],
                        'mode': 'markers',
                        'marker': {'size': 12},
                        'name': 'Latitude'
                    },
                ],
                'layout': {
                    'title': 'Patient Coordinates',
                    'xaxis': {'title': 'longitude'},
                    'yaxis': {'title': 'latitude'},
                    'height': 400,
                    'width': 6
                }
            }
        )
    ])

# Callback to update textarea output
@app.callback(
    Output('textarea-patient-discription-output', 'children'),
    Input('textarea-patient-discription', 'value')
)
def update_textarea(value):
    return ' Information about patient: \n{}'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)