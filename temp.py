##############################################################################################################
###############This callback is only about to display the existing Intervention distribution.#################

@app.callback(
    Output('map', 'children'),
    Output('store-coordinates', 'data'),
    Output('store-map-children', 'data'),
    Output('store-patients', 'data'),
    Input('map', 'clickData'),
    Input('show-aed-checklist', 'value'),
    State('store-map-children', 'data'),
    State('store-patients', 'data'),
    prevent_initial_call=True
)

def update_map(click_data, checklist_values, stored_children, stored_patients):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    current_children = [dl.TileLayer()]

    if 'AED' in checklist_values:
        aed_data = aed_location_existed.read_aed_data()
        aed_markers = aed_location_existed.generate_aed_markers(aed_data)
        current_children += aed_markers

    if 'CLICK' in checklist_values:
        current_children += stored_children

    patients_df = pd.DataFrame(stored_patients)

    if 'NEW_INTERVENTION' in checklist_values:
        if triggered_id == 'map' and click_data:
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
            current_children.append(patient_marker)
        else:
            # 保留之前的标记
            for _, row in patients_df.iterrows():
                patient_marker = dl.Marker(position=[row['latitude'], row['longitude']], icon={
                    "iconUrl": "/assets/patient.png",
                    "iconSize": [50, 50],
                    "iconAnchor": [25, 50],
                    "popupAnchor": [1, -34],
                }, children=[
                    dl.Popup([
                        html.Div(f"Patient Location: ({row['latitude']}, {row['longitude']})")
                    ])
                ])
                current_children.append(patient_marker)
        return current_children, dash.no_update, dash.no_update, patients_df.to_dict('records')

    if 'NEW_INTERVENTION' not in checklist_values:
        # 清空 patients_df 并清除地图上的标记
        patients_df = initial_patients_df
        current_children = [dl.TileLayer()]

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
        return current_children, json.dumps(coordinates), current_children, patients_df.to_dict('records')

    return current_children, dash.no_update, stored_children, patients_df.to_dict('records')
