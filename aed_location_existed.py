import dash_leaflet as dl
import pandas as pd
import os
import dash

###############################
#   AED location and marker   #
###############################

def read_aed_data(file_path='data/AED_locations_ThreeCity.xlsx'):
    # Get the current working directory
    base_dir = os.getcwd()
    # Combine relative path to get the full file path
    full_path = os.path.join(base_dir, file_path)
    # Read the Excel data
    data = pd.read_excel(full_path)
    # Ensure there are no null values in the data
    data = data.dropna(subset=['latitude', 'longitude'])
    return data

# Generate AED markers
def generate_aed_markers(data):
    markers = []
    for _, row in data.iterrows():
        marker = dl.Marker(
            position=[row['latitude'], row['longitude']],
            icon={
                "iconUrl": "/assets/aed_old.png",  # Ensure aed_icon.png is located in the assets folder
                "iconSize": [21, 21],  # Icon size
                "iconAnchor": [12, 41],  # Icon anchor point
                "popupAnchor": [1, -34],  # Popup anchor point
            }
        )
        markers.append(marker)
    return markers

<<<<<<< Updated upstream
<<<<<<< HEAD
def read_patient_data(file_path='data/citycombined_intervention_data.xlsx'):
=======
def read_patient_data(file_path='data/patients_combined.xlsx'):
>>>>>>> a77a5a4788b8c0485012dea46a31ca23c9464aeb
    # 获取当前工作目录
=======
###############################
# patient location and marker #
###############################

def read_patient_data(file_path='data/patients_combined.xlsx'):
    # Get the current working directory
>>>>>>> Stashed changes
    base_dir = os.getcwd()
    # Combine relative path to get the full file path
    full_path = os.path.join(base_dir, file_path)
    # Read the Excel data
    data = pd.read_excel(full_path)
    # Ensure there are no null values in the data
    data = data.dropna(subset=['latitude', 'longitude'])
    return data

# Generate patient markers
def generate_patient_markers(data):
    markers = []
    for _, row in data.iterrows():
<<<<<<< Updated upstream
        # 根据 target 列的值选择图标颜色
<<<<<<< HEAD
        if row['target'] == 0:
            icon_url = "/assets/green_person.png"  # 绿色圈的图标文件路径
        elif row['target'] == 1:
            icon_url = "/assets/red_person.png"  # 红色圈的图标文件路径
        else:
            continue  # 如果 target 不是 0 或 1，则跳过该行
=======
=======
        # Select icon color based on the target column value
>>>>>>> Stashed changes
        if row['Mortality'] == 0:
            icon_url = "/assets/green_person.png"  # Path to green icon
        elif row['Mortality'] == 1:
            icon_url = "/assets/red_person.png"  # Path to red icon
        else:
<<<<<<< Updated upstream
            continue  # 如果 Mortality 不是 0 或 1，则跳过该行
>>>>>>> a77a5a4788b8c0485012dea46a31ca23c9464aeb
=======
            continue  # Skip if Mortality is not 0 or 1
>>>>>>> Stashed changes

        # Create marker
        marker = dl.Marker(
            position=[row['latitude'], row['longitude']],
            icon={
                "iconUrl": icon_url,
                "iconSize": [21, 21],  # Icon size
                "iconAnchor": [12, 41],  # Icon anchor point
                "popupAnchor": [1, -34],  # Popup anchor point
            }
        )
        markers.append(marker)
    return markers

###############################
## hospital location marker  ##
###############################

# Read hospital location data
def read_hospital_data(file_path='data/hospitals.xlsx'):
    # Get the current working directory
    base_dir = os.getcwd()
    # Combine relative path to get the full file path
    full_path = os.path.join(base_dir, file_path)
    # Read the Excel data
    data = pd.read_excel(full_path)
    # Ensure there are no null values in the data
    data = data.dropna(subset=['latitude', 'longitude'])
    return data

# Generate hospital markers
def generate_hospital_markers(data):
    markers = []
    for _, row in data.iterrows():
        marker = dl.Marker(
            position=[row['latitude'], row['longitude']],
            icon={
                "iconUrl": "/assets/hospital.png",  # Ensure hospital.png is located in the assets folder
                "iconSize": [21, 21],  # Icon size
                "iconAnchor": [12, 41],  # Icon anchor point
                "popupAnchor": [1, -34],  # Popup anchor point
            }
        )
        markers.append(marker)
    return markers
