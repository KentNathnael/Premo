# Premo — AI Car Price Prediction

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Framework](https://img.shields.io/badge/framework-Flask%20%7C%20XGBoost-green)
![License](https://img.shields.io/badge/license-MIT-orange)

**Premo** is an **AI-powered project** designed to predict car prices using the **XGBoost** algorithm.  
Developed by **Rio Dwi Oktavianto, Kent Nathanael, Theodorus Yuriputra Wibisono, and Nathaniel Christodeo Panget** as part of a data science and web deployment exploration.

---

## ✨ Features

- 📊 **Car price prediction** based on features such as year, brand, model, condition, and more.  
- ⚡ **XGBoost Model**: a high-performance boosting algorithm for accurate predictions.  
- 🌐 **Web-ready**: easy to integrate with Flask or FastAPI.  
- 📂 **Modular project structure**: clean and extendable for future improvements.  

---

## 📁 Project Structure

```
/
├── data/                # raw dataset & processed dataset
├── model/               # trained XGBoost models (pickle/joblib)
├── test/                # testing scripts & evaluation data
├── training.ipynb       # notebook for training & experiments
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/KentNathnael/Premo.git
cd Premo
```

### 2. Setup environment
```bash
python -m venv venv
source venv/bin/activate   # MacOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the model
Run the Jupyter Notebook:
```bash
jupyter notebook training.ipynb
```
The trained model will be saved under the `model/` folder.

### 5. Testing
Use the scripts inside the `test/` directory to evaluate the model.

---

🌍 Deployment

Premo is deployed and can be accessed at:
👉 premo.fun

Check it out to see the live web app in action!

---

## 📌 Planned API Endpoints

If integrated with Flask/FastAPI, planned endpoints include:

- `POST /predict` → send car features → return predicted price  
- `POST /predict_batch` → upload CSV → return predictions for each entry  

---

## 🛠 Tech Stack

- **Python 3.9+**
- **XGBoost**
- **scikit-learn**
- **Pandas, NumPy**
- (Optional) Flask / FastAPI for deployment

---

## 🧑‍🤝‍🧑 Authors

- Rio Dwi Oktavianto  
- Kent Nathanael  
- Theodorus Yuriputra Wibisono  
- Nathaniel Christodeo Panget

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).  

---

© 2025 Rio, Kent, Theodorus, Nathaniel — All Rights Reserved
