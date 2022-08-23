from flask import Flask, render_template,request
from process_db import process_database,plot_nom
from os import system

system('clear')


db = process_database()
app = Flask(__name__) 

@app.route("/")
def form():
    return  render_template ('index.html', title="L'Evaluateur de Prénom")

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

app.run()