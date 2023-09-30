import os
import json
from datetime import datetime as dt
import pandas as pd

# no modificar
folder_data = "1_external"
folder_pipeline = "2_pipeline"
folder_output = "3_output"
folder_gmaps = "gmaps"

# extraemos nombres de cada estado segun nombre de carpeta
state_name = pd.DataFrame(
    pd.DataFrame(
        os.listdir(
            os.path.join(folder_data,folder_gmaps))).rename(
                columns={0:"state"})["state"].str.split("-").str[1])

# indentificamos las columnas de interes y aquellas que se deben desanidar
vars_interes=[
    "gmap_id" # pk google maps
    ,"user_id" # pk user >> resp
    ,"name"
    ,"time"
    ,"rating"
    ,"text"
    #,"pics" # irrelevante
    #,"resp" # desanidar
    ]

vars_desanidar=[
    "gmap_id" # pk google maps
    ,"user_id" # pk user >> resp
    ,"time" # pk user >> resp
    ,"resp" # desanidar
    ]

for i in range(min(state_name.index),max(state_name.index)):

    # creamos una variable con el nombre de estado
    # para facilitar el loop para todos los estados
    state = state_name["state"][i]
    folder_state = "review-" + str(state)

    # contamos numero de archivos al interior de cada carpeta del estado
    # para facilitar el loop
    count_file = 0
    # Iterate
    for path in os.listdir(os.path.join(folder_data,folder_gmaps,folder_state)):
        # check if current path is a file
        if os.path.isfile(os.path.join(folder_data,folder_gmaps,folder_state,path)):
            count_file += 1

    # extraemos la informacion
    data = []
    for f in range(1, count_file):
        with open(os.path.join(
            folder_data,folder_gmaps,folder_state, str(f) + ".json"), "r") as file:
            for line in file:
                data.append(json.loads(line))
    gmaps_state = pd.DataFrame(data)

    # nos concentramos en: vars_desanidar
    gmaps_state_dsndr = pd.DataFrame(gmaps_state[vars_desanidar]).dropna(subset=["gmap_id","user_id"])
    gmaps_state_dsndr.rename(
        columns={"time":"user_time"},
        inplace=True
        )

    # se normaliza la columna
    gmaps_state_dsndr = gmaps_state_dsndr.set_index(["gmap_id","user_id","user_time"])
    gmaps_state_dsndda = pd.json_normalize(
        gmaps_state_dsndr["resp"]).set_index(gmaps_state_dsndr.index) # type: ignore
    gmaps_state_dsndda.reset_index(inplace=True) # mueve le indice a una columna
    # renombramos para facilitar la union mas abajo
    gmaps_state_dsndda.rename(
        columns={"time":"resp_time","text":"resp_text"},
        inplace=True
        )
    # solo incluimos las variables de interes
    gmaps_state_interes = gmaps_state[vars_interes].copy().dropna(
        subset=["gmap_id","user_id"]) # type: ignore
    # renombramos para facilitar la union mas abajo
    gmaps_state_interes.rename(
        columns={"name":"user_name","time":"user_time","text":"user_text"},
        inplace=True
        )

    # unir los dataframes
    gmaps_state_norm = pd.merge(
        gmaps_state_interes,
        gmaps_state_dsndda,
        on=["gmap_id","user_id","user_time"],
        how="left")

    # generamos una columna state
    # para facilitar la union de todos los datos
    gmaps_state_norm["state"] = state

    # movemos 'state' a la primera fila para facilitar la visualizacion
    first_column = gmaps_state_norm.pop("state")
    gmaps_state_norm.insert(0, "state", first_column)
    
    # Convierte la columna 'user_time' a datetime y almacena el resultado en una nueva columna 'time_total'
    gmaps_state_norm['user_time_year'] = pd.to_datetime(gmaps_state_norm['user_time'], unit='ms').dt.year # type: ignore
    gmaps_state_norm['user_time_month'] = pd.to_datetime(gmaps_state_norm['user_time'], unit='ms').dt.month # type: ignore
    gmaps_state_norm['user_time_day'] = pd.to_datetime(gmaps_state_norm['user_time'], unit='ms').dt.day # type: ignore
    gmaps_state_norm['user_time_hms'] = pd.to_datetime(gmaps_state_norm['user_time'], unit='ms').dt.time # type: ignore
    gmaps_state_norm['resp_time_year'] = pd.to_datetime(gmaps_state_norm['resp_time'], unit='ms').dt.year # type: ignore
    gmaps_state_norm['resp_time_month'] = pd.to_datetime(gmaps_state_norm['resp_time'], unit='ms').dt.month # type: ignore
    gmaps_state_norm['resp_time_day'] = pd.to_datetime(gmaps_state_norm['resp_time'], unit='ms').dt.day # type: ignore
    gmaps_state_norm['resp_time_hms'] = pd.to_datetime(gmaps_state_norm['resp_time'], unit='ms').dt.time # type: ignore

    # Removemos duplicados
    gmaps_state_norm.drop_duplicates(inplace=True)
    
    # df final por estado
    # guardamos en pipeline con el fin de alivianar la carga al RAM local
    gmaps_state_norm.to_parquet(
        os.path.join(folder_pipeline,folder_gmaps, str(folder_state) + "_norm.parquet"))