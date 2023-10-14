# Liberias
import os
import json
import numpy as np
import pandas as pd

# Ruta de la carpeta que contiene los archivos JSON
#ruta_datos = "C:/Users/54280/Documents/GitHub/proyectogrupal/Pruebas/metadata-sitios"

# no modificar
folder_data = "1_data_extract"
folder_pipeline = "2_pipeline"
folder_output = "3_output"
folder_gmaps = "gmaps"
folder_metadata = "metadata-sitios"

#### CONSOLIDAR DF
# Lista para almacenar los DataFrames de datos JSON
data_frames = []

#Itero sobre los archivos JSON en la carpeta
for filename in os.listdir(os.path.join(folder_data,folder_gmaps,folder_metadata)):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_data,folder_gmaps,folder_metadata, filename)
        # Leo el archivo JSON y creo un DataFrame
        with open(file_path, 'r', encoding='utf-8') as file:
            data = pd.read_json(file, lines=True)
        data_frames.append(data)

# Combino todos los DataFrames de datos JSON en uno
df_gmaps = pd.concat(data_frames, ignore_index=True)
####

#### FILTRAR POR CATEGORIA
# Saco la lista que compone category y la dejo como texto para explorarla
df_exploded = df_gmaps.explode('category')

# Lista de palabras clave
palabras_clave = ["restaurant", "food", "cafe", "diner", "bakery", "lunch", "brunch"]

# Combino palabras clave en un patrón de búsqueda con '|'
patron_busqueda = '|'.join(palabras_clave)

# Eliminar registros con valores faltantes en la columna "category"
df_exploded = df_exploded.dropna(subset=['category'])

# Convertir la columna "category" a minúsculas y eliminar espacios en blanco
df_exploded['category'] = df_exploded['category'].str.lower().str.strip()

# Filtrar los registros que contienen cualquier parte de las palabras clave en la columna "category"
data_gmaps_metadata = df_exploded[df_exploded['category'].str.contains(patron_busqueda, case=False)].copy()
####

#### FILTRAR POR hours-state
# Creo una nueva columna 'hours-state_cat' en función de las etiquetas existentes
def categorizar_estado(row):
    if pd.notna(row) and ('Open' in row or '24 hours' in row):
        return 'Open'
    elif pd.notna(row) and 'Temporarily closed' in row:
        return 'Temporarily closed'
    elif pd.notna(row) and 'Permanently closed' in row:
        return 'Permanently closed'
    else:
        return 'Specific Hours'

data_gmaps_metadata['hours-state_cat'] = data_gmaps_metadata['state'].apply(categorizar_estado).copy()

# Elimino las filas donde 'hours-state_cat' es 'Permanently closed'
data_gmaps_metadata = data_gmaps_metadata.loc[
    data_gmaps_metadata['hours-state_cat'] != 'Permanently closed'].drop(
    columns=[
        "relative_results"
        #,"hours"
        ,"state"]
    ).copy()
####

#### REMOVER DUPLICADOS EN COLUMNAS CON LISTAS: hours, MISC

## Columnas de interes
column_nonlist = [
    "gmap_id"
    ,"name"
    ,"address"
    ,"description"
    ,"latitude"
    ,"longitude"
    ,"category"
    ,"avg_rating"
    ,"num_of_reviews"
    ,"price"
    #,"MISC"
    #,"hours"
    ,"hours-state_cat"
    ]
column_list_misc = [
    "gmap_id"
    ,"MISC"
    #,"hours"
    ]
column_list_hours = [
    "gmap_id"
    #,"MISC"
    ,"hours"
    ]

## PRIMERO: column_nonlist
# nos quedamos con las filas unicas de las columnas sin listas
data_gmaps_metadata_nonlist = data_gmaps_metadata[
    column_nonlist].drop_duplicates().sort_values(by=['gmap_id']).copy()

# Contamos el numero de caracteres en 'category'
data_gmaps_metadata_nonlist["category_length"] = data_gmaps_metadata_nonlist["category"].str.len()
# Nos quedamos con los valores en 'category_length'que contienen mayor info; 
# keep='last' corresponde a la fila donde 'category_length' es mas alto
data_gmaps_metadata_nonlist_dupslen = data_gmaps_metadata_nonlist[
    data_gmaps_metadata_nonlist.duplicated(
        subset=['gmap_id'],keep='last')
    ].sort_values(by=['gmap_id','category_length']).drop(columns=['category_length'])

# df con datos sin las filas con datos duplicados
data_gmaps_metadata_nonlist_unique = data_gmaps_metadata_nonlist[
    ~data_gmaps_metadata_nonlist.duplicated(
        subset=['gmap_id'],keep=False)
    ].sort_values(by=['gmap_id']).drop(columns=['category_length'])

# unimos el df sin las filas con datos duplicados
# y el df con las filas con mayor informacion
data_gmaps_metadata_nonlist_sindups = pd.concat(
    [data_gmaps_metadata_nonlist_unique,
     data_gmaps_metadata_nonlist_dupslen])

## SEGUNDO: column_list_hours
data_gmaps_metadata_hours = data_gmaps_metadata[
    column_list_hours].dropna(subset=['hours']).copy()
data_gmaps_metadata_hours['hours_list'] = [list(map(tuple, lst)) for lst in data_gmaps_metadata_hours.hours]
data_gmaps_metadata_hours_list = data_gmaps_metadata_hours.drop(columns=['hours']).copy()

# para que drop_duplicates acepte las columnas anidadas, transformamos las columas en tuple
data_gmaps_metadata_hours_sindups = data_gmaps_metadata_hours_list.assign(
        hours_list = data_gmaps_metadata_hours_list['hours_list'].map(tuple)
        ).drop_duplicates()
# regresamos a su formato inicial la columna hours
data_gmaps_metadata_hours_2join = pd.merge(
    left=data_gmaps_metadata_hours_sindups,
    right=data_gmaps_metadata_hours.drop(
        columns=['hours_list']).reset_index().drop_duplicates(subset='index').set_index('index'),
    how='left').drop(columns=['hours_list'])

## TERCERO: column_list_misc
data_gmaps_metadata_misc = data_gmaps_metadata[
    column_list_misc].dropna(subset=['MISC']).copy()

# para que drop_duplicates acepte las columnas anidadas, transformamos las columas en tuple
data_gmaps_metadata_misc = data_gmaps_metadata[
    column_list_misc].dropna(subset=['MISC']).copy()
data_gmaps_metadata_misc_sindups = data_gmaps_metadata_misc.assign(
    MISC = data_gmaps_metadata_misc['MISC'].map(tuple)
    ).rename(
        columns={'MISC':'misc_tuple'}
        ).drop_duplicates().sort_values(by=['gmap_id'])
# regresamos a su formato inicial la columna misc
data_gmaps_metadata_misc_2join = pd.merge(
    left=data_gmaps_metadata_misc_sindups,
    right=data_gmaps_metadata_misc.reset_index().drop_duplicates(subset='index').set_index('index'),
    how='left').drop(columns=['misc_tuple'])

## CUARTO: Unimos los dfs
# hacemos un left join donde nonlist es nuestro df de referencia.
data_gmaps_metadata_sindups = pd.merge(pd.merge(
    left=data_gmaps_metadata_nonlist_sindups,
    right=data_gmaps_metadata_hours_2join,
    how='left'),
    right=data_gmaps_metadata_misc_2join,
    how='left')

#### EXPORTAR DF FINAL
# Exporto df_filtrado para probar union por latitud y longitud con la base de yeld
data_gmaps_metadata_sindups.to_parquet(
    os.path.join(folder_pipeline,'gmaps_metadata_limpio.parquet'))
####
