import dash
from dash import Dash, html, Input, Output, dcc, callback_context, State
import dash_leaflet as dl
import json
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Import self-defined function
import aed_location_existed

app = Dash(__name__,
           external_stylesheets=[dbc.themes.VAPOR],  # set the theme of the project
           title='MDA Project-AED Location Optimization',
           use_pages=True,
           suppress_callback_exceptions=True)
server = app.server

# Initialize months for the slider
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

# Set layout
app.layout = dbc.Container(
    [
        # 1 Set the title of the project
        dbc.Row(
            dbc.Col(
                html.H1("AED Optimization for better Survival", style={'text-align': 'center', 'color': 'white'}),
                width=12
            )
        ),
        # 2.
        dbc.Row(
            [
                dbc.Col(
                    dl.Map(
                        id='map',
                        children=[dl.TileLayer()],
                        center=[50.8503, 4.3517],
                        zoom=12.5,
                        style={'width': '100%', 'height': '80vh'}
                    ),
                    width=6
                ),
                dbc.Col(
                    html.Div(
                        dcc.Checklist(
                            options=[
                                {'label': 'Existing AED Locations', 'value': 'AED'},
                                {'label': 'Patients', 'value': 'patient'},
                                {'label': 'New AED Placement', 'value': 'newAED'},
                            ],
                            value=[],
                            id='show-aed-hospital-checklist',
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
        # 3 存储坐标值
        dbc.Row(
            dbc.Col(
                dcc.Store(id='store-coordinates'),
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
        # 4 slide bar
        dbc.Row(
            dbc.Col(
                html.Div([
                    dcc.Textarea(
                        id='textarea-patient-discription',
                        value='Textarea content initialized\nwith multiple lines of text',
                        style={'width': '100%', 'height': 300},
                    ),
                    html.Div(id='textarea-patient-discription-output', style={'whiteSpace': 'pre-line'})
                ]),
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Store(id='store-coordinates', data=[]),
                width=12
            )
        )
    ],
    fluid=False
)

# Callback to display existing AED locations and handle new AED placements
@app.callback(
    Output('map', 'children'),
    Output('store-coordinates', 'data'),  # 对应回调函数stored_chidren
    Input('map', 'clickData'),  # 对应函数里的click_data,传递到函数里
    Input('show-aed-hospital-checklist', 'value'),
    State('store-coordinates', 'data'),
    prevent_initial_call=True
)
def update_aed_locations(click_data, checklist_values, stored_coordinates):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    base_layers = [dl.TileLayer()]

    # Display existing AED locations if the checklist value is selected
    if 'AED' in checklist_values:
        aed_data = aed_location_existed.read_aed_data()
        aed_markers = aed_location_existed.generate_aed_markers(aed_data)
        base_layers += aed_markers
    if 'patient' in checklist_values:
        patient_data =aed_location_existed.read_patient_data()
        aed_markers = aed_location_existed.generate_patient_markers(patient_data)
        base_layers += aed_markers

    # Add new AED location if map is clicked and 'newAED' is selected
    if triggered_id == 'map' and click_data and 'newAED' in checklist_values:
        coordinates = click_data['latlng']
        lat, lon = coordinates['lat'], coordinates['lng']
        print("New location of AED is", lat, lon)

        aed_icon = {
            "iconUrl": "/assets/aed_new.png",
            "iconSize": [50, 50],
            "iconAnchor": [25, 50],
            "popupAnchor": [1, -34],
        }
        new_marker = dl.Marker(position=[lat, lon], icon=aed_icon)
        stored_coordinates.append({'lat': lat, 'lng': lon})
        base_layers.append(new_marker)

    # Add previously stored coordinates for new AED locations
    if 'newAED' in checklist_values:
        for coord in stored_coordinates:
            new_marker = dl.Marker(position=[coord['lat'], coord['lng']], icon={
                "iconUrl": "/assets/aed_new.png",
                "iconSize": [50, 50],
                "iconAnchor": [25, 50],
                "popupAnchor": [1, -34],
            })
            base_layers.append(new_marker)
    else:
        # Clear stored coordinates when 'newAED' is unchecked
        stored_coordinates = []

    return base_layers, stored_coordinates

if __name__ == '__main__':
    app.run_server(debug=True)
