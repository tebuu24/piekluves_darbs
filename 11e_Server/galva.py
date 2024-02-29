from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database initialization
conn = sqlite3.connect('darbinieki.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS darbinieki (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vards TEXT NOT NULL,
        uzvards TEXT NOT NULL,
        tituls TEXT NOT NULL,
        parole TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS atslegas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        atslegas_numurs TEXT NOT NULL,
        pieejamiba INTEGER NOT NULL,
        komentars TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS izsniegums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lietotajs TEXT NOT NULL,
        atslegas_numurs TEXT NOT NULL,
        izsniegts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        komentars TEXT
    )
''')
conn.commit()

# Password hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        vards = request.form['vards']
        parole = request.form['parole']

        cursor.execute("SELECT * FROM darbinieki WHERE vards = ?", (vards,))
        user = cursor.fetchone()

        if user and user[4] == hash_password(parole):
            flash('Veiksmīga pieteikšanās!', 'success')
            return redirect(url_for('atslegas'))
        else:
            flash('Nepareiza lietotāja vārds vai parole.', 'danger')

    return render_template('login.html')

# Admin panel route
@app.route('/admin')
def admin_panel():
    cursor.execute("SELECT * FROM darbinieki")
    darbinieki = cursor.fetchall()
    return render_template('admin.html', darbinieki=darbinieki)

# Atslēgu informācijas route
@app.route('/atslegas')
def atslegas():
    cursor.execute("SELECT * FROM atslegas")
    atslegas = cursor.fetchall()
    return render_template('atslegas.html', atslegas=atslegas)

# Print data from the "darbinieki" table
cursor.execute("SELECT * FROM darbinieki")
darbinieki_data = cursor.fetchall()
print("Darbinieki data:")
for row in darbinieki_data:
    print(row)

# Print data from the "atslegas" table
cursor.execute("SELECT * FROM atslegas")
atslegas_data = cursor.fetchall()
print("Atslegas data:")
for row in atslegas_data:
    print(row)

# Print data from the "izsniegums" table
cursor.execute("SELECT * FROM izsniegums")
izsniegums_data = cursor.fetchall()
print("Izsniegums data:")
for row in izsniegums_data:
    print(row)

if __name__ == '__main__':
    app.run(debug=True)