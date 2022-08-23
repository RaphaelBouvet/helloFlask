from crypt import methods
from urllib import request
from flask import Flask, render_template,request
from jinja2 import Environment

app = Flask(__name__) # instantiation application

@app.route("/")
def form():
    return  render_template ('index.html', title="L'Evaluateur de Prénom")

@app.route("/visualise", methods= ['POST', 'GET'])
def visualise():
    if request.method == 'GET':
        return f"Merci d'utiliser le formulaire pour la visualisation"
    elif request.method == 'POST':
        form_data = request.form
        prenom = form_data['Name']
        date = form_data['date']
        return render_template('visualise.html',**form_data)

app.run()