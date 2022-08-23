from flask import Flask, render_template
from jinja2 import Environment

app = Flask(__name__) # instantiation application

@app.route("/")
def home():
    return  render_template ('index.html', title="L'Evaluateur de Prénom")

@app.route("/visualise")
def visualise():
    return render_template('visualise.html', title = 'Raphaël', text = 'est un escargot tout chaud')



app.run()