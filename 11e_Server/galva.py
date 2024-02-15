# Musu Flask serveris
from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
from flask import json
from flask import jsonify
from flask import Flask, request, redirect


app = Flask(__name__)

@app.route('/',methods=['GET'])
def root():
    return render_template("tests.html")

@app.route('/uzruna',methods=['GET', 'POST'])
def uzruna():
   if request.method == 'POST':
      vards1 = request.form['vards']
      uzvards1 = request.form['uzvards']
      return render_template("sveiciens.html",vards=vards1,uzvards=uzvards1)  
   else:
      vards1 = request.args.get('vards')
      uzvards1 = request.args.get('uzvards')
      return vards1, uzvards1
  
#login lapa----
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    #parbaude
    if username == 'liet' and password == 'lietuva':
        return redirect('/sveiciens')
    else:
        return 'nepareiza login info'

@app.route('/vards')
def katevisauc():
  return render_template("katevisauc.html") 
 
@app.route('/dati')
def dati():
  aa = {'name':"bumba",'vecums':"16"}
  return jsonify(aa)

# Tukšas formas izsaukums
# Šo izsauc ar http://127.0.0.1:5000/personas
@app.route('/personas')
def personas():
  personas = []
  with open("static/personas.txt","r",encoding="UTF-8") as f1:
    for rinda in f1:
      personas.append(rinda)   
  return jsonify({"personas": personas})

@app.route('/dts', methods=['POST'])
def receive_data():
  data = request.json #sanem datus no fetch
  print(data)
  response_data ={'meassage':'dati sanemti veiksmigi'}
  return jsonify(response_data) #atgriež vertibu fetch

@app.route('/data')
def data():
  return render_template("data.html")
# Rezervējam virtuves piederumus
# Šo izsauc ar http://127.0.0.1:5000/rezerveshana

# Tukšas formas izsaukums
# Šo izsauc ar http://127.0.0.1:5000/visi
@app.route('/visi')
def visi():
  return render_template("personas.html")

#----------------------------------------------------      

@app.route('/tests')
def health():
  return render_template("tests.html")

if __name__ == '__main__':
  app.run(debug=True,port=5000) # ,host='0.0.0.0' host='0.0.0.0' - datora IP adrese
