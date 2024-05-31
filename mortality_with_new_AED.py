import dash_leaflet as dl
import pandas as pd
import os
import joblib
from geopy.distance import geodesic



def calculate_distance(coord1, coord2):
    """
    计算两个地理坐标之间的距离（单位：公里）
    """
    return geodesic(coord1, coord2).kilometers

def update_patient_survival_probabilities(new_aed_location, patients_df, model, distance_threshold=5):
    """
    计算新AED位置附近患者的生存概率
    """
    # 加载保存的模型流水线
    model = joblib.load('aed_survival_pipeline.pkl')

    new_lat, new_lon = new_aed_location

    # 初步筛选
    nearby_patients = patients_df[
        (patients_df['latitude'] >= new_lat - 0.045) & 
        (patients_df['latitude'] <= new_lat + 0.045) & 
        (patients_df['longitude'] >= new_lon - 0.045) & 
        (patients_df['longitude'] <= new_lon + 0.045)
    ]

    # 精确计算距离并筛选
    nearby_patients['distance_to_new_aed'] = nearby_patients.apply(
        lambda row: calculate_distance(new_aed_location, (row['latitude'], row['longitude'])), axis=1
    )
    nearby_patients = nearby_patients[nearby_patients['distance_to_new_aed'] <= distance_threshold]

    # 提取这些患者的数据
    X_nearby = nearby_patients[key_cols]
    survival_probabilities = model.predict_proba(X_nearby)[:, 0]  # 假设生存概率是正类的概率

    # 更新DataFrame中的生存概率
    patients_df.loc[nearby_patients.index, 'Survival_Probability'] = survival_probabilities

    return patients_df