import dash
from dash import Dash, html, Input, Output, dcc, callback_context, State
import dash_leaflet as dl
import json
import pandas as pd
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import joblib

# Import self-defined function
import aed_location_existed
from update_survival_probabilities import update_distance_to_aed, update_patient_survival_probabilities, generate_patient_tooltips_with_probability, model
from layout import create_top_bar, placeholder

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],  # set the theme of the project
           title='MDA Project-AED Location Optimization',
           use_pages=True,
           pages_folder="",  # 禁用 pages 文件夹
           suppress_callback_exceptions=True)
server = app.server

# Initialize a DataFrame to store patient coordinates
initial_patients_df = pd.DataFrame(columns=['index', 'latitude', 'longitude'])

# Set layout
# 定义应用的布局
app.layout = dbc.Container(
    [
        # 调用 create_top_bar 函数
        create_top_bar('AED Optimization for Better Survival'),
        placeholder,

        # 2. Main content with map and sidebar
        dbc.Row(
            [
                dbc.Col(
                    dl.Map(
                        id='map',
                        children=[dl.TileLayer()],
                        center=[50.8503, 4.3517],
                        zoom=12.5,
                        style={'width': '100%', 'height': '90vh'}
                    ),
                    width=9,
                    style={'padding-left': '10px', 'padding-right': '0',
                           'margin-top': '5px',}  # 调整左侧和右侧内边距
                ),
                dbc.Col(
                    html.Div(
                        [
                            dcc.Checklist(
                                options=[
                                    {'label': '  Existing AED Locations', 'value': 'AED'},
                                    {'label': '  Patients', 'value': 'patient'},
                                    {'label': '  Hospitals', 'value': 'hospital'},
                                    {'label': '  New AED Placement', 'value': 'newAED'},
                                ],
                                value=[],
                                id='show-aed-hospital-checklist',
                                style={
                                    'color': '#1C4E80',  # Change text color
                                    'fontSize': '20px',  # Change font size
                                    'fontFamily': 'Arial',  # Change font family
                                    'margin-top': '10px',
                                    'margin-bottom': '40px',
                                    'padding-left': '10px',
                                    'line-height': '2.5'
                                },
                                inputStyle={
                                    'margin-right': '10px',  # Add space between checkbox and label
                                    'transform': 'scale(1.4)'  # Make checkboxes larger
                                }
                            ),
                            html.Div(
                                dcc.Textarea(
                                    id='textarea-patient-description',
                                    value='Text Area: \n If you add new AED on the map, there will be the accurate postion',
                                    style={
                                        'width': '100%', 
                                        'height': '780px',
                                        'color': '#1C4E80',  # Match text color
                                        'fontSize': '18px',  # Match font size
                                        'fontFamily': 'Arial',  # Match font family
                                        'border-radius': '10px',
                                        'padding': '10px',
                                    },
                                ),
                                style={'margin-top': '20px'}
                            ),
                            html.Div(id='textarea-patient-discription-output', style={'whiteSpace': 'pre-line'})
                        ],
                        style={
                            'margin-bottom': '5px',
                            'background-color': 'rgba(245, 245, 245, 1)',
                            'padding': '10px',
                            'border-radius': '10px',
                            'height': '90vh',
                            'overflow-y': 'auto'
                        }
                    ),
                    width=3,
                    style={'padding-right': '20px', 'margin-top': '5px'}  # 调整右侧内边距和外边距
                )
            ]
        ),
        # 存储坐标值
        dbc.Row(
            dbc.Col(
                dcc.Store(id='store-coordinates'),
                width=12,
                style={'position': 'relative', 'z-index': '1'}
            )
        )
    ],
    fluid=True
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

    # 如果 stored_coordinates 是 None，则初始化为空列表
    if stored_coordinates is None:
        stored_coordinates = []

    # Display existing AED locations if the checklist value is selected
    if 'AED' in checklist_values:
        aed_data = aed_location_existed.read_aed_data()
        aed_markers = aed_location_existed.generate_aed_markers(aed_data)
        base_layers += aed_markers

    if 'patient' in checklist_values:
        patient_data =aed_location_existed.read_patient_data()
        aed_markers = aed_location_existed.generate_patient_markers(patient_data)
        base_layers += aed_markers

    if 'hospital' in checklist_values:
        patient_data =aed_location_existed.read_hospital_data()
        aed_markers = aed_location_existed.generate_hospital_markers(patient_data)
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


    # 重新计算所有患者的生存概率
    if 'newAED' in checklist_values and stored_coordinates:
        # 获取所有 AED 位置
        aed_locations = [(coord['lat'], coord['lng']) for coord in stored_coordinates]
        patients_df = aed_location_existed.read_patient_data()  # 加载患者数据
        
        # 更新患者的 distance_to_aed 列
        patients_df = update_distance_to_aed(patients_df, aed_locations)

        # 计算患者的生存概率
        patients_df = update_patient_survival_probabilities(patients_df, model)

        # 添加或更新患者的 Tooltip 到地图上
        patient_tooltips = generate_patient_tooltips_with_probability(patients_df)
        for lat, lon, tooltip in patient_tooltips:
            for marker in base_layers:
                if isinstance(marker, dl.Marker) and marker.position == [lat, lon]:
                    if marker.children is None:
                        marker.children = []
                    marker.children.append(tooltip)
                    break


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


@app.callback(
    Output('textarea-patient-description', 'value'),
    Input('store-coordinates', 'data'),
    prevent_initial_call=True
)
def update_textarea_content(stored_coordinates):
    if not stored_coordinates:
        raise PreventUpdate

    description = "New AED Locations:\n"
    for i, coord in enumerate(stored_coordinates):
        description += f"{i + 1}. Latitude: {coord['lat']}, Longitude: {coord['lng']}\n"

    return description







if __name__ == '__main__':
    app.run_server(debug=True)
