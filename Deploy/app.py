from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__, template_folder="templates", static_folder="assets")

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='car_prices'
)
cursor = conn.cursor()

@app.route('/')
def count():
    cursor.execute("SELECT COUNT(*) FROM car")
    data = cursor.fetchone() 
    return render_template('index.html', jumlah=data[0])  

@app.route("/pages/ui-features/buttons.html")
def buttons_page():
    return render_template("pages/ui-features/buttons.html")

@app.route("/pages/ui-features/dropdowns.html")
def dropdowns_page():
    return render_template("pages/ui-features/dropdowns.html")

@app.route("/pages/ui-features/typography.html")
def typography_page():
    return render_template("pages/ui-features/typography.html")

@app.route("/pages/forms/basic_elements.html", methods=['GET', 'POST'])
def forms_page():
    cursor.execute("SELECT DISTINCT make FROM car") 
    makes = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT `condition` FROM car ORDER BY `condition` ASC")
    conditions = cursor.fetchall()
    
    selected_make = None
    selected_model = None
    selected_trim = None
    selected_year = None
    selected_interior = None
    selected_sales_year = None
    models = []
    trims = []
    years = []
    interior = []
    sales_years = []

    if request.method == 'POST':
        selected_make = request.form.get('make')
        selected_model = request.form.get('model')
        selected_trim = request.form.get('trim')
        selected_year = request.form.get('year')
        selected_interior = request.form.get('interior')
        selected_sales_year = request.form.get('SaleDate')

        if selected_make:
            cursor.execute("SELECT DISTINCT model FROM car WHERE make=%s", (selected_make,))
            models = cursor.fetchall()

        if selected_make and selected_model:
            cursor.execute("SELECT DISTINCT trim FROM car WHERE make=%s AND model=%s", (selected_make, selected_model))
            trims = cursor.fetchall()
            
        if selected_make and selected_model and selected_trim:
            cursor.execute("SELECT DISTINCT year FROM car WHERE make=%s AND model=%s AND trim=%s ORDER BY year ASC", (selected_make, selected_model, selected_trim))
            years = cursor.fetchall()
        
        if selected_make and selected_model and selected_trim and selected_year:
            cursor.execute("SELECT DISTINCT interior FROM car WHERE make=%s AND model=%s AND trim=%s AND year=%s", (selected_make, selected_model, selected_trim, selected_year))
            interior = cursor.fetchall()
            
        if selected_make and selected_model and selected_trim and selected_year and selected_interior:
            cursor.execute("SELECT DISTINCT SaleDate FROM car WHERE make=%s AND model=%s AND trim=%s AND year=%s AND interior=%s", (selected_make, selected_model, selected_trim, selected_year, selected_interior))
            sales_years = cursor.fetchall()

    return render_template(
        'pages/forms/basic_elements.html',
        makes=makes,
        models=models,
        trims=trims,
        years=years,
        interior=interior,
        sales_years=sales_years,
        conditions=conditions,
        selected_make=selected_make,
        selected_model=selected_model,
        selected_trim=selected_trim,
        selected_year=selected_year,
        selected_interior = selected_interior,
        selected_sales_year=selected_sales_year
    )


if __name__ == '__main__':
    app.run(debug=True)
