import pandas as pd
import numpy as np
from geopy.distance import geodesic
from sklearn.neighbors import BallTree
import googlemaps

# 使用你的Google Maps API密钥
api_key = 'AIzaSyAaMgtqAAp07HTqibk9KlYkHIfHYK2sutc'
gmaps = googlemaps.Client(key=api_key)

# 导入医院和AED数据
hospitals = pd.read_excel('data/hospitals.xlsx')
aed_all = pd.read_excel('data/AED_locations.xlsx')
aed_data = aed_all[['id', 'full_address', 'latitude', 'longitude', 'public']]
aed_data.dropna(axis=0, inplace=True)
public_aed = aed_data[aed_data['public'] == 'yes']

# 计算救护中心和AED的直线距离
centers_coords = np.radians(hospitals[['latitude', 'longitude']])
tree_centers = BallTree(centers_coords, metric='haversine')
aed_coords = np.radians(public_aed[['latitude', 'longitude']])
tree_aed = BallTree(aed_coords, metric='haversine')

# 定义函数以计算步行距离和寻找最近的急救中心和 AED
def get_walking_distance(patient_location, center_location):
    try:
        result = gmaps.distance_matrix(origins=[patient_location],
                                       destinations=[center_location],
                                       mode="walking")
        if result['rows'][0]['elements'][0]['status'] == 'OK':
            distance = result['rows'][0]['elements'][0]['distance']['value']  # 距离以米为单位
            return distance
        else:
            print(f"Error in Google Maps API response: {result['rows'][0]['elements'][0]['status']}")
            return float('inf')
    except Exception as e:
        print(f"Exception occurred: {e}")
        return float('inf')

def find_nearest_center(patient):
    patient_location = (patient['latitude'], patient['longitude'])
    patient_index = patient.name  # 使用index来代替name
    
    # 计算步行距离到最近的急救中心
    nearest_centers = indices_centers[patient_index]  # 获取直线距离最近的急救中心索引
    walking_distances_centers = []
    for center_index in nearest_centers:
        center = hospitals.iloc[center_index]
        center_location = (center['latitude'], center['longitude'])
        distance = get_walking_distance(patient_location, center_location)
        walking_distances_centers.append((distance, center['full_address']))
    min_distance_center, nearest_center_name = min(walking_distances_centers, key=lambda x: x[0])
    
    return nearest_center_name, min_distance_center

def find_nearest_aed(patient):
    patient_location = (patient['latitude'], patient['longitude'])
    patient_index = patient.name  # 使用index来代替name
    
    # 计算步行距离到最近的 AED
    nearest_aeds = indices_aed[patient_index]  # 获取直线距离最近的 AED 索引
    aed_nearest = public_aed.iloc[nearest_aeds[0]]
    aed_location = (aed_nearest['latitude'], aed_nearest['longitude'])
    distance_aed = get_walking_distance(patient_location, aed_location)
    
    return aed_nearest['full_address'], distance_aed
