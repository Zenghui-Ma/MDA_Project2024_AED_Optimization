import dash_leaflet as dl
import pandas as pd
import os
import dash

# 读取AED位置数据
def read_aed_data(file_path='data/AED_locations_ThreeCity.xlsx'):
    # 获取当前工作目录
    base_dir = os.getcwd()
    # 拼接相对路径，得到文件的绝对路径
    full_path = os.path.join(base_dir, file_path)
    # 读取Excel数据
    data = pd.read_excel(full_path)
    # 确保数据中没有空值
    data = data.dropna(subset=['latitude', 'longitude'])
    return data

# 生成AED标记
def generate_aed_markers(data):
    markers = []
    for _, row in data.iterrows():
        marker = dl.Marker(
            position=[row['latitude'], row['longitude']],
            icon={
                "iconUrl": "/assets/aed_old.png",  # 确保aed_icon.png文件位于assets文件夹中
                "iconSize": [21, 21],  # 图标大小
                "iconAnchor": [12, 41],  # 图标锚点
                "popupAnchor": [1, -34],  # 弹出框锚点
            }
        )
        markers.append(marker)
    return markers

<<<<<<< HEAD
def read_patient_data(file_path='data/citycombined_intervention_data.xlsx'):
=======
def read_patient_data(file_path='data/patients_combined.xlsx'):
>>>>>>> a77a5a4788b8c0485012dea46a31ca23c9464aeb
    # 获取当前工作目录
    base_dir = os.getcwd()
    # 拼接相对路径，得到文件的绝对路径
    full_path = os.path.join(base_dir, file_path)
    # 读取Excel数据
    data = pd.read_excel(full_path)
    # 确保数据中没有空值
    data = data.dropna(subset=['latitude', 'longitude'])
    return data


# display patients location
import dash_leaflet as dl

def generate_patient_markers(data):
    markers = []
    for _, row in data.iterrows():
        # 根据 target 列的值选择图标颜色
<<<<<<< HEAD
        if row['target'] == 0:
            icon_url = "/assets/green_person.png"  # 绿色圈的图标文件路径
        elif row['target'] == 1:
            icon_url = "/assets/red_person.png"  # 红色圈的图标文件路径
        else:
            continue  # 如果 target 不是 0 或 1，则跳过该行
=======
        if row['Mortality'] == 0:
            icon_url = "/assets/green_person.png"  # 绿色圈的图标文件路径
        elif row['Mortality'] == 1:
            icon_url = "/assets/red_person.png"  # 红色圈的图标文件路径
        else:
            continue  # 如果 Mortality 不是 0 或 1，则跳过该行
>>>>>>> a77a5a4788b8c0485012dea46a31ca23c9464aeb

        # 创建标记
        marker = dl.Marker(
            position=[row['latitude'], row['longitude']],
            icon={
                "iconUrl": icon_url,
                "iconSize": [21, 21],  # 图标大小
                "iconAnchor": [12, 41],  # 图标锚点
                "popupAnchor": [1, -34],  # 弹出框锚点
            }
        )
        markers.append(marker)
    return markers
