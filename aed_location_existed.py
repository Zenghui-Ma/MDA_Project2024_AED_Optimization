import dash_leaflet as dl
import pandas as pd
import os

# 读取AED位置数据
def read_aed_data(file_path='data/AED_locations.xlsx'):
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
