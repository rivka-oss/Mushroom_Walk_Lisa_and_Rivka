from flask import Flask, render_template, request 
from collections import defaultdict
import os
import pandas as pd



app = Flask(__name__)

data = pd.read_csv("C:/Users/rivka/OneDrive/Bureau/.venv/Github/data/mushrooms.csv")


FIELDNAMES = [
"class", "cap-shape", "cap-surface", "cap-color", "bruises", "odor",
"gill-attachment", "gill-spacing", "gill-size", "gill-color",
"stalk-shape", "stalk-root", "stalk-surface-above-ring", "stalk-surface-below-ring",
"stalk-color-above-ring", "stalk-color-below-ring", "veil-type", "veil-color",
"ring-number", "ring-type", "spore-print-color", "population", "habitat"
]

def load_mushrooms():
    return data.copy()


groups = {
"Cap characteristics": ['cap-shape', 'cap-surface', 'cap-color'],
"Gill characteristics": ['gill-attachment', 'gill-spacing', 'gill-size', 'gill-color'],
"Stalk characteristics": ['stalk-shape', 'stalk-root',
'stalk-surface-above-ring', 'stalk-surface-below-ring',
'stalk-color-above-ring', 'stalk-color-below-ring'],
"Veil & Ring characteristics": ['veil-type', 'veil-color',
'ring-number', 'ring-type'],
"Other characteristics": ['bruises', 'odor', 'spore-print-color'],
"Environmental characteristics": ['population', 'habitat']
}

class_name = {"e":"edible","p":"poisonous"}

cap_shape_name = {
    "b": "bell", "c": "conical", "x": "convex",
    "f": "flat", "k": "knobbed", "s": "sunken"
}

cap_surface_name = {
    "f": "fibrous", "g": "grooves",
    "y": "scaly", "s": "smooth"
}

cap_color_name = {
    "n": "brown", "b": "buff", "c": "cinnamon",
    "g": "gray", "r": "green", "p": "pink",
    "u": "purple", "e": "red", "w": "white",
    "y": "yellow"
}

bruises_name = {
    "t": "bruises", "f": "no"
}

odor_name = {
    "a": "almond", "l": "anise", "c": "creosote",
    "y": "fishy", "f": "foul", "m": "musty",
    "n": "none", "p": "pungent", "s": "spicy"
}

gill_attachment_name = {
    "a": "attached", "d": "descending",
    "f": "free", "n": "notched"
}

gill_spacing_name = {
    "c": "close", "w": "crowded", "d": "distant"
}

gill_size_name = {
    "b": "broad", "n": "narrow"
}

gill_color_name = {
    "k": "black", "n": "brown", "b": "buff",
    "h": "chocolate", "g": "gray", "r": "green",
    "o": "orange", "p": "pink", "u": "purple",
    "e": "red", "w": "white", "y": "yellow"
}

stalk_shape_name = {
    "e": "enlarging", "t": "tapering"
}

stalk_root_name = {
    "b": "bulbous", "c": "club", "u": "cup",
    "e": "equal", "z": "rhizomorphs",
    "r": "rooted", "?": "missing"
}

stalk_surface_above_ring_name = {
    "f": "fibrous", "y": "scaly",
    "k": "silky", "s": "smooth"
}

stalk_surface_below_ring_name = {
    "f": "fibrous", "y": "scaly",
    "k": "silky", "s": "smooth"
}

stalk_color_above_ring_name = {
    "n": "brown", "b": "buff", "c": "cinnamon",
    "g": "gray", "o": "orange", "p": "pink",
    "e": "red", "w": "white", "y": "yellow"
}

stalk_color_below_ring_name = {
    "n": "brown", "b": "buff", "c": "cinnamon",
    "g": "gray", "o": "orange", "p": "pink",
    "e": "red", "w": "white", "y": "yellow"
}

veil_type_name = {
    "p": "partial", "u": "universal"
}

veil_color_name = {
    "n": "brown", "o": "orange",
    "w": "white", "y": "yellow"
}

ring_number_name = {
    "n": "none", "o": "one", "t": "two"
}

ring_type_name = {
    "c": "cobwebby", "e": "evanescent",
    "f": "flaring", "l": "large", "n": "none",
    "p": "pendant", "s": "sheathing", "z": "zone"
}

spore_print_color_name = {
    "k": "black", "n": "brown", "b": "buff",
    "h": "chocolate", "r": "green", "o": "orange",
    "u": "purple", "w": "white", "y": "yellow"
}

population_name = {
    "a": "abundant", "c": "clustered",
    "n": "numerous", "s": "scattered",
    "v": "several", "y": "solitary"
}

habitat_name = {
    "g": "grasses", "l": "leaves", "m": "meadows",
    "p": "paths", "u": "urban", "w": "waste",
    "d": "woods"
}



value_names = {
    "class": class_name,
    "cap-shape": cap_shape_name,
    "cap-surface": cap_surface_name,
    "cap-color": cap_color_name,
    "bruises": bruises_name,
    "odor": odor_name,
    "gill-attachment": gill_attachment_name,
    "gill-spacing": gill_spacing_name,
    "gill-size": gill_size_name,
    "gill-color": gill_color_name,
    "stalk-shape": stalk_shape_name,
    "stalk-root": stalk_root_name,
    "stalk-surface-above-ring": stalk_surface_above_ring_name,
    "stalk-surface-below-ring": stalk_surface_below_ring_name,
    "stalk-color-above-ring": stalk_color_above_ring_name,
    "stalk-color-below-ring": stalk_color_below_ring_name,
    "veil-type": veil_type_name,
    "veil-color": veil_color_name,
    "ring-number": ring_number_name,
    "ring-type": ring_type_name,
    "spore-print-color": spore_print_color_name,
    "population": population_name,
    "habitat": habitat_name
}



def filter_mushrooms(mushrooms):

    characteristic = request.args.get("characteristic", "")
    selected_value = request.args.get("value", "")

    if characteristic and selected_value:
        mushrooms = mushrooms[
            mushrooms[characteristic].astype(str) == selected_value
        ]

    return mushrooms

@app.get("/")

def index():
    print(os.path.exists("static/style.css"))
    all_mushrooms = load_mushrooms()
    
    for column, mapping in value_names.items():
        all_mushrooms[column] = all_mushrooms[column].replace(mapping)
    selected_group = request.args.get("group", "")
    selected_characteristic = request.args.get("characteristic", "")
    selected_value = request.args.get("value", "")

    characteristics = groups.get(selected_group, [])

    if selected_characteristic not in characteristics:
        selected_characteristic = ""
        selected_value = ""

    # Initialiser les valeurs
    values = []
    if selected_characteristic:
        values = sorted(
        all_mushrooms[selected_characteristic]
        .dropna()
        .loc[lambda s: s != "?"]
        .astype(str)
        .unique()
    )
           

    
    if selected_value not in values:
        selected_value = ""

    mushrooms = filter_mushrooms(all_mushrooms)
    mushrooms = mushrooms.to_dict(orient="records")
    all_mushrooms_records = all_mushrooms.to_dict(orient="records")
  
    # ATTENTION--- ANALYSE CIBLÉE (VARIABLE + HABITAT) ---
    target_var = request.args.get("target_var", "class")
    target_habitat = request.args.get("target_habitat", "")
    available_vars = [f for f in FIELDNAMES if f != "habitat"]
    
    if target_var not in available_vars:
        target_var = "class"
    # Filtrer les champignons selon l'habitat choisi (si un habitat est sélectionné)
    
    subset = all_mushrooms_records

    if target_habitat:
        subset = [
            m for m in all_mushrooms_records
            if m.get("habitat") == target_habitat
        ]
  
    # Compter les occurrences de la variable choisie dans ce sous-ensemble
    var_counts = defaultdict(int)
    for m in subset:
        val = m.get(target_var, "inconnu")
        var_counts[val] += 1
# ---------------------------------------------

    habitats = sorted(all_mushrooms["habitat"].dropna().unique())
    print(type(mushrooms))
    print(type(mushrooms[0]) if mushrooms else "Liste vide")
    
    return render_template("index2.html",
                           mushrooms = mushrooms, 
                           groups = groups,
                           characteristics = characteristics,
                           values = values, 
                           selected_group = selected_group,
                           selected_characteristic=selected_characteristic,
                           selected_value=selected_value,
                           # --- Passage des variables pour l'analyse ciblée ---
                            
                            var_counts=var_counts,
                            target_var=target_var,
                            target_habitat=target_habitat,
                            available_vars=available_vars,
                            habitats=habitats,
# ---------------------------------------------------                
                           total = len(data),
                           error = "")

if __name__ == '__main__' :
    app.run(debug=True)


