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
        darbinieks_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vards TEXT NOT NULL,
        uzvards TEXT NOT NULL,
        tituls TEXT NOT NULL,
        parole TEXT NOT NULL
    )
''')

# pie pieejamības vajadzētu pārveidot uz boolean!
cursor.execute('''
    CREATE TABLE IF NOT EXISTS atslegas (
        atslegas_id INTEGER PRIMARY KEY AUTOINCREMENT,
        atslegas_numurs TEXT NOT NULL,
        pieejamiba BOOLEAN NOT NULL,   
        komentars TEXT,
        kastes_nr INTEGER NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS izsniegums (
        izsniegums_id INTEGER PRIMARY KEY AUTOINCREMENT,
        darbinieka_id INTEGER NOT NULL,
        atslegas_id TEXT NOT NULL,
        izsnieguma_laiks TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        komentars TEXT
    )
''')
conn.commit()

# Funkcija parolei hashēšanai
def hash_parole(parole):
    return hashlib.sha256(parole.encode()).hexdigest()

#lietotāja pieslēgšanās lapa
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        lietotajvards = request.form['lietotajvards']
        parole = request.form['parole']

        # Pārbauda, vai lietotājvārds un parole ir admin
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

#admin pieslēgšanās lapa
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

# Admin panel page with employee data
@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        vards = request.form['vards']
        uzvards = request.form['uzvards']
        tituls = request.form['tituls']
        parole = request.form['parole']
        parole_atskaites = request.form['parole_atskaites']

        # Check if passwords match
        if parole != parole_atskaites:
            flash('Paroles nesakrīt!', 'danger')
            return redirect(url_for('admin_panel'))

        # Insert data into darbinieki table
        cursor.execute("INSERT INTO darbinieki (vards, uzvards, tituls, parole) VALUES (?, ?, ?, ?)",
                       (vards, uzvards, tituls, hash_parole(parole)))
        conn.commit()
        flash('Darbinieks veiksmīgi pievienots!', 'success')

    # Fetch all employees from darbinieki table
    cursor.execute("SELECT * FROM darbinieki")
    darbinieki = cursor.fetchall()
    return render_template('admin_panel.html', darbinieki=darbinieki)



# Atslēgu informācijas route
@app.route('/atslegas')
def atslegas():
    cursor.execute("SELECT * FROM atslegas")
    atslegas = cursor.fetchall()

    return render_template('atslegas.html', atslegas=atslegas)

if __name__ == '__main__':
    app.run(debug=True)
