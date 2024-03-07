from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'jūsu_slēptā_atslēga'

# Datubāzes inicializācija
conn = sqlite3.connect('darbinieki.db', check_same_thread=False)
cursor = conn.cursor()

# Izveido tabulas, ja tās vēl neeksistē
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

# Funkcija parolei hashēšanai
def hash_parole(parole):
    return hashlib.sha256(parole.encode()).hexdigest()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        lietotajvards = request.form['lietotajvards']
        parole = request.form['parole']

        # Pārbauda, vai lietotājvārds un parole ir pareizi
        if lietotajvards == 'admin' and parole == 'adminparole':
            flash('Veiksmīga pieteikšanās!', 'success')
            return redirect(url_for('admin_panel'))  # Novirza uz admin paneļa lapu
        else:
            # Pārbauda, vai lietotājs eksistē datubāzē
            cursor.execute("SELECT * FROM darbinieki WHERE vards = ? AND parole = ?", (lietotajvards, hash_parole(parole)))
            lietotajs = cursor.fetchone()
            if lietotajs:
                flash('Veiksmīga pieteikšanās!', 'success')
                return redirect(url_for('atslegas'))  # Novirza uz atslēgu lapu
            else:
                flash('Nepareizs lietotājvārds vai parole.', 'danger')

    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        lietotajvards = request.form['lietotajvards']
        parole = request.form['parole']

        # Pārbauda, vai lietotājvārds un parole ir pareizi adminam
        if lietotajvards == 'admin' and parole == 'adminparole':
            flash('Veiksmīga pieteikšanās!', 'success')
            return redirect(url_for('admin_panel'))  # Novirza uz admin paneļa lapu
        else:
            flash('Nepareizs lietotājvārds vai parole.', 'danger')

    return render_template('admin.html')

@app.route('/pievienot', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        vards = request.form['vards']
        uzvards = request.form['uzvards']
        tituls = request.form['tituls']
        parole = request.form['parole']

        # Ievieto datus tabulā darbinieki
        cursor.execute("INSERT INTO darbinieki (vards, uzvards, tituls, parole) VALUES (?, ?, ?, ?)",
                       (vards, uzvards, tituls, hash_parole(parole)))
        conn.commit()
        flash('Darbinieks veiksmīgi pievienots!', 'success')

    return render_template('pievienot.html')

# Atslēgu informācijas route
@app.route('/atslegas')
def atslegas():
    cursor.execute("SELECT * FROM atslegas")
    atslegas = cursor.fetchall()
    return render_template('atslegas.html', atslegas=atslegas)

# Funkcija, lai izdrukātu datus no "darbinieki" tabulas
cursor.execute("SELECT * FROM darbinieki")
darbinieki_data = cursor.fetchall()
print("Darbinieki dati:")
for row in darbinieki_data:
    print(row)

# Funkcija, lai izdrukātu datus no "atslegas" tabulas
cursor.execute("SELECT * FROM atslegas")
atslegas_data = cursor.fetchall()
print("Atslēgu dati:")
for row in atslegas_data:
    print(row)

# Funkcija, lai izdrukātu datus no "izsniegums" tabulas
cursor.execute("SELECT * FROM izsniegums")
izsniegums_data = cursor.fetchall()
print("Izsnieguma dati:")
for row in izsniegums_data:
    print(row)

# Funkcija, lai ierakstītu datus failā
def rakstīt_failā(dati, fails):
    try:
        with open(fails, 'w') as f:
            for row in dati:
                f.write(','.join(str(viens) for viens in row) + '\n')
        print(f"Dati veiksmīgi ierakstīti failā {fails}")
    except Exception as e:
        print(f"Kļūda, rakstot datus failā {fails}: {e}")

if __name__ == '__main__':
    app.run(debug=True)
