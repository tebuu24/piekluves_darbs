from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
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
        vards = request.form['vards']
        uzvards = request.form['uzvards']
        parole = request.form['parole']
 
        # Check if user exists in the database
        cursor.execute("SELECT * FROM darbinieki WHERE vards = ? AND uzvards = ? AND parole = ?", (vards, uzvards, parole))
        user = cursor.fetchone()
       
        if user:
            # Store username in session
            session['username'] = f"{vards} {uzvards}"  # Combine first and last name
            flash('Veiksmīga pieteikšanās!', 'success')
            return redirect(url_for('atslegas'))  # Redirect to the 'atslegas' page upon successful login
        else:
            flash('Nepareizs lietotājvārds vai parole.', 'danger')
   
    # If the request method is GET or if the login attempt was unsuccessful, render the login page
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
@app.route('/admin_panel')
def admin_panel():
    cursor.execute("SELECT * FROM darbinieki")
    darbinieki = cursor.fetchall()
    return render_template('admin_panel.html', darbinieki=darbinieki)

# pievienot lietotāju
@app.route('/add_user', methods=['POST'])
def add_user():
    vards = request.form['vards']
    uzvards = request.form['uzvards']
    tituls = request.form['tituls']
    parole = request.form['parole']
    parole_atskaites = request.form['parole_atskaites']

    # vai paroles sakrīt
    if parole != parole_atskaites:
        flash('Paroles nesakrīt!', 'danger')
    else:
        # ievietot datubāzes tabulā
        cursor.execute("INSERT INTO darbinieki (vards, uzvards, tituls, parole) VALUES (?, ?, ?, ?)",
                       (vards, uzvards, tituls, parole))
        conn.commit()
        flash('Darbinieks veiksmīgi pievienots!', 'success')
    # atpakaļ uz admin_panel lapu
    return redirect(url_for('admin_panel'))


# Atslēgu informācijas 
@app.route('/atslegas')
def atslegas():
    # Retrieve the current user from the session
    current_user = session.get('username')
    if current_user:
        # Pass the current user to the template
        return render_template('atslegas.html', username=current_user)
    else:
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))

#dzēst lietotāju no admin_panel lapas 
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        cursor.execute("DELETE FROM darbinieki WHERE id = ?", (user_id,))
        conn.commit()
        return jsonify({'message': 'Lietotājs ir dzēsts'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 






if __name__ == '__main__':
    app.run(debug=True)
