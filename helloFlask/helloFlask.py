from flask import Flask # import de l’objet Flask

app = Flask(__name__) # instantiation application
@app.route("/")

def home():
    return "<p>Bienvenue chez moi</p>" # association d’une route (URL) avec la fonction ‘home()’
# on renvoie une chaîne de caractères

app.run()