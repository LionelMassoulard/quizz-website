# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 21:12:58 2020

@author: Lionel Massoulard
"""


import flask

import os.path
from glob import glob

import pandas as pd
import numpy as np

    
# Create the application.
app = flask.Flask(__name__)


configuration = {
        "img_height":512,
        "img_width":512,
        "black_height":64,
        "black_width":64,
}



def get_grid(img_height,black_height, img_width, black_width, **kwargs):
    nb_of_rows = int(img_width / black_width)
    nb_of_cols = int(img_height / black_height)
    
    all_positions = []
    for i in range(nb_of_rows):
        for j in range(nb_of_cols):
            all_positions.append((i*black_width, j*black_height))
    
    return [{"ind":ind, "left":l,"top":t} for ind,(l,t) in enumerate(all_positions)]


@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    
    return "Welcome" 

@app.route('/quiz/<category>/<int:nb>')
def quiz(category, nb):
    all_positions = get_grid(**configuration)
    if nb > len(blasons) - 1:
        nb = -1
        
    nb_blacks=len(all_positions)
    np.random.seed(nb+SEED)
    black_order = np.arange(nb_blacks)
    np.random.shuffle(black_order)
    black_order = [int(b) for b in black_order]
    

    blason_name = BLASONS[category][nb]
    return flask.render_template('quiz.html',
                                 nb_blacks=nb_blacks,
                                 all_positions=all_positions,
                                 blason_name=blason_name,
                                 blason_link=INV_MAPPING[category][blason_name],
                                 nb=nb,
                                 category=category,
                                 black_order=black_order,
                                 **configuration)


def create_file_mapping():
    files = glob(".\static\*-256px.png")
    
    all_map = []
    for f in files:
        folder, base_name = os.path.split(f)
        cleaned_name = base_name.replace("-2014-v01-256px.png","").replace("-"," ").title()
        
        all_map.append((base_name, cleaned_name))
        
    return pd.DataFrame(all_map, columns=["base_name","cleaned_name"])
    
if False:
    df = create_file_mapping()
    df.to_csv(".\mapping.csv", index=False)
        
    
def load_mapping():
    df = pd.read_csv(".\mapping.csv", encoding="utf-8", sep=",")
    df.loc[df["category"].isnull(), "category"] = "hard"

    mapping = {}
    inv_mapping = {}    
    for g, group in df.groupby("category"):
        mapping[g] = {base_name:cleaned_name for base_name, cleaned_name in zip(group["base_name"], group["cleaned_name"])}
        inv_mapping[g] = {v:k for k,v in mapping[g].items()}
    return mapping, inv_mapping






#@app.route('/test')
#def test():
#    return flask.render_template('test.html')

if __name__ == '__main__':
    
    _ , INV_MAPPING = load_mapping()
    SEED = 123

    np.random.seed(SEED)
    BLASONS = {}
    for k, v in INV_MAPPING.items():
        
        blasons = list(v)
        order   = np.arange(len(blasons))
        np.random.shuffle(order)
        order   = list(order)
        blasons = [blasons[o] for o in order]
        BLASONS[k] = blasons
    
    app.debug=True
    app.run()