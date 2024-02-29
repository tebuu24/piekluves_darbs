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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username and password are correct (you can replace this with your authentication logic)
        if username == 'admin' and password == 'adminpassword':
            flash('Veiksmīga pieteikšanās!', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Nepareiza lietotājvārds vai parole.', 'danger')

    return render_template('login.html')

@app.route('/admin_panel')
def admin_panel():
    # You can add your admin panel logic here
    return 'Admin Panel'


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

# Function to write data to a text file
def write_to_file(data, filename):
    try:
        with open(filename, 'w') as f:
            for row in data:
                f.write(','.join(str(item) for item in row) + '\n')
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"Error writing data to {filename}: {e}")



if __name__ == '__main__':
    app.run(debug=True)