from flask import Flask, render_template, request, flash
from process_db import connect_db_msg, process_database,plot_nom, return_random, save_msg
from os import system

system('clear')
secret_key='totally_secret_do_not_copy_key'

db = process_database()

app = Flask(__name__) 
app.secret_key = secret_key

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'GET':
        return render_template('base.html',title = 'Site de Raphaël')
    elif request.method == 'POST':
        flash('Merci pour le commentaire', category='info')
        data = request.form
        msg = data['message']
        save_msg(msg)
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

@app.route('/about')
def about():
    return render_template('about.html')

app.run(debug=True)