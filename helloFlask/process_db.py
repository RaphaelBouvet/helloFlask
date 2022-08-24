from cgitb import reset
import pandas as pd
import numpy as np
from io import BytesIO
import base64
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import sqlite3


def process_database():
    pren = pd.read_csv('databases/dpt2020.zip', sep=";")  

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

def return_random(db):
    l_unique = db['prenom'].unique()
    prenom = np.random.choice(l_unique)
    return prenom

def connect_db_msg():
    con = sqlite3.connect('databases/db_commentary.db')
    db = pd.read_sql("SELECT * from comments", con,index_col='index',columns=['msg_string','msg_sentiment_analised'])
    return db

def save_msg(msg):
    db = connect_db_msg()
    user_id = len(db)
    msg = pd.DataFrame(zip([msg],['nd']),columns=db.columns,index=[user_id])
    con = sqlite3.connect('databases/db_commentary.db')
    msg.to_sql("comments", con, if_exists='append')


if __name__ == '__main__':
    print('Testing plots')
    con = sqlite3.connect('databases/db_commentary.db')
    db = pd.read_sql("SELECT * from comments", con,index_col='index',columns=['msg_string','msg_sentiment_analised'])
    print(db)
    msg = "j'aime pas le site"
    user_id = len(db)
    print(user_id)
    msg = pd.DataFrame(zip([msg],['nd']),columns=['string','sentiment'])
    print(msg)
    db = pd.concat((db,msg)).reset_index(drop=True)
    print(db)
    con = sqlite3.connect('databases/db_commentary.db')
    db.tail(1).to_sql("comments", con, if_exists='append')
