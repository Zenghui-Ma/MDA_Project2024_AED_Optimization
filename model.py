import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib
import datetime
import time


intervention = pd.read_excel('data/intervention_all.xlsx')

# 解析日期时间字符串
def parse_datetime(x):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f%z", "%Y-%m-%d %H:%M:%S.%f"):
        try:
            return datetime.datetime.strptime(x, fmt)
        except ValueError:
            continue
    raise ValueError(f"时间数据 '{x}' 不匹配任何已知格式")

intervention['T0'] = intervention['T0'].astype("string")
intervention['T0'] = intervention['T0'].str[:26]
intervention['T0'] = intervention['T0'].apply(parse_datetime)
intervention['time'] = intervention['T0'].apply(lambda x: x.time())
intervention['Mortality'] = intervention.apply(lambda row: 1 if row['Abandon reason']=='Overleden' else 0, axis=1)

key_col = ['Mission ID','PostalCode permanence', 'Latitude intervention', 'Longitude intervention', 
           'EventLevel Trip', 'time', 'T3-T0 in Minutes', 'Mortality']
inter = intervention[key_col]
# 重命名列
inter.rename(columns={'PostalCode permanence': 'Postal_code',
                      'Latitude intervention': 'latitude',
                      'Longitude intervention': 'longitude'}, inplace=True)

import pandas as pd
from geopy.distance import geodesic
from sklearn.neighbors import BallTree
import numpy as np
import googlemaps

# 使用你的Google Maps API密钥
api_key = 'AIzaSyAaMgtqAAp07HTqibk9KlYkHIfHYK2sutc'
gmaps = googlemaps.Client(key=api_key)

patients = inter.copy()
hospitals = pd.read_excel('data/hospitals.xlsx')
aed_all = pd.read_excel('data/AED_locations.xlsx')
aed_data = aed_all[['id', 'full_address', 'latitude', 'longitude', 'public']]
aed_data.dropna(axis = 0, inplace = True)
public_aed = aed_data[aed_data['public'] == 'yes']

# 确保索引连续
patients.reset_index(drop=True, inplace=True)


# 计算救护中心的直线距离
centers_coords = np.radians(hospitals[['latitude', 'longitude']])
tree_centers = BallTree(centers_coords, metric='haversine')
patients_coords = np.radians(patients[['latitude', 'longitude']])
distances_centers, indices_centers = tree_centers.query(patients_coords, k=5)

# 计算 AED 的直线距离
aed_coords = np.radians(public_aed[['latitude', 'longitude']])
tree_aed = BallTree(aed_coords, metric='haversine')
distances_aed, indices_aed = tree_aed.query(patients_coords, k=1)


# 定义一个函数来计算步行距离
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

# 计算步行距离
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

# 计算步行距离
def find_nearest_aed(patient):
    patient_location = (patient['latitude'], patient['longitude'])
    patient_index = patient.name  # 使用index来代替name
    
    # 计算步行距离到最近的 AED
    nearest_aeds = indices_aed[patient_index]  # 获取直线距离最近的 AED 索引
    aed_nearest = public_aed.iloc[nearest_aeds[0]]
    aed_location = (aed_nearest['latitude'], aed_nearest['longitude'])
    distance_aed = get_walking_distance(patient_location, aed_location)
    
    return aed_nearest['full_address'], distance_aed


# 对每个患者计算步行距离最近的急救中心
results_centers = patients.apply(find_nearest_center, axis=1, result_type='expand')
patients['nearest_center_name'] = results_centers[0]
patients['distance_to_center'] = results_centers[1] / 1000  # 转换为公里

# 对每个患者计算步行距离最近的 AED
results_aeds = patients.apply(find_nearest_aed, axis=1, result_type='expand')
patients['nearest_aed_name'] = results_aeds[0]
patients['distance_to_aed'] = results_aeds[1] / 1000  # 转换为公里
patients.to_excel('data/patients.xlsx')

# model
patients = pd.read_excel('data/patients.xlsx')
# 将事件类型和时间等特征转化为合适的格式
patients['time'] = patients['time'].str[:8]
patients['time'] = pd.to_datetime(patients['time'], format='%H:%M:%S').dt.hour
patients.to_excel('data/patients.xlsx')


# 选择特征和标签
key_cols = ['Postal_code', 'latitude', 'longitude', 'EventLevel Trip', 
            'distance_to_center', 'distance_to_aed', 'time']
X = patients[key_cols]
y = patients['Mortality']

# 获取所有可能的类别
postal_code_categories = sorted(X['Postal_code'].unique())
event_level_categories = sorted(X['EventLevel Trip'].unique())

# 对分类变量进行One-Hot编码
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['latitude', 'longitude', 
                                   'distance_to_center', 'distance_to_aed', 'time']),
        ('cat', OneHotEncoder(categories=[postal_code_categories, event_level_categories], handle_unknown='ignore'), 
         ['Postal_code', 'EventLevel Trip'])
    ])

# XGBoost模型
xgb = XGBClassifier(random_state=42)

# 超参数范围
param_grid = {
    'n_estimators': [200],
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [1.0],
    'colsample_bytree': [1.0]
}

# 网格搜索
grid_search = GridSearchCV(
    estimator=xgb, param_grid=param_grid, 
    scoring='roc_auc', cv=10, verbose=2, n_jobs=-1  # 将交叉验证的折数改为5
)

# 建立模型流水线
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('grid_search', grid_search)
])

# 训练模型并进行交叉验证
model.fit(X, y)

# 保存整个模型流水线
joblib.dump(model, 'aed_survival_pipeline.pkl')

# 评估模型
cv_results = grid_search.cv_results_
best_params = grid_search.best_params_
best_score = grid_search.best_score_

print(f'Best Parameters: {best_params}')
print(f'Best ROC AUC Score: {best_score}')

