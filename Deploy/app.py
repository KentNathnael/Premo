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

# @app.route('/')
# def makee():
#     cursor.execute("SELECT DISTINCT make FROM car") 
#     data = cursor.fetchall()
#     return render_template('pages/forms/basic_elements.html', jumlah=data)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        cursor.execute("INSERT INTO mahasiswa (nama, email) VALUES (%s, %s)", (nama, email))
        conn.commit()
        return redirect('/')
    return render_template('tambah.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        cursor.execute("UPDATE mahasiswa SET nama=%s, email=%s WHERE id=%s", (nama, email, id))
        conn.commit()
        return redirect('/')
    cursor.execute("SELECT * FROM mahasiswa WHERE id=%s", (id,))
    data = cursor.fetchone()
    return render_template('edit.html', mhs=data)

@app.route('/hapus/<int:id>')
def hapus(id):
    cursor.execute("DELETE FROM mahasiswa WHERE id=%s", (id,))
    conn.commit()
    return redirect('/')

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
    models = []
    trims = []
    years = []
    interior = []

    if request.method == 'POST':
        selected_make = request.form.get('make')
        selected_model = request.form.get('model')
        selected_trim = request.form.get('trim')
        selected_year = request.form.get('year')
        selected_interior = request.form.get('interior')

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

    return render_template(
        'pages/forms/basic_elements.html',
        makes=makes,
        models=models,
        trims=trims,
        years=years,
        interior=interior,
        conditions=conditions,
        selected_make=selected_make,
        selected_model=selected_model,
        selected_trim=selected_trim,
        selected_year=selected_year,
        selected_interior = selected_interior
    )



if __name__ == '__main__':
    app.run(debug=True)
