from flask import Flask, render_template,request
from process_db import process_database,plot_nom, return_random
from os import system

system('clear')

db = process_database()
app = Flask(__name__) 

@app.route('/')
def index():
    return render_template('base.html',title = 'Site de Raphaël')

@app.route("/prenom")
def prenom():
    return  render_template('prenom.html', title="L'Evaluateur de Prénom")

@app.route("/visualise", methods= ['POST', 'GET'])
def visualise():
    if request.method == 'GET':
        return f"Merci d'utiliser le formulaire pour la visualisation"
    elif request.method == 'POST':
        form_data = request.form
        prenom = form_data['prenom']
        annee = int(form_data['date'])# a changer
        img = plot_nom(prenom,annee,db)
        
        # return f"<img src='data:image/png;base64,{data}'/>"
        return render_template('visualise.html', image=img)

@app.route("/generator", methods = ['POST', 'GET'])
def generateur():
    if request.method == 'GET':
        return render_template('generateur.html', title="Generateur de Prénom")
    elif request.method == 'POST':
        prenom = return_random(db)
        img = plot_nom(prenom,2020,db)
        return render_template('generated.html', prenom=prenom, image=img)


app.run(debug=True)