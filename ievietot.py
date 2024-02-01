from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)

# Funkcija, lai ģenerētu nejaušu noslēpumu atslēgu
def generet_noslepuma_atslegu():
    return os.urandom(24)

# Iestatīt noslēpuma atslēgu Flask lietotnei
app.config['SECRET_KEY'] = generet_noslepuma_atslegu()

try:
    # Mēģināt importēt flask-talisman
    from flask_talisman import Talisman
    Talisman(app)
    print("flask-talisman konfigurēts veiksmīgi.")
except Exception as e:
    print(f"Kļūda, konfigurējot flask-talisman: {e}")

# Pārējais kods paliek nemainīgs
