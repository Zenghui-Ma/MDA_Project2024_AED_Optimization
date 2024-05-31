import joblib
import dash_leaflet as dl
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree
from geopy.distance import geodesic
from aed_location_existed import read_patient_data, read_aed_data

# 加载保存的模型流水线
model = joblib.load('aed_survival_pipeline.pkl')

def update_distance_to_aed(patients_df, aed_locations):
    """
    更新患者到最近的 AED 的距离
    """
    if not aed_locations:
        # 如果 aed_locations 为空，则返回原始的 patients_df
        patients_df['distance_to_aed'] = np.nan
        return patients_df
    
    # 创建 BallTree 以计算距离
    aed_coords = np.radians(aed_locations)
    tree_aed = BallTree(aed_coords, metric='haversine')
    patient_coords = np.radians(patients_df[['latitude', 'longitude']])
    
    distances_aed, indices_aed = tree_aed.query(patient_coords, k=1)
    distances_aed = distances_aed * 6371  # 转换为公里
    
    patients_df['distance_to_aed'] = distances_aed
    return patients_df

def update_patient_survival_probabilities(patients_df, model):
    """
    计算所有患者的生存概率
    """
    # 提取这些患者的数据
    key_cols = ['Postal_code', 'latitude', 'longitude', 'EventLevel Trip', 
                'distance_to_center', 'distance_to_aed', 'time']
    X = patients_df[key_cols]
    print('Computing the new survival probability...')
    non_survival_probabilities = model.predict_proba(X)[:, 0]  # 获取负类（生存）的概率
    print('Computed.')

    # 更新DataFrame中的生存概率
    patients_df['Non_Survival_Probability'] = non_survival_probabilities

    return patients_df

def generate_patient_tooltips_with_probability(patients_df):
    tooltips = []
    for _, row in patients_df.iterrows():
        popup_text = f"{row['Non_Survival_Probability']:.2f}"
        tooltip = dl.Tooltip(popup_text, permanent=True, direction="right")
        tooltips.append((row['latitude'], row['longitude'], tooltip))
    return tooltips