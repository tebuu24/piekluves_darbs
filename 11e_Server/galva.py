from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'jūsu_slēptā_atslēga'

# Funkcija datubāzes savienojuma izveidei
def get_db_connection():
    conn = sqlite3.connect('darbinieki.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inicializē datubāzi
with get_db_connection() as conn:
    cursor = conn.cursor()
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

# Lietotāja pieslēgšanās maršruts
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        vards = request.form['vards']
        uzvards = request.form['uzvards']
        parole = request.form['parole']

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM darbinieki WHERE vards = ? AND uzvards = ? AND parole = ?", (vards, uzvards, parole))
            user = cursor.fetchone()

        if user:
            session['username'] = f"{vards} {uzvards}"  # Apvieno vārdu un uzvārdu
            flash('Veiksmīga pieteikšanās!', 'success')
            return redirect(url_for('atslegas'))  # Pārvirza uz 'atslegas' lapu pēc veiksmīgas pieslēgšanās
        else:
            flash('Nepareizs lietotājvārds vai parole.', 'danger')

    return render_template('login.html')

# Admina pieslēgšanās maršruts
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        lietotajvards = request.form['lietotajvards']
        parole = request.form['parole']
        if lietotajvards == 'admin' and parole == 'adminparole':
            flash('Veiksmīga pieteikšanās!', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Nepareizs lietotājvārds vai parole.', 'danger')

    return render_template('admin.html')

# Admina paneļa lapa
@app.route('/admin_panel')
def admin_panel():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM darbinieki")
        darbinieki = cursor.fetchall()
    return render_template('admin_panel.html', darbinieki=darbinieki)

# Pievieno lietotāju
@app.route('/add_user', methods=['POST'])
def add_user():
    vards = request.form['vards']
    uzvards = request.form['uzvards']
    tituls = request.form['tituls']
    parole = request.form['parole']
    parole_atskaites = request.form['parole_atskaites']

    if parole != parole_atskaites:
        flash('Paroles nesakrīt!', 'danger')
    else:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO darbinieki (vards, uzvards, tituls, parole) VALUES (?, ?, ?, ?)",
                           (vards, uzvards, tituls, parole))
            conn.commit()
        flash('Darbinieks veiksmīgi pievienots!', 'success')

    return redirect(url_for('admin_panel'))

# Atslēgu datu iegūšana no datubāzes
@app.route('/atslegas')
def atslegas():
    current_user = session.get('username')
    if current_user:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT atslegas_numurs, kastes_nr FROM atslegas WHERE kastes_nr IN (1, 2)")
            keys = cursor.fetchall()

        vecais_korpuss = [key['atslegas_numurs'] for key in keys if key['kastes_nr'] == 1]
        jaunais_korpuss = [key['atslegas_numurs'] for key in keys if key['kastes_nr'] == 2]

        return render_template('atslegas.html', username=current_user, vecais_korpuss=vecais_korpuss, jaunais_korpuss=jaunais_korpuss)
    else:
        flash('Lūdzu, pieslēdzieties vispirms.', 'danger')
        return redirect(url_for('login'))

# Izrakstīšanās maršruts
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Jūs esat veiksmīgi izrakstījies!', 'success')
    return redirect(url_for('login'))

# Dzēš lietotāju
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM darbinieki WHERE darbinieks_id = ?", (user_id,))
            conn.commit()
        return jsonify({'message': 'Lietotājs ir dzēsts'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Funkcija atslēgas pievienošanai datubāzē
def add_atslega(atslegas_numurs, pieejamiba, komentars, kastes_nr):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Pārbauda vai atslēga jau eksistē
            cursor.execute("SELECT atslegas_id FROM atslegas WHERE atslegas_numurs = ?", (atslegas_numurs,))
            existing_key = cursor.fetchone()

            if existing_key is None:
                cursor.execute('''
                    INSERT INTO atslegas (atslegas_numurs, pieejamiba, komentars, kastes_nr)
                    VALUES (?, ?, ?, ?)
                ''', (atslegas_numurs, pieejamiba, komentars, kastes_nr))
                conn.commit()
                print("Atslēga veiksmīgi pievienota!")
            else:
                print("Atslēga ar šo numuru jau eksistē.")
    except sqlite3.Error as e:
        print("Kļūda pievienojot atslēgu:", e)

# Maršruts atslēgas pievienošanas lapas attēlošanai
@app.route('/add_key', methods=['GET', 'POST'])
def add_key():
    if request.method == 'POST':
        atslegas_numurs = request.form['atslegas_numurs']
        pieejamiba = request.form.get('pieejamiba') == 'on'
        komentars = request.form['komentars']
        kastes_nr = int(request.form['kastes_nr'])
        add_atslega(atslegas_numurs, pieejamiba, komentars, kastes_nr)
        flash('Atslēga veiksmīgi pievienota!', 'success')
        return redirect(url_for('add_key'))
    return render_template('add_key.html')

# Pievieno atslēgas no Python koda
keys_to_add = [
    {'atslegas_numurs': 'A1', 'pieejamiba': True, 'komentars': 'Galvenā ieeja', 'kastes_nr': 1},
    {'atslegas_numurs': 'B2', 'pieejamiba': True, 'komentars': 'Serveru telpa', 'kastes_nr': 2},
    {'atslegas_numurs': 'C3', 'pieejamiba': False, 'komentars': 'Noliktava', 'kastes_nr': 1},
    # Pievieno vairāk atslēgu pēc nepieciešamības
]

# Pievieno atslēgas datubāzē no Python koda
for key in keys_to_add:
    add_atslega(key['atslegas_numurs'], key['pieejamiba'], key['komentars'], key['kastes_nr'])

if __name__ == '__main__':
    app.run(debug=True)
