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

# 假设patients是你的DataFrame
patients = pd.read_excel('data/patients_combined.xlsx')

# 将事件类型和时间等特征转化为合适的格式
patients['time'] = patients['time'].str[:8]
patients['time'] = pd.to_datetime(patients['time'], format='%H:%M:%S').dt.hour

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
