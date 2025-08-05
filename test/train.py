import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
import pickle
import json
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 🔌 Koneksi ke database
def load_data_from_mysql():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='car_prices',
        port=3308
    )
    query = "SELECT * FROM car"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 🔄 Ambil data
print("🔄 Mengambil data dari database...")
df = load_data_from_mysql()

# 🔧 Preprocessing
df = df.drop_duplicates()
df = df.dropna(subset=['sellingprice', 'odometer', 'year'])

# Konversi odometer ke numeric
df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce')

# Konversi SaleDate jadi tahun
df['SaleDate'] = pd.to_datetime(df['SaleDate'], errors='coerce')
df['SaleYear'] = df['SaleDate'].dt.year

# Kolom yang dibutuhin
cols = ['year', 'make', 'model', 'trim', 'interior', 'condition', 'odometer', 'SaleYear']
target = 'sellingprice'

# Drop yang masih kosong
df = df.dropna(subset=cols + [target])

# Label Encoding buat kolom kategori
X = df[cols].copy()
y = df[target]

encoders = {}
for col in ['make', 'model', 'trim', 'interior']:
    le = LabelEncoder()
    X.loc[:, col] = le.fit_transform(X[col])
    encoders[col] = le

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🏋️ Training model
print("🏋️ Melatih model XGBoost...")
model = XGBRegressor(n_estimators=100, learning_rate=0.1)
model.fit(X_train, y_train)

# 💾 Simpan model dan encoder
with open('../model/best_xgboost_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('../model/label_encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)




print("✅ Model dan encoder berhasil disimpan.")
