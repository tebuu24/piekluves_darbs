from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3

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
            cursor.execute("SELECT * FROM darbinieki WHERE vards = ? AND parole = ?", (lietotajvards, parole))
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

# Admin panelis, kur var pievienot jaunu lietotāju un redzēt datubāzes datus
# Admin panel page with employee data
@app.route('/admin_panel')
def admin_panel():
    # Fetch all employees from darbinieki table
    cursor.execute("SELECT * FROM darbinieki")
    darbinieki = cursor.fetchall()
    return render_template('admin_panel.html', darbinieki=darbinieki)

# Add user route
@app.route('/add_user', methods=['POST'])
def add_user():
    vards = request.form['vards']
    uzvards = request.form['uzvards']
    tituls = request.form['tituls']
    parole = request.form['parole']
    parole_atskaites = request.form['parole_atskaites']

    # Check if passwords match
    if parole != parole_atskaites:
        return ({'message': 'Paroles nesakrīt!', 'type': 'danger'})

    # Insert data into darbinieki table
    cursor.execute("INSERT INTO darbinieki (vards, uzvards, tituls, parole) VALUES (?, ?, ?, ?)",
                   (vards, uzvards, tituls, parole))
    conn.commit()
    return ({'message': 'Darbinieks veiksmīgi pievienots!', 'type': 'success'})

# Atslēgu informācijas route
@app.route('/atslegas')
def atslegas():
    cursor.execute("SELECT * FROM atslegas")
    atslegas = cursor.fetchall()

    return render_template('atslegas.html', atslegas=atslegas)

if __name__ == '__main__':
    app.run(debug=True)
