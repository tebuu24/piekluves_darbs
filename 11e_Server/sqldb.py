import sqlite3
 
# savieno ar db
conn = sqlite3.connect('musu_datubaze.db')
 
#izveido kursora objektu ar kuru veido izmainas
cursor = conn.cursor()
 
# izveido tabulu
cursor.execute('''
    CREATE TABLE IF NOT EXISTS darbinieki (
        id INTEGER PRIMARY KEY,
        vards TEXT
        uzvards TEXT
        statuss TEXT
        pk TEXT
    )
               
    CREATE TABLE IF NOT EXISTS atslega (
        id INTEGER PRIMARY KEY,
        numurs INTEGER
        kurpuss INTEGER
        apraksts TEXT
        kastes_nr TEXT
    )
    
    CREATE TABLE IF NOT EXISTS izsniegums (
        id INTEGER PRIMARY KEY,
        darbinieka_ID TEXT
        atslēgas_ID TEXT
        apraksts INTEGER
        laiks_kad_izsniegta TEXT
        laiks_kad_atgriezta TEXT
    )
''')
 
# Commit the changes and close the connection
conn.commit()
conn.close()