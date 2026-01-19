from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import mysql.connector
import os
import joblib
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = Flask(__name__)

# Load model dan encoder (cukup sekali)
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "..", "model", "best_xgboost_model.pkl")
encoder_path = os.path.join(base_dir, "..", "model", "label_encoders.pkl")

with open(model_path, "rb") as f:
    model = joblib.load(f)

with open(encoder_path, "rb") as f:
    encoders = joblib.load(f)

# Fungsi koneksi baru per query
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        port=3308,
        password='',
        database='car_prices'
    )

def get_distinct_values(column):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT {column} FROM car WHERE {column} IS NOT NULL ORDER BY {column}")
    values = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return values

def get_distinct_sale_years():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT YEAR(SaleDate) FROM car WHERE SaleDate IS NOT NULL ORDER BY YEAR(SaleDate)")
    years = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return years

@app.route('/', methods=["GET", "POST"])
def index():
    prediction = None
    car_description = None
    makes = get_distinct_values("make")
    models = get_distinct_values("model")
    trims = get_distinct_values("trim")
    interiors = get_distinct_values("interior")
    sale_years = get_distinct_sale_years()

    if request.method == "POST":
        try:
            year = int(request.form["year"])
            make = request.form["make"]
            model_name = request.form["model"]
            trim = request.form["trim"]
            interior = request.form["interior"]
            condition = float(request.form["condition"])
            odometer = int(request.form["odometer"])
            sale_year = int(request.form["sale_year"])

            # Validasi input
            if make not in encoders['make'].classes_:
                raise ValueError(f"Make '{make}' not found in encoder.")
            if model_name not in encoders['model'].classes_:
                raise ValueError(f"Model '{model_name}' not found in encoder.")
            if trim not in encoders['trim'].classes_:
                raise ValueError(f"Trim '{trim}' not found in encoder.")
            if interior not in encoders['interior'].classes_:
                raise ValueError(f"Interior '{interior}' not found in encoder.")

            # Encode
            make_encoded = encoders['make'].transform([make])[0]
            model_encoded = encoders['model'].transform([model_name])[0]
            trim_encoded = encoders['trim'].transform([trim])[0]
            interior_encoded = encoders['interior'].transform([interior])[0]

            input_data = np.array([[year, make_encoded, model_encoded, trim_encoded,
                                    interior_encoded, condition, odometer, sale_year]])

            pred_price = model.predict(input_data)[0]
            prediction = round(pred_price, 2)
            
            prompt = f"Berikan saya deskripsi singkat dalam bahasa inggris mengenai mobil {make} {model_name} tahun {year}. Mohon untuk tidak menyertakan harga dalam deskripsi ini dan gunakan bahasa yang biasa digunakan dalam situs jual beli mobil bekas."

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt},
                    ]
                )
                car_description = response.choices[0].message.content
            except Exception as e:
                car_description = f"Gagal ambil deskripsi dari GPT: {e}"

        except Exception as e:
            prediction = f"Prediction Error: {e}"

    return render_template("index.html",
                           makes=makes,
                           models=models,
                           trims=trims,
                           interiors=interiors,
                           sale_years=sale_years,
                           prediction=prediction,
                           car_description=car_description)

# CHAINED ENDPOINTS
@app.route('/get-models/<make>')
def get_models(make):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT model FROM car WHERE make = %s ORDER BY model", (make,))
    models = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(models)

@app.route('/get-trims/<make>/<model>')
def get_trims(make, model):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT trim FROM car WHERE make = %s AND model = %s ORDER BY trim", (make, model))
    trims = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(trims)

@app.route('/get-interiors/<make>/<model>/<trim>')
def get_interiors(make, model, trim):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT interior FROM car 
        WHERE make = %s AND model = %s AND trim = %s 
        ORDER BY interior
    """, (make, model, trim))
    interiors = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(interiors)

@app.route('/get-years/<make>/<model>')
def get_years(make, model):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT year FROM car 
        WHERE make = %s AND model = %s 
        ORDER BY year DESC
    """, (make, model))
    years = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(years)

@app.route('/get-sale-years/<make>/<model>')
def get_sale_years(make, model):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT YEAR(SaleDate) FROM car
        WHERE make = %s AND model = %s AND SaleDate IS NOT NULL
        ORDER BY YEAR(SaleDate)
    """, (make, model))
    years = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(years)

if __name__ == "__main__":
    app.run()