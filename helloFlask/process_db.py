from turtle import color
import pandas as pd
import numpy as np
from io import BytesIO
import base64
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


def process_database():
    pren = pd.read_csv('helloFlask/databases/dpt2020.zip', sep=";")  

    pren = pren.astype({'sexe':"category",
                        'preusuel':'O',
                        'annais':"category",
                        'dpt':"category",
                        'nombre':'int16'
                            })

    dic_rename={'preusuel':'prenom',
                'annais':'annee'}
    pren = pren.rename(dic_rename, axis=1)
    pren['prenom'] = pren.prenom.str.lower()
    pren['sexe'].replace({1: 'm', 2: 'f'},inplace=True)
    pren = pren[pren['annee'].str.contains("XXXX")==False]

    return pren


def plot_nom(rgex,annee,dataframe):
    """
    Prend une expression régulière et recherche celle ci dans une data frame 
    possédant une col prénom pour calcul de l'occurence en fonction des années
    """
    recherche = dataframe[dataframe['prenom'].str.contains(rgex,regex=True)==True]   
    recherche = recherche[['nombre','annee']].groupby(['annee'],observed=True).sum().sort_index()
    print(recherche)
    y_recherche = recherche.values
    x = [int(year) for year in recherche.index]
    
    fig = Figure()
    ax = fig.subplots()
    
    ax.plot(x, y_recherche, color='blue')
    ax.axvline(annee)
    ax.set_xlabel('Année de Naissance')
    ax.set_ylabel(f'Occurence du prénom {rgex}')

    buf = BytesIO()
    # fig.savefig(buf, format="png")
    FigureCanvas(fig).print_png(buf)

    # data = base64.b64encode(buf.getbuffer()).decode("ascii")
    image = "data:image/png;base64,"
    image += base64.b64encode(buf.getvalue()).decode('utf8')
    return image

if __name__ == '__main__':
    print('Testing plots')
    db = process_database()
    plot_nom('raphael', 1993, db)
