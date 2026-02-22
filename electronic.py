import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# 샘플 데이터 생성
np.random.seed(42)
data_size = 1000
metal_oxides = ['MnO2', 'Co3O4', 'NiO', 'TiO2']
electrolytes = ['polymer', 'aqueous', 'organic']

df = pd.DataFrame({
    'Metal_Oxide': np.random.choice(metal_oxides, data_size),
    'Graphene_Ratio': np.random.uniform(1, 70, data_size),  
    'Surface_Area': np.random.uniform(500, 3000, data_size),  
    'Electrolyte': np.random.choice(electrolytes, data_size),
    'Voltage': np.random.uniform(1, 4, data_size),  
    'Current_Density': np.random.uniform(1, 15, data_size),  
})

# 범주형 데이터를 숫자로 변환
df['Metal_Oxide'] = df['Metal_Oxide'].astype('category').cat.codes
df['Electrolyte'] = df['Electrolyte'].astype('category').cat.codes

# 출력 변수 생성 (가상의 데이터)
df['Capacitance'] = 50 + df['Graphene_Ratio'] * 1.2 + df['Surface_Area'] * 0.02 + df['Voltage'] * 5
df['Efficiency'] = 70 + df['Metal_Oxide'] * 2 + df['Graphene_Ratio'] * 0.3 - df['Current_Density'] * 1.5

# 데이터 분할
X = df.drop(columns=['Capacitance', 'Efficiency'])
y_capacitance = df['Capacitance']
y_efficiency = df['Efficiency']

X_train, X_test, y_train_cap, y_test_cap = train_test_split(X, y_capacitance, test_size=0.2, random_state=42)
X_train, X_test, y_train_eff, y_test_eff = train_test_split(X, y_efficiency, test_size=0.2, random_state=42)

# 모델 학습
model_capacitance = RandomForestRegressor(n_estimators=100, random_state=42)
model_efficiency = RandomForestRegressor(n_estimators=100, random_state=42)

model_capacitance.fit(X_train, y_train_cap)
model_efficiency.fit(X_train, y_train_eff)

# 예측 수행
y_pred_cap = model_capacitance.predict(X_test)
y_pred_eff = model_efficiency.predict(X_test)

# 모델 평가
mae_cap = mean_absolute_error(y_test_cap, y_pred_cap)
r2_cap = r2_score(y_test_cap, y_pred_cap)

mae_eff = mean_absolute_error(y_test_eff, y_pred_eff)
r2_eff = r2_score(y_test_eff, y_pred_eff)

# **최적의 조합 찾기 (합산 값이 가장 높은 인덱스 찾기)**
best_index = np.argmax(y_pred_cap + y_pred_eff)

# **best_index가 실제 데이터 크기 내에 있는지 확인**
if best_index < len(X_test):
    best_params = X_test.iloc[best_index]
else:
    best_params = None  # 오류 방지를 위해 None 처리

# 최종 결과 출력
(mae_cap, r2_cap, mae_eff, r2_eff, best_params)
